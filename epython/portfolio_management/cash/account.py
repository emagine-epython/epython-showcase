import kydb
import datetime
from cash.cash_trx import CashTrx
from common.position_mixin import PositionMixin
from portfolio_management.kydb_config import OBJDB_CONFIG
from portfolio_management.cash.interest_rate import InterestRate
from portfolio_management.utils.sql import SQLMixin
from portfolio_management.common.base_item import BaseItem, Factory, ROOT_PATH
import logging
import json

LOGGER = logging.getLogger(__name__)


class Account(BaseItem, PositionMixin, SQLMixin, kydb.DbObj):
    """
    An Account is a collection of cash transactions for the same person / entity
    A account will be able to calculate its balance (equivalent to positions)
    An eod process will calculate:
     - accrual interest
     - updated balance
    """

    @kydb.stored
    def ccy(self):
        return None

    def __str__(self):
        return '{0}[{1}]'.format(self.id(), self.ccy())

    def add_cash_trx(self, cash_trx_id):
        self.cash_trxs().add(cash_trx_id)

    @kydb.stored
    def cash_trxs(self) -> set():
        return set()

    def cash_trxs_obj(self) -> list:
        path = BaseItem
        return [self.db[Factory.get_class_path('CashTrx', t)] for t in self.cash_trxs()]

    def get_balance(self) -> float:
        '''
        Updates balance and returns value up to latest transaction
        :return:
        '''
        sync_point = self.sync_points().get('eod', datetime.datetime(2000, 1, 1))
        now = datetime.datetime.now()
        return self.balance() + sum([x.amount() for x in self.cash_trxs_obj() if sync_point < x.ts() <= now])

    @kydb.stored
    def balance(self) -> float:
        return 0.00

    def eod(self, dt=None):
        if not dt:
            today = datetime.datetime.today()
            dt = datetime.datetime(today.year, today.month, today.day, 23, 59, 59)
        if 'eod' not in self.sync_points():
            self.sync_points()['eod'] = datetime.datetime(2000, 1, 1)
        LOGGER.info('Account: {0} processing eod as of: {1}'.format(self.id(), dt))
        print('processing eod as of: {0}'.format(dt))
        # rate = InterestRate.query(dt, self.ccy())
        interest_rate = 0.31 / 100
        day_count = InterestRate.day_count()
        accrual = round(self.get_balance() * (interest_rate / day_count), 2)
        self.deposit(amount=accrual, date=dt - datetime.timedelta(seconds=1), description='interest accrual')
        self.balance.setvalue(self.get_balance())
        self.sync_points()['eod'] = dt

    def deposit(self, amount, date, description):
        trx = Factory.create('CashTrx', db=self.db, amount=amount, ccy=self.ccy(), ts=date, description=description)
        self.db[trx.path()] = trx
        self.add_cash_trx(trx.id())

    def withdrawal(self, amount, date, description):
        trx = Factory.create('CashTrx', db=self.db, amount=-amount, ccy=self.ccy(), ts=date, description=description)
        self.db[trx.path()] = trx
        self.add_cash_trx(trx.id())


def main():
    pass


if __name__ == '__main__':
    main()
