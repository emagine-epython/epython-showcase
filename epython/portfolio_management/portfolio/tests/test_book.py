from portfolio_management.common.base_item import Factory
from portfolio_management.portfolio.event import Event, EventType
from portfolio_management.portfolio.deal import DealEq, DealFx
from portfolio_management.portfolio.instrument import Instrument, InstrumentFx
from test_db import db
from portfolio_management.utils.test_datetime import datetime_items
import mock


def setup_book(db, datetime_items):
    _event = Factory.create('Event', db=db, event_type=EventType.Open)
    assert (isinstance(_event, Event))

    _book1 = Factory.create('Book', db=db)

    _instrument1 = Factory.create('Instrument', db=db, name='Apple', id='AAP',
                                  instrument_type='equity', category='Nasdaq', symbol='AAP',
                                  description='Apple stock', venue='NYSE')
    print('Instrument: {0}'.format(_instrument1))

    _deal1 = Factory.create('DealEq', db=db, state=_event, instrument=_instrument1, price=2.24, qty=1000, ccy='USD',
                            updated=datetime_items['today'])
    print('Deal: {0}'.format(_deal1))

    _instrument2 = Factory.create('InstrumentFx', db=db, ccy_pair='EURUSD',
                                  instrument_type='fx', category='spot', venuw='NYSE')
    _deal2 = Factory.create('DealFx', db=db, state=_event, instrument=_instrument2, rate=1.1747, qty=1000, ccy1='EUR',
                            ccy2='USD', ccy1_amount=1000, ccy2_amount=1000/1.747, updated=datetime_items['today'])

    _instrument3 = Factory.create('Instrument', db=db, name='Google', id='GOOGL', instrument_type='equity',
                                  category='Nasdaq', symbol='GOOGL', description='Google stock', venue='NYSE')
    print('Instrument: {0}'.format(_instrument1))

    _deal3 = Factory.create('DealEq', db=db, state=_event, instrument=_instrument3, price=3.24, qty=200, ccy='USD',
                            direction='S')

    print('Deal: {0}'.format(_deal3))

    _instrument4 = Factory.create('InstrumentFx', db=db, ccy_pair='EURUSD', id='EURUSD', instrument_type='fx',
                                  category='spot', venue='NYSE')
    _deal4 = Factory.create('DealFx', db=db, state=_event, instrument=_instrument4, rate=1.1747, qty=2200, ccy1='EUR',
                            ccy2='USD', ccy1_amount=2200, ccy2_amount=2200/1.1747, direction='S')

    _book1.add(_book1.deals(), _deal1, DealEq)
    _book1.add(_book1.deals(), _deal2, DealFx)
    _book1.add(_book1.deals(), _deal3, DealEq)
    _book1.add(_book1.deals(), _deal4, DealFx)

    print('book: {0}'.format(_book1))

    _book1.add_account(Factory.create('Account', db=db, name=_book1.id(), ccy='USD'))
    _book1.add_account(Factory.create('Account', db=db, name=_book1.id(), ccy='EUR'))

    return _book1


def test_book(db, datetime_items):
    _book1 = setup_book(db, datetime_items)
    _accountUSD = [x for x in _book1.accounts() if x.ccy() == 'USD'][0]
    _accountUSD.deposit(2500, datetime_items['today'], 'funds')
    _deal3 = _book1.create_deal('DealEq', db, 'AAP', 100, 2.34, 'USD', datetime_items['today'], direction='B')
    assert(isinstance(_deal3, DealEq))
    assert (isinstance(_deal3.instrument(), Instrument))
    assert (_deal3.instrument().symbol(), 'AAP')


def test_deposit(db, datetime_items):

    _book1 = setup_book(db, datetime_items)
    _accountUSD = [x for x in _book1.accounts() if x.ccy() == 'USD'][0]
    _accountUSD.deposit(2500, datetime_items['today'], 'funds')
    assert(_accountUSD.get_balance() == 2500)


def test_withdrawal(db, datetime_items):

    _book1 = setup_book(db, datetime_items)
    _accountEUR = [x for x in _book1.accounts() if x.ccy() == 'USD'][0]
    _accountEUR.deposit(2500, datetime_items['today'], 'funds')
    assert(_accountEUR.get_balance() == 2500)
    _accountEUR.withdrawal(1500, datetime_items['today'], 'funds')
    assert (_accountEUR.get_balance() == 1000)


def test_positions(db, datetime_items):

    _book1 = setup_book(db, datetime_items)
    _positions = _book1.positions()
    print('Positions')
    for k, v in _positions.items():
        print('{0}: {1:,.2f}'.format(k, v))

    assert ('USD' in _positions)
    assert (isinstance(_positions['USD'], float))
    assert (round(_positions['USD'], 2) == -1587.59)



