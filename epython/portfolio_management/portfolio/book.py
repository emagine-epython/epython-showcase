import kydb
from portfolio_management.common.base_item import BaseItem, Factory
import portfolio_management.utils.func_utils as fu
from portfolio_management.common.account_container_mixin import AccountContainerMixin
from portfolio_management.common.position_mixin import PositionMixin
import logging

LOGGER = logging.getLogger(__name__)


class Book(BaseItem, AccountContainerMixin, PositionMixin, kydb.DbObj):
    """
    A collection of deals
    Performs some group functions
    Carries a collection of accounts so it can manage its cash
    Accounts are managed by the cash manager for things that are only cash related: interest accrual, etc
    """

    @kydb.stored
    def deals(self):
        return []

    def positions(self) -> dict:
        positions = {}
        for account in self.accounts():
            if account.ccy() not in positions:
                positions[account.ccy()] = account.balance()
            else:
                positions[account.ccy()] += account.balance()

        for deal in self.deals():
            for k, v in deal.positions().items():
                if k not in positions:
                    positions[k] = v
                else:
                    positions[k] += v
        return positions

    def __str__(self):
        return '{0}'.format(self.id())

    def create_deal(self, deal_type, db, symbol, qty, price_or_rate, ccy, date, tenor=None, direction='B'):
        account_for_ccy = [x for x in self.accounts() if x.ccy() == ccy]
        if not account_for_ccy:
            raise Exception('Book {0} has no account for ccy: {1}, please add an account with enough funds for this '
                            'operation'.format(self.id, self.ccy()))
        if account_for_ccy[0].get_balance() < qty * price_or_rate:
            raise Exception('Book {0} has not enough cash in account {1} for ccy {2}, please add funds to your account'.
                            format(self.id(), account_for_ccy.id(), self.ccy()))
        if deal_type == 'DealEq':
            instrument = Factory.create('Instrument', db=db, symbol=symbol)
            deal = Factory.create(deal_type, db=db, instrument=instrument, qty=qty, price=price_or_rate, ccy=ccy, date=date,
                                  direction=direction)
        elif deal_type == 'DealFx':
            instrument = Factory.create('Instrument', db=db, ccy_pair=symbol, name=symbol)
            deal = Factory.create(deal_type, db=db, ccy_pair=symbol, qty=qty, rate=price_or_rate, ccy1=symbol[0:3],
                                  ccy2=symbol[3:], ccy1_amount=qty, ccy2_amount=qty/price_or_rate,
                                  date=date, direction=direction)
        else:
            raise Exception('Invalid deal type: {0}'.format(deal_type))
        return deal


def main():
    pass


if __name__ == '__main__':
    main()
