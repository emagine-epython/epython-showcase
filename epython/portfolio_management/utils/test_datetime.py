import datetime
import pytest

@pytest.fixture
def datetime_items():
    _now = datetime.datetime.now()
    items = {'now': _now,
    'time_delta': datetime.timedelta(minutes=10),
    'date_delta': datetime.timedelta(days=1),
    'today': datetime.datetime(_now.year, _now.month, _now.day),
    'dates': [_now - datetime.timedelta(days=4),
             _now - datetime.timedelta(days=3, hours=5),
             _now - datetime.timedelta(days=2, hours=1)]
             }
    return items
