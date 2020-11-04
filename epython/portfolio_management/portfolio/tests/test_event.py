from portfolio_management.portfolio.event import Event, EventType
from portfolio_management.common.base_item import Factory
from enum import Enum
import datetime
from test_db import db


def test_event(db):
    _event1 = Factory.create('Event', db=db)
    _event2 = Factory.create('Event', db=db, event_type=EventType.Amend)
    _event3 = Factory.create('Event', db=db, event_type=EventType.Amend, ts=datetime.datetime.now() + datetime.timedelta(days=1))
    print('Event1: {0}'.format(_event1))
    print('Event2: {0}'.format(_event2))
    print('Event3: {0}'.format(_event3))
