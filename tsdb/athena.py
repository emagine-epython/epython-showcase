import kydb
import hashlib
import boto3
import time
import pandas as pd
import numpy as np
from .base import TimeSeries
from datetime import date, datetime
from .sql import TimeSeriesSQLMixin
from typing import Union

QUERY_RESULT_CACHE = '/cache/'


class AthenaTimeSeriesException(Exception):
    pass


class AthenaTimeSeries(TimeSeriesSQLMixin, TimeSeries):
    def init(self):
        self.athena_client = boto3.client('athena')

    @kydb.stored
    def database(self) -> str:
        return ''

    @kydb.stored
    def res_s3_path(self) -> str:
        return ''

    def _athena_query_kwargs(self,
                             start_dt: Union[date, datetime],
                             end_dt: Union[date, datetime]) -> dict:
        return {
            'QueryString': self.sql(start_dt, end_dt),
            'QueryExecutionContext': {
                'Database': self.database(),
            },
            'ResultConfiguration': {
                'OutputLocation': self.res_s3_path(),
            },
            'WorkGroup': 'primary'
        }

    def curve(self,
              start_dt: Union[date, datetime],
              end_dt: Union[date, datetime]) -> pd.DataFrame:

        query_kwargs = self._athena_query_kwargs(start_dt, end_dt)
        hashstr = hashlib.sha224(str(query_kwargs).encode()).hexdigest()
        cache_path = QUERY_RESULT_CACHE + hashstr
        try:
            res_s3_path = self.db[cache_path]
            try:
                price_df = pd.read_csv(res_s3_path)
            except FileNotFoundError:
                # Cache object is there, but the s3 object expired
                raise KeyError(res_s3_path)
        except KeyError:
            query_res = self.athena_client.start_query_execution(
                **query_kwargs)
            execution_id = query_res['QueryExecutionId']
            res_s3_path = self.wait_for_results(execution_id)
            price_df = pd.read_csv(res_s3_path)
            self.db[cache_path] = res_s3_path

        price_df['dt'] = price_df.dt.apply(lambda x: np.datetime64(x[:19]))
        return price_df.set_index('dt')

    def wait_for_results(self, execution_id: int, max_execution=30,
                         sleep_time=1):
        state = 'RUNNING'

        while (max_execution > 0 and state in ['RUNNING', 'QUEUED']):
            max_execution = max_execution - 1
            response = self.athena_client.get_query_execution(
                QueryExecutionId=execution_id)

            if 'QueryExecution' in response and \
                    'Status' in response['QueryExecution'] and \
                    'State' in response['QueryExecution']['Status']:
                state = response['QueryExecution']['Status']['State']
                if state == 'FAILED':
                    raise AthenaTimeSeriesException(
                        f'Execution{execution_id} failed: {response}')

                elif state == 'SUCCEEDED':
                    s3_path = response['QueryExecution']['ResultConfiguration'
                                                         ]['OutputLocation']
                    return s3_path
            time.sleep(sleep_time)

        raise TimeoutError(f'Failed to wait for {execution_id}')
