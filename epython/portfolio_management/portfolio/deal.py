import kydb
from portfolio_management.common.base_item import BaseItem, Factory
from portfolio_management.common.account_container_mixin import AccountContainerMixin
from portfolio_management.common.position_mixin import PositionMixin
from portfolio_management.portfolio.event import Event, EventType
from portfolio_management.portfolio.instrument import Instrument, InstrumentFx
import portfolio_management.utils.func_utils as fu


class Deal(BaseItem, AccountContainerMixin, PositionMixin, kydb.DbObj):
    """
    Represents a buy / sell transaction for a financial instrument
    """

    @kydb.stored
    def state(self):
        return None

    def positions(self) -> dict:
        return {}

    def __str__(self):
        return '{0}[{1}] {2}'.format(self.id(), self.state(), self.positions())

    def apply_event(self, event_type, price=None, qty=None, ccy=None):
        if event_type == EventType.Amend:
            if price:
                self.price.setvalue(price)
            if qty:
                self.price.setvalue(qty)
            if ccy:
                self.ccy.setvalue(ccy)

        self.events().append(self.state())
        self.state.setvalue(Factory.create('Event', db=self.db, event_type=event_type))

    @kydb.stored
    def instrument(self) -> Instrument:
        return None

    @kydb.stored
    def direction(self) -> str:
        return 'B'

    @kydb.stored
    def ccy(self) -> str:
        return ''

    @kydb.stored
    def qty(self) -> float:
        return 0.00

    @kydb.stored
    def events(self) -> list:
        return []


class DealEq(Deal):
    """
    Equity type deal
    """

    @kydb.stored
    def price(self) -> float:
        return 0.00

    def positions(self) -> dict:
        positions = {
            self.ccy() : - self.qty() * self.price(),
            self.instrument().symbol(): self.qty()
        }
        return positions

    @kydb.stored
    def notional(self) -> float:
        return self.qty() if self.qty() else 0.00 * self.price() if self.price() else 0.00


class DealFx(Deal):
    """
    FX Spot type deal
    """

    @kydb.stored
    def rate(self) -> float:
        return 0.00

    @kydb.stored
    def ccy1(self) -> str:
        return ''

    @kydb.stored
    def ccy2(self) -> str:
        return ''

    @kydb.stored
    def ccy1_amount(self) -> float:
        return 0.00

    @kydb.stored
    def ccy2_amount(self) -> float:
        return 0.00

    def positions(self) -> dict:
        factor = 1 if self.direction() == 'B' else -1
        positions = {self.ccy1(): self.ccy1_amount() * factor, self.ccy2(): self.ccy2_amount() * factor * -1}
        return positions

    @kydb.stored
    def instrument(self) -> InstrumentFx:
        return None


def main():
    pass


if __name__ == '__main__':
    main()
