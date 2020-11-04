import kydb
from portfolio_management.kydb_config import OBJDB_CONFIG
from portfolio_management.utils.sql import SQLMixin
from portfolio_management.common.base_item import Factory
import hashlib
import pandas as pd

QUERY_RESULT_CACHE = '/cache/'

class InterestRateHistory(SQLMixin, kydb.DbObj):



    @kydb.stored
    def path(self) -> str:
        return ''

    @kydb.stored
    def history(self) -> list:
        return []

SQL_TEMPLATE = '''
WITH t AS
    (SELECT date_parse(datetime,
        '%m/%d/%Y') AS dt
    FROM interest_rate
    WHERE pair = '{pair}'
            AND year = '{dt:%Y}'
SELECT *
FROM t
WHERE dt = date = '{dt:%Y-%m-%d}'        
'''


class InterestRate(SQLMixin, kydb.DbObj):
    """
    Interest rate
    Ideally we could updated tis daily from some source
    it should be independent for each currency
    """

    @staticmethod
    @kydb.stored
    def day_count():
        return 365

    @kydb.stored
    def res_s3_path(self):
        return None

    def sql(self, dt, ccy):
        dt = self._ensure_datetime(dt)

        kwargs = {'dt': dt, 'ccy': ccy}

        for k, v in self.sql_kwargs().items():
            kwargs[k] = v

        return self.sql_template().format(**kwargs)

    @kydb.stored
    def rate(self) -> float:
        return 0.31

    @kydb.stored
    def ccy(self):
        return None

    @kydb.stored
    def updated(self):
        return None

    @staticmethod
    def query(self, dt, ccy):
        query_kwargs = self.interest_rate_query_args(dt, ccy)
        hashstr = hashlib.sha224(str(query_kwargs).encode()).hexdigest()
        cache_path = QUERY_RESULT_CACHE + hashstr
        try:
            res_s3_path = self.db[cache_path]
            try:
                interest_rate = pd.read_csv(res_s3_path)
            except FileNotFoundError:
                # Cache object is there, but the s3 object expired
                raise KeyError(res_s3_path)
        except KeyError:
            query_res = self.athena_client.start_query_execution(
                **query_kwargs)
            execution_id = query_res['QueryExecutionId']
            res_s3_path = self.wait_for_results(execution_id)
            interest_rate = pd.read_csv(res_s3_path)
            self.db[cache_path] = res_s3_path

        return interest_rate

    def interest_rate_query_args(self, dt, ccy):
        return {
            'QueryString': self.sql(dt, ccy),
            'QueryExecutionContext': {
                'Database': self.database(),
            },
            'ResultConfiguration': {
                'OutputLocation': self.res_s3_path(),
            },
            'WorkGroup': 'primary'
        }

    def __str__(self):
        return '{0}:{1} {2}'.format(self.ccy(), self.rate(), self.updated())


def main():
    db = kydb.connect('memory://local')
    db.mkdir('/portfolio_management/interest_rate')
    db.upload_objdb_config(OBJDB_CONFIG)
    key = '001'
    _account = Factory.create('Account', key, id='001', ccy='USD')
    print('Account: {0}'.format(_account))
    _trx1 = Factory.create('CashTrx', db=db, amount=1000.01, ccy='USD', description='test1')
    _trx2 = Factory.create('CashTrx', db=db, amount=1000.01, ccy='USD', description='test2')
    _trx3 = Factory.create('CashTrx', db=db, amount=1000.01, ccy='EUR', description='test3')
    _account.cash_trxs().extend([_trx1, _trx2, _trx3])


if __name__ == '__main__':
    main()
