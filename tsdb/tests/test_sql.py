import kydb
from tsdb.base import TimeSeries
from tsdb.sql import TimeSeriesSQLMixin
from datetime import datetime, date

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
    'DummySqlTimeSeries': {
        'module_path': 'tsdb.tests.test_sql',
        'class_name': 'DummySqlTimeSeries'
    }
}


class DummySqlTimeSeries(TimeSeriesSQLMixin, TimeSeries):
    pass


def test_sql():
    db = kydb.connect('memory://db')
    db.upload_objdb_config(OBJDB_CONFIG)
    sql_template_path = '/templates/my_test_template.sql'
    db[sql_template_path] = SQL_TEMPLATE
    ts = db.new('DummySqlTimeSeries', '/fxcm/GBPUSD_MINUTELY',
                sql_template_path=sql_template_path,
                sql_kwargs={'pair': 'GBPUSD'})

    expected = '''
WITH t AS
    (SELECT date_parse(datetime,
        '%m/%d/%Y %H:%i:%S.000') AS dt,
        (bidclose+askclose) / 2 AS closeprice
    FROM fxcm
    WHERE pair = 'GBPUSD'
            AND year BETWEEN '2017' AND '2017')
SELECT *
FROM t
WHERE dt
    BETWEEN timestamp '2017-05-01 00:00:00.000'
        AND timestamp '2017-05-02 00:00:00.000'
'''
    actual = ts.sql(datetime(2017, 5, 1), datetime(2017, 5, 2))
    assert actual == expected

    actual = ts.sql(date(2017, 5, 1), date(2017, 5, 2))
    assert actual == expected
