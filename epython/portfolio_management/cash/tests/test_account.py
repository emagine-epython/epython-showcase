from portfolio_management.cash.account import Account
from portfolio_management.common.base_item import Factory
from test_db import db
import datetime


def test_account_new(db):
    name = 'Test'
    _account = Factory.create('Account', db=db, name=name, ccy='EUR')
    assert isinstance(_account, Account)
    assert _account.name() == name
    print('Account: {0}'.format(_account))


def test_account_trxs(db):

    _account = Factory.create('Account', db=db, ccy='USD')
    print('Account: {0}'.format(_account))

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

    _account.add_cash_trx(_trx1.id())
    _account.add_cash_trx(_trx2.id())
    _account.add_cash_trx(_trx3.id())

    for t in _account.cash_trxs():
        print(t)
    # balance
    bce = _account.get_balance()
    print('bce1: {0:,.2f} {1}'.format(bce, _account.ccy()))
    print('sync_points: {0}'.format(_account.sync_points()))
    balance_before_eod = _account.get_balance()
    print('balance_before_eod: {0:,.2f}'.format(balance_before_eod))

    for t in _account.cash_trxs():
        print(t)

    _account.eod(dt=today-date_delta)
    print('balance_after_eod: {0:,.2f} {1} @ {2}'.format(_account.balance(), _account.ccy(),
                                                         _account.sync_points().get('eod')))
    for t in _account.cash_trxs():
        print(t)

    bce = _account.get_balance()
    print('bce_after_eod: {0:,.2f}'.format(bce))
    print(_account.sync_points())

    _account.deposit(100, today - date_delta + time_delta + time_delta, 'deposit 1')
    _account.withdrawal(10, today - date_delta + time_delta + time_delta + time_delta, 'withdrawal 1')

    bce = _account.get_balance()
    print('bce_after more trx: {0:,.2f}'.format(bce))
    print(_account.sync_points())

    _account.eod(dt=today-time_delta)
    print('balance_after_eod: {0:,.2f} {1} @ {2}'.format(_account.balance(), _account.ccy(),
                                                         _account.sync_points().get('eod')))
    for t in _account.cash_trxs():
        print(t)

    bce = _account.get_balance()
    print('bce_after more trx and eod: {0:,.2f}'.format(bce))
    print(_account.sync_points())
