from portfolio_management.portfolio.event import Event, EventType
from portfolio_management.common.base_item import Factory
from portfolio_management.portfolio.deal import DealEq, DealFx
from portfolio_management.portfolio.deal import Instrument, InstrumentFx
from test_db import db
from portfolio_management.utils.test_datetime import datetime_items


def setup_deal(db, datetime_items):

    _event = Factory.create('Event', db=db, event_type=EventType.Open)
    assert (isinstance(_event, Event))

    _instrument1 = Factory.create('Instrument', db=db, name='Apple', id='AAP', instrument_type='equity', category='Nasdaq',
                                  symbol='AAP', description='Apple stock', venue='NYSE')
    print('Instrument: {0}'.format(_instrument1))

    _deal1 = Factory.create('DealEq', db=db, state=_event, instrument=_instrument1, price=2.24, qty=1000,
                            ccy='USD')

    print('Deal: {0}'.format(_deal1))

    _instrument2 = Factory.create('InstrumentFx', db=db, ccy_pair='EURUSD', instrument_type='fx',
                                  category='spot', venue='NYSE')

    _deal2 = Factory.create('DealFx', db=db, state=_event, instrument=_instrument2, rate=1.1747, qty=1000,
                            ccy1='EUR', ccy2='USD', ccy1_amount=1000, ccy2_amount=1000/1.1747,
                            updated=datetime_items['today'])

    return [_deal1, _deal2]


def test_deal(db, datetime_items):

    _deals = setup_deal(db, datetime_items)
    assert(isinstance(_deals[0], DealEq))
    assert (isinstance(_deals[1], DealFx))
    assert (isinstance(_deals[0].instrument(), Instrument))
    assert (isinstance(_deals[1].instrument(), InstrumentFx))

    print('Positions')
    _positions = _deals[0].positions()
    for k, v in _positions.items():
        print(k, v)
    assert('USD' in _positions)
    assert(_positions['USD'] == -2240.0)
    assert ('AAP' in _positions)
    assert (_positions['AAP'] == 1000)

    print('Positions')
    _positions = _deals[1].positions()
    for k, v in _positions.items():
        print(k, v)
    assert('EUR' in _positions)
    assert(_positions['EUR'] == 1000)
    assert('USD' in _positions)
    assert(int(_positions['USD']) == -851)

