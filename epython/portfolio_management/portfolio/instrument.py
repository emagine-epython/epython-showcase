import kydb
from portfolio_management.common.base_item import BaseItem, Factory


class InstrumentBase(BaseItem, kydb.DbObj):
    """
    Represents a financial instrument
    There are different types
    The idea is to provide a symbol
    and the system will pick the fill instrument definition from a data source
    Still needs instrument type enumeration
    """

    @kydb.stored
    def instrument_type(self) -> str:
        return ''

    @kydb.stored
    def category(self) -> str:
        return ''

    @kydb.stored
    def description(self) -> str:
        return ''

    @kydb.stored
    def venue(self) -> str:
        return ''

    def __str__(self):
        return '{0}[{1}]: {2}'.format(self.id(), self.instrument_type(), self.category())


class Instrument(InstrumentBase):
    """
    Equity instrument
    """

    @kydb.stored
    def name(self) -> str:
        return ''

    @kydb.stored
    def symbol(self) -> str:
        return ''

    def __str__(self):
        return '{0} {1}-{2}'.format(super().__str__(), self.name(), self.symbol())


class InstrumentFx(InstrumentBase):
    """
    Fx Spot Instrument
    """

    @kydb.stored
    def ccy_pair(self) -> str:
        return ''

    def __str__(self):
        return '{0} {1}'.format(super().__str__(), self.ccy_pair())


def main():
    pass


if __name__ == '__main__':
    main()
