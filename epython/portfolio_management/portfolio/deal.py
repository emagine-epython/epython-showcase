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
    def state(self) -> str:
        return ''

    def state_obj(self) -> Event:
        return self.db[Factory.get_class_path('Event', self.state())]

    def positions(self) -> dict:
        return {}

    def __str__(self):
        return '{0}[{1}]'.format(self.id(), self.state())

    def apply_event(self, event_type, price=None, qty=None, ccy=None):
        if event_type == EventType.Amend:
            if price:
                self.price.setvalue(price)
            if qty:
                self.price.setvalue(qty)
            if ccy:
                self.ccy.setvalue(ccy)

        self.events().add(self.state())
        event = Factory.create('Event', db=self.db, event_type=event_type)
        self.state.setvalue(event.id())

    @kydb.stored
    def instrument(self) -> str:
        return ''

    def instrument_obj(self) -> Instrument:
        return self.db[Factory.get_class_path('Instrument', self.instrument())]

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
    def events(self) -> set:
        return set()

    @kydb.stored
    def events_obj(self) -> list:
        return [self.db[Factory.get_class_path('Event', a)] for a in self.events()]

    @kydb.stored
    def instrument(self) -> str:
        return ''


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
            self.instrument_obj().symbol(): self.qty()
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

    def instrument_obj(self) -> InstrumentFx:
        return self.db[Factory.get_class_path('InstrumentFx', self.instrument())]


def main():
    pass


if __name__ == '__main__':
    main()
