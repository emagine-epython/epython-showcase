import kydb
from portfolio_management.cash.account import Account
import datetime
from portfolio_management.common.base_item import Factory


class AccountContainerMixin:

    def add_account(self, account_id):
        self.accounts().add(account_id)

    def delete_account(self, account_id):
        item = [x for x in self.accounts() if x.id() == account_id]
        if item:
            self.accounts().remove(item[0])
            return True
        return False

    def get_account(self, account_id):
        item = [x for x in self.accounts() if x.id() == account_id]
        if item:
            return item[0]
        return None

    @kydb.stored
    def accounts(self) -> set:
        return set()

    def accounts_obj(self) -> list:
        return [self.db[Factory.get_class_path('Account', a)] for a in self.accounts()]

    def get_balance(self) -> dict:
        balances = {}
        for account in self.accounts_obj():
            balance = account.get_balance()
            if account.ccy() not in balances:
                balances[account.ccy()] = balance
            else:
                balances[account.ccy()] += balance
        return balances

