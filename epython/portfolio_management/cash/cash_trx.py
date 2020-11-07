import kydb
from portfolio_management.common.base_item import BaseItem
import datetime


class CashTrx(BaseItem, kydb.DbObj):
    """
    Represents a cash transaction
    it is immutable
    """

    @kydb.stored
    def ts(self, ts=None):
        if not ts:
            ts = datetime.datetime.now()
        return ts

    @kydb.stored
    def amount(self):
        return 0.00

    @kydb.stored
    def ccy(self):
        return None

    @kydb.stored
    def description(self):
        return None

    def __str__(self):
        return '{0} {1} [{2}]: {3}'.format(self.amount(), self.ccy(), self.ts(), self.description())


def main():
    pass


if __name__ == '__main__':
    main()
