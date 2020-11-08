import kydb
import datetime
from test_db import db
from portfolio_management.cash.cash_trx import CashTrx
from portfolio_management.common.base_item import Factory


def test_balance_create(db):
    db = kydb.connect('dynamodb://epython/jose')
    _trx1 = Factory.create('CashTrx', db=db, amount=1000.01, ccy='USD', updated=datetime.datetime.now(),
                           description='test')
    print('CashTrx: {0}'.format(_trx1))
    # _trx2 = Factory.create('CashTrx', db=db, amount=2000.02, ccy='GBP', updated=datetime.datetime.now(),
    #                       description='test')
    print('CashTrx: {0}'.format(_trx1))
    # print('CashTrx: {0}'.format(_trx2))
    assert(isinstance(_trx1, CashTrx))
    # assert(isinstance(_trx2, CashTrx))
    key = _trx1.path()
    print('key: {0}'.format(key))
    _trxRead = db[key]
    assert (isinstance(_trxRead, CashTrx))
    assert (_trxRead.id(), _trx1.id())
    print('check read trx')

