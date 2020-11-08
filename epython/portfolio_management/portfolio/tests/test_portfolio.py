from portfolio_management.common.base_item import Factory
from portfolio_management.portfolio.event import Event, EventType
from portfolio_management.portfolio.book import Book
from portfolio_management.portfolio.instrument import Instrument, InstrumentFx
from portfolio_management.portfolio.deal import DealEq, DealFx
import datetime
from test_db import db
from portfolio_management.utils.test_datetime import datetime_items
import kydb
from portfolio_management.kydb_config import OBJDB_CONFIG
import pickle
import json
import portfolio_management.utils.json_serialiser as js


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
    _account1.add_cash_trx(_trx1.id())
    _account1.add_cash_trx(_trx2.id())
    _account1.add_cash_trx(_trx3.id())

    _trx11 = Factory.create('CashTrx', db=db, amount=1000.01, ccy='USD', description='test1', ts=datetime_items['dates'][0])
    _trx12 = Factory.create('CashTrx', db=db, amount=1000.01, ccy='USD', description='test2', ts=datetime_items['dates'][1])
    _trx13 = Factory.create('CashTrx', db=db, amount=1000.01, ccy='USD', description='test3', ts=datetime_items['dates'][2])
    _account2.add_cash_trx(_trx11.id())
    _account2.add_cash_trx(_trx12.id())
    _account2.add_cash_trx(_trx13.id())

    _trx21 = Factory.create('CashTrx', db=db, amount=1000.01, ccy='USD', description='test1', ts=datetime_items['dates'][0])
    _trx22 = Factory.create('CashTrx', db=db, amount=1000.01, ccy='USD', description='test2', ts=datetime_items['dates'][1])
    _trx23 = Factory.create('CashTrx', db=db, amount=1000.01, ccy='USD', description='test3', ts=datetime_items['dates'][2])
    _account3.add_cash_trx(_trx21.id())
    _account3.add_cash_trx(_trx22.id())
    _account3.add_cash_trx(_trx23.id())

    _cash_manager.add_account(_account1.id())
    _cash_manager.add_account(_account2.id())
    _cash_manager.add_account(_account3.id())
    for account in _cash_manager.accounts_obj():
        print('Account[{0}]: {1}'.format(account, db[account.path()]))

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

    _ptf.add_account(_account1.id())
    _ptf.add_account(_account2.id())
    _ptf.add_account(_account3.id())
    for account in _ptf.accounts_obj():
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

    _deal1 = Factory.create('DealEq', db=db, state=_event.id(), instrument=_instrument1.id(), price=2.24, qty=1000, ccy='USD')
    print('Deal: {0}'.format(_deal1))

    _instrument2 = Factory.create('InstrumentFx', db=db, symbol='EURUSD', ccy_pair='EURUSD', instrument_type='fx',
                                  category='spot', venue='NYSE')
    print('Instrument2: {0}'.format(_instrument2))

    _deal2 = Factory.create('DealFx', db=db, state=_event.id(), instrument=_instrument2.id(), rate=1.27, qty=1000,
                            ccy1='EUR', ccy2='USD', ccy1_amount=1000, ccy2_amount=1000/1.27)
    print('Deal2: {0}'.format(_deal2))

    _instrument3 = Factory.create('Instrument', db=db, name='Google', instrument_type='equity',
                                  category='Nasdaq', symbol='GOOGL', description='Google stock', venue='NYSE')
    print('Instrument3: {0}'.format(_instrument3))

    _deal3 = Factory.create('DealEq', db=db, state=_event.id(), instrument=_instrument3.id(), price=1.27, qty=1000, ccy='USD')
    print('Deal3: {0}'.format(_deal3))

    _instrument4 = Factory.create('InstrumentFx', db=db, symbol='EURUSD', ccy_pair='EURUSD', instrument_type='fx',
                                  category='spot', venue='NYSE')
    print('Instrument4: {0}'.format(_instrument4))

    _deal4 = Factory.create('DealFx', db=db, state=_event.id(), instrument=_instrument4.id(), rate=1.27, qty=1000, ccy1='EUR',
                            ccy2='USD', ccy1_amount=1000, ccy2_amount=1000/1.27)
    print('Deal4: {0}'.format(_deal4))

    # assert deals
    _test_deal1 = db[_deal1.path()]
    assert (isinstance(_test_deal1, DealEq))
    assert (_test_deal1 == _deal1)
    assert (_test_deal1.instrument() == _deal1.instrument())
    assert (_test_deal1.instrument_obj() == _deal1.instrument_obj())
    assert (isinstance(_test_deal1.instrument_obj(), Instrument))
    _test_instrument1 = db[_test_deal1.instrument_obj().path()]
    assert (isinstance(_test_instrument1, Instrument))

    _test_deal2 = db[_deal2.path()]
    assert (isinstance(_test_deal2, DealFx))
    assert (_test_deal2 == _deal2)
    assert (_test_deal2.instrument() == _deal2.instrument())
    assert (_test_deal2.instrument_obj() == _deal2.instrument_obj())
    assert (isinstance(_test_deal2.instrument_obj(), InstrumentFx))
    _test_instrument2 = db[_test_deal2.instrument_obj().path()]
    assert (isinstance(_test_instrument2, InstrumentFx))

    _book1.add(_book1.deals(), _deal1.id(), str)
    _book1.add(_book1.deals(), _deal2.id(), str)
    _book1.add(_book1.deals(), _deal3.id(), str)
    _book1.add(_book1.deals(), _deal4.id(), str)

    print('book: {0}'.format(_book1))

    _ptf.add(_ptf.books(), _book1.id(), str)

    _positions = _ptf.positions()
    print('Positions')
    for k, v in _positions.items():
        print('{0}: {1}'.format(k, v))

    return _ptf


def test_portfolio_sql(datetime_items):
    db = kydb.connect('dynamodb://epython/jose')
    #kdb.upload_objdb_config(OBJDB_CONFIG)
    _ptf = test_portfolio(db, datetime_items)
    _ptf.name.setvalue('TestPortfolio')
    key = 'portfolio_management/portfolio/{0}'.format(_ptf.name())
    db[key] = _ptf
    _ptf2 = db[key]
    print(_ptf2)
