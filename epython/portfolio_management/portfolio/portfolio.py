import kydb

from portfolio.book import Book
from portfolio_management.common.position_mixin import PositionMixin
from portfolio_management.common.account_container_mixin import AccountContainerMixin
from portfolio_management.common.base_item import BaseItem, Factory


class Portfolio(BaseItem, AccountContainerMixin, PositionMixin, kydb.DbObj):
    """
    A portfolio is a collection of books
    Serves to manage a group of investments
    It can query its books to provide a summary of its position
    It also takes a collection of accounts to manage its cash positions
    Accounts can be on different currencies
    Portfolios can be used to segregate groups of investments that can be setup
    with different investment profiles
    - Aggressive
    - Conservative
    - Balanced
    A portfolio gets allocated a budget by funding associated accounts
    These accounts are shared by member books
    Transactions have to respect the funding allocations
    Accounts can accrue interest (managed by cash manager)
    """

    @kydb.stored
    def books(self) -> set:
        return set()

    def books_obj(self) -> list:
        return [self.db[b] for b in self.books()]

    def positions(self) -> dict:
        positions = self.get_balance()
        positions.update(self.child_positions(self.books_obj()))
        return positions


def main():
    pass


if __name__ == '__main__':
    main()
