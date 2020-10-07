import kydb
import pytest
import contextlib
import pandas as pd
import numpy as np
from datetime import date
from unittest import mock
from pandas.testing import assert_frame_equal
from tsdb.athena import AthenaTimeSeriesException

SQL_TEMPLATE = '''
WITH t AS
    (SELECT date_parse(datetime,
        '%m/%d/%Y %H:%i:%S.000') AS dt,
        (bidclose+askclose) / 2 AS closeprice
    FROM fxcm
    WHERE pair = '{pair}'
            AND year BETWEEN '{start_dt:%Y}' AND '{end_dt:%Y}')
SELECT *
FROM t
WHERE dt
    BETWEEN timestamp '{start_dt:%Y-%m-%d %H:%M:%S.000}'
        AND timestamp '{end_dt:%Y-%m-%d %H:%M:%S.000}'
'''


OBJDB_CONFIG = {
    'AthenaTimeSeries': {
        'module_path': 'tsdb.athena',
        'class_name': 'AthenaTimeSeries'
    }
}


@pytest.fixture
def ts():
    db = kydb.connect('memory://db')
    db.upload_objdb_config(OBJDB_CONFIG)
    sql_template_path = '/templates/my_test_template.sql'
    db[sql_template_path] = SQL_TEMPLATE
    ts = db.new('AthenaTimeSeries', '/fxcm/GBPUSD_MINUTELY',
                database='epython-marketdata',
                res_s3_path='s3://epython-athena/result-cache/',
                sql_template_path=sql_template_path,
                sql_kwargs={'pair': 'GBPUSD'})

    return ts


def test__athena_query_kwargs(ts):
    res = ts._athena_query_kwargs(date(2017, 5, 1), date(2017, 5, 2))

    assert res['QueryExecutionContext'] == {'Database': 'epython-marketdata'}
    assert res['ResultConfiguration'] == {
        'OutputLocation': 's3://epython-athena/result-cache/'}
    assert res['WorkGroup'] == 'primary'


def test_curve(ts):
    client = mock.Mock()
    exec_id = 'test_curve'
    client.start_query_execution.return_value = {'QueryExecutionId': exec_id}
    ts.athena_client = client

    data = [
        ('2017-05-01 00:00:00.000', 1.293370),
        ('2017-05-01 00:01:00.000', 1.293440),
        ('2017-05-01 00:02:00.000', 1.293375),
        ('2017-05-01 00:03:00.000', 1.293280),
        ('2017-05-01 00:04:00.000', 1.293135)]

    price_df = pd.DataFrame(data, columns=['dt', 'closeprice'])
    expected = price_df.copy()
    expected['dt'] = expected.dt.apply(lambda x: np.datetime64(x[:19]))
    expected.set_index('dt', inplace=True)

    with contextlib.ExitStack() as stack:
        wait_for_results = stack.enter_context(
            mock.patch.object(ts, 'wait_for_results'))
        wait_for_results.return_value = 's3://my-bucket/result-cache'
        read_csv = stack.enter_context(mock.patch('pandas.read_csv'))
        read_csv.return_value = price_df.copy()
        res = ts.curve(date(2017, 5, 1), date(2017, 5, 2))

        # Check that we have the cache
        assert len(ts.wait_for_results.call_args_list) == 1
        assert_frame_equal(res, expected)
        cache_path = '/cache/6ff053d32c23e4393e97e02' \
                     'd49a7c0dd8438f88f40807303afafb4c1'

        assert ts.db[cache_path] == 's3://my-bucket/result-cache'

        # Call again and we'd see that it no longer hit wait_for_results
        read_csv.return_value = price_df.copy()
        res = ts.curve(date(2017, 5, 1), date(2017, 5, 2))
        assert len(ts.wait_for_results.call_args_list) == 1
        assert_frame_equal(res, expected)

        # The s3 result expired. Will have to query Athena
        read_csv.side_effect = [FileNotFoundError, price_df.copy()]
        res = ts.curve(date(2017, 5, 1), date(2017, 5, 2))
        assert len(ts.wait_for_results.call_args_list) == 2
        assert_frame_equal(res, expected)


def test_wait_for_results_success(ts):
    client = mock.Mock()
    output_loc = 's3://my-bucket/result-cache/abjflajsljd.csv'
    client.get_query_execution.return_value = {
        'QueryExecution': {
            'Status': {'State': 'SUCCEEDED'},
            'ResultConfiguration': {'OutputLocation': output_loc}
        }
    }
    ts.athena_client = client
    assert output_loc == ts.wait_for_results('abcde')


def test_wait_for_results_failed(ts):
    client = mock.Mock()
    client.get_query_execution.return_value = {
        'QueryExecution': {
            'Status': {'State': 'FAILED'}
        }
    }
    ts.athena_client = client

    with pytest.raises(AthenaTimeSeriesException):
        ts.wait_for_results('abcde')


def test_wait_for_results_timeout(ts):
    client = mock.Mock()
    client.get_query_execution.return_value = {
        'QueryExecution': {
            'Status': {'State': 'RUNNING'}
        }
    }
    ts.athena_client = client

    with pytest.raises(TimeoutError):
        ts.wait_for_results('abcde', max_execution=1, sleep_time=0.01)

    client.get_query_execution.return_value = {
        'QueryExecution': {
            'Status': {'State': 'QUEUED'}
        }
    }

    with pytest.raises(TimeoutError):
        ts.wait_for_results('abcde', max_execution=1, sleep_time=0.01)
