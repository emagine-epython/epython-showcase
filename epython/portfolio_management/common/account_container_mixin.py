import kydb
from portfolio_management.cash.account import Account
import datetime


class AccountContainerMixin:

    def add_account(self, account):
        assert isinstance(account, Account)
        if account not in self.accounts():
            self.accounts().append(account)
            return True
        return False

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
    def accounts(self) -> list:
        return []

    def get_balance(self) -> dict:
        balances = {}
        for account in self.accounts():
            balance = account.get_balance()
            if account.ccy() not in balances:
                balances[account.ccy()] = balance
            else:
                balances[account.ccy()] += balance
        return balances

