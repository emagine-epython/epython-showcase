from portfolio_management.common.base_item import Factory
from test_db import db
import datetime


def test_cash_manager(db):
    _cash_manager = Factory.create('CashManager', db=db)
    _account1 = Factory.create('Account', db=db, name='a001', ccy='USD')
    _account2 = Factory.create('Account', db=db, name='a002', ccy='USD')
    _account3 = Factory.create('Account', db=db, name='a003', ccy='EUR')
    print('account1: {0}'.format(_account1))
    print('account2: {0}'.format(_account2))
    print('account3: {0}'.format(_account3))

    now = datetime.datetime.now()
    time_delta = datetime.timedelta(minutes=10)
    date_delta = datetime.timedelta(days=1)
    today = datetime.datetime(now.year, now.month, now.day)
    dates = [now - datetime.timedelta(days=4),
             now - datetime.timedelta(days=3, hours=5),
             now - datetime.timedelta(days=2, hours=1)]

    _trx1 = Factory.create('CashTrx', db=db, amount=1000.01, ccy='USD', description='test1', ts=dates[0])
    _trx2 = Factory.create('CashTrx', db=db, amount=1000.01, ccy='USD', description='test2', ts=dates[1])
    _trx3 = Factory.create('CashTrx', db=db, amount=1000.01, ccy='USD', description='test3', ts=dates[2])

    _account1.add_cash_trx(_trx1.id())
    _account1.add_cash_trx(_trx2.id())
    _account1.add_cash_trx(_trx3.id())

    _trx11 = Factory.create('CashTrx', db=db, amount=1000.01, ccy='USD', description='test1', ts=dates[0])
    _trx12 = Factory.create('CashTrx', db=db, amount=1000.01, ccy='USD', description='test2', ts=dates[1])
    _trx13 = Factory.create('CashTrx', db=db, amount=1000.01, ccy='USD', description='test3', ts=dates[2])

    _account2.add_cash_trx(_trx11.id())
    _account2.add_cash_trx(_trx12.id())
    _account2.add_cash_trx(_trx13.id())

    _trx21 = Factory.create('CashTrx', db=db, amount=1000.01, ccy='USD', description='test1', ts=dates[0])
    _trx22 = Factory.create('CashTrx', db=db, amount=1000.01, ccy='USD', description='test2', ts=dates[1])
    _trx23 = Factory.create('CashTrx', db=db, amount=1000.01, ccy='USD', description='test3', ts=dates[2])

    _account3.add_cash_trx(_trx21.id())
    _account3.add_cash_trx(_trx22.id())
    _account3.add_cash_trx(_trx23.id())

    _cash_manager.add_account(_account1.id())
    _cash_manager.add_account(_account2.id())
    _cash_manager.add_account(_account3.id())

    for account in _cash_manager.accounts_obj():
        print('Account[{0}]: {1}'.format(account.id(), account))

    balances = _cash_manager.get_balance()
    print('Balance')
    for k, v in balances.items():
        print('Ccy [{0}]: {1:,.2f}'.format(k, v))

    _cash_manager.eod(today-date_delta)

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
        print('Cash Manager sync_points : [{0}] {1}'.format(k, v))
