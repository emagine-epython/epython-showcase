from portfolio_management.common.base_item import Factory
from portfolio_management.portfolio.event import Event, EventType
from portfolio_management.portfolio.book import Book
from portfolio_management.portfolio.deal import DealEq, DealFx
import datetime
from test_db import db
from portfolio_management.utils.test_datetime import datetime_items


def test_portfolio(db, datetime_items):

    _ptf = Factory.create('Portfolio', db=db)

    print('datetime_items: {0}'.format(datetime_items))

    _cash_manager = Factory.create('CashManager', db=db)

    _account1 = Factory.create('Account', db=db, name='a001', ccy='USD')
    _account2 = Factory.create('Account', db=db, name='a002', ccy='USD')
    _account3 = Factory.create('Account', db=db, name='a003', ccy='EUR')

    _trx1 = Factory.create('CashTrx', db=db, amount=1000.01, ccy='USD', description='test1', ts=datetime_items['dates'][0])
    _trx2 = Factory.create('CashTrx', db=db, amount=1000.01, ccy='USD', description='test2', ts=datetime_items['dates'][1])
    _trx3 = Factory.create('CashTrx', db=db, amount=1000.01, ccy='USD', description='test3', ts=datetime_items['dates'][2])
    _account1.cash_trxs().extend([_trx1, _trx2, _trx3])

    _trx11 = Factory.create('CashTrx', db=db, amount=1000.01, ccy='USD', description='test1', ts=datetime_items['dates'][0])
    _trx12 = Factory.create('CashTrx', db=db, amount=1000.01, ccy='USD', description='test2', ts=datetime_items['dates'][1])
    _trx13 = Factory.create('CashTrx', db=db, amount=1000.01, ccy='USD', description='test3', ts=datetime_items['dates'][2])
    _account2.cash_trxs().extend([_trx11, _trx12, _trx13])

    _trx21 = Factory.create('CashTrx', db=db, amount=1000.01, ccy='USD', description='test1', ts=datetime_items['dates'][0])
    _trx22 = Factory.create('CashTrx', db=db, amount=1000.01, ccy='USD', description='test2', ts=datetime_items['dates'][1])
    _trx23 = Factory.create('CashTrx', db=db, amount=1000.01, ccy='USD', description='test3', ts=datetime_items['dates'][2])
    _account3.cash_trxs().extend([_trx21, _trx22, _trx23])

    _cash_manager.add_account(_account1)
    _cash_manager.add_account(_account2)
    _cash_manager.add_account(_account3)
    for account in _cash_manager.accounts():
        print('Account[{0}]: {1}'.format(account.id(), account))

    balances = _cash_manager.get_balance()
    print('Balance')
    for k, v in _cash_manager.balance().items():
        print('Ccy [{0}]: {1:,.2f}'.format(k, v))

    _cash_manager.eod(datetime_items['today'] - datetime_items['date_delta'])

    print('Balance')
    for k, v in _cash_manager.balance().items():
        print('Ccy [{0}]: {1:,.2f}'.format(k, v))

    print('sync_points')
    for k, v in _cash_manager.sync_points().items():
        print('Cash Manager sync_points : [{0}]{1}'.format(k, v))

    _cash_manager.eod()

    print('Balance')
    for k, v in _cash_manager.balance().items():
        print('Ccy [{0}]: {1:,.2f}'.format(k, v))

    print('sync_points')
    for k, v in _cash_manager.sync_points().items():
        print('Cash Manager sync_points : [{0}]{1}'.format(k, v))

    _ptf.add_account(_account1)
    _ptf.add_account(_account2)
    _ptf.add_account(_account3)
    for account in _ptf.accounts():
        print('Account: {0}'.format(account))

    _ptf.eod()

    for k, v in _ptf.balance().items():
        print('Balance[{0}]: {1}'.format(k, v))

    _event = Factory.create('Event', db=db, event_type=EventType.Open)
    assert (isinstance(_event, Event))

    _book1 = Factory.create('Book', db=_ptf.db)

    _instrument1 = Factory.create('Instrument', db=db, name='Apple', instrument_type='equity', category='Nasdaq',
                                  symbol='AAP', description='Apple stock', venue='NYSE')
    print('Instrument: {0}'.format(_instrument1))

    _deal1 = Factory.create('DealEq', db=db, state=_event, instrument=_instrument1, price=2.24, qty=1000, ccy='USD')
    print('Deal: {0}'.format(_deal1))

    _instrument2 = Factory.create('InstrumentFx', db=db, symbol='EURUSD', ccy_pair='EURUSD', instrument_type='fx',
                                  category='spot', venue='NYSE')

    _deal2 = Factory.create('DealFx', db=db, state=_event, instrument=_instrument2, rate=1.27, qty=1000,
                            ccy1='EUR', ccy2='USD', ccy1_amount=1000, ccy2_amount=1000/1.27)

    _instrument3 = Factory.create('Instrument', db=db, name='Google', id='GOOGL', instrument_type='equity',
                                  category='Nasdaq', symbol='GOOGL', description='Google stock', venue='NYSE')
    print('Instrument: {0}'.format(_instrument3))

    _deal3 = Factory.create('DealEq', db=db, state=_event, instrument=_instrument3, price=1.27, qty=1000, ccy='USD')

    _instrument4 = Factory.create('InstrumentFx', db=db, symbol='EURUSD', ccy_pair='EURUSD', instrument_type='fx',
                                  category='spot', venue='NYSE')

    _deal4 = Factory.create('DealFx', db=db, state=_event, instrument=_instrument4, rate=1.27, qty=1000, ccy1='EUR',
                            ccy2='USD', ccy1_amount=1000, ccy2_amount=1000/1.27)

    _book1.add(_book1.deals(), _deal1, DealEq)
    _book1.add(_book1.deals(), _deal2, DealFx)
    _book1.add(_book1.deals(), _deal3, DealEq)
    _book1.add(_book1.deals(), _deal4, DealFx)

    print('book: {0}'.format(_book1))

    _ptf.add(_ptf.books(), _book1, Book)

    _positions = _ptf.positions()
    print('Positions')
    for k, v in _positions.items():
        print('{0}: {1}'.format(k, v))

def test_portfolio_sql():
    pass
