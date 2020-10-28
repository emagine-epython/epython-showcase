import kydb
import pandas as pd
import pytest
from datetime import datetime
from qpython import qconnection
from qpython.qtype import QException

OBJDB_CONFIG = {
    'KDBTimeSeries': {
        'module_path': 'tsdb.kdb',
        'class_name': 'KDBTimeSeries'
    }
}

COMMANDS = [
    't:([] dt:(); v: ())',
    '`t insert (1602192606.08, 100.2)',
    '`t insert (1602192666.08, 100.5)',
    '`t insert (1602192726.08, 100.3)',
]


kdb_available = pytest.mark.skipif(True, reason='require conneciton to KDB+')


@kdb_available
@pytest.fixture
def ts():
    with qconnection.QConnection(host='localhost', port=5001) as q:
        for cmd in COMMANDS:
            try:
                q(cmd)
            except QException as msg:
                print('q error: \'%s' % msg)

    db = kydb.connect('memory://kdb')
    db.upload_objdb_config(OBJDB_CONFIG)
    ts = db.new('KDBTimeSeries', '/Bloomerg/VOD.L')

    return ts


@kdb_available
def test_kdb(ts):
    res = ts.curve(
        datetime(2020, 10, 8, 22, 31, 6),
        datetime(2020, 10, 8, 23))

    data = [
        (1602192666.08, 100.5),
        (1602192726.08, 100.3)
    ]

    expected = pd.DataFrame(data, columns=['dt', 'v'])
    pd.testing.assert_frame_equal(res, expected)


@kdb_available
def test_cmd(ts):
    cmd = ts.q_cmd(
        datetime(2020, 10, 8, 22, 31, 6),
        datetime(2020, 10, 8, 23))

    assert cmd == 'select from t where dt>=1602192666.0,dt<=1602194400.0'
