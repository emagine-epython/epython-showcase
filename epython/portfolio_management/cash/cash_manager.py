import kydb
from portfolio_management.common.account_container_mixin import AccountContainerMixin
from portfolio_management.common.position_mixin import PositionMixin
from portfolio_management.common.base_item import BaseItem, Factory
from portfolio_management.kydb_config import OBJDB_CONFIG
from portfolio_management.cash.account import Account
from portfolio_management.cash.cash_trx import CashTrx
import copy
import datetime


class CashManager(BaseItem, AccountContainerMixin, PositionMixin, kydb.DbObj):
    """
    Singleton object to manage a collection of accounts
    Implements an eod process to maintain a balance and apply interest accrual
    Can be used for group operations on its accounts
    """

    def eod(self, date=None):
        if not date:
            now = datetime.datetime.now()
            date =  datetime.datetime(now.year, now.month, now.day)
        for account in self.accounts():
            account.eod(date)
        self.balance.setvalue(self.get_balance())
        self.sync_points()['eod'] = date

    @kydb.stored
    def balance(self) -> dict:
        return {}

    def calc_balance(self, ts=None) -> dict:
        balances = {}
        for account in self.accounts():
            account.calc_balance(ts)
            balance = account.balance()
            if account.ccy() not in balances:
                balances[account.ccy()] = account.balance()
            else:
                balances[account.ccy()] += account.balance()
        self.balance.setvalue(balances)
        return self.balance()


def main():
    pass

if __name__ == '__main__':
    main()
