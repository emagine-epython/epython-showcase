import kydb
from enum import Enum
import datetime


class EventType(Enum):
    """
    Represent stages in deal life cycle
    """
    New = 0
    Open = 1
    Amend = 2
    Cancel = 3
    Close = 4
    Expire = 5
    Exercise = 6


class Event(kydb.DbObj):
    """
    Marks stages in deal life cycle
    Applying an event changes deal state
    All deals start with an Open EVent
    Depending upon deal type, some or all events may apply
    """

    @kydb.stored
    def id(self) -> str:
        return ''

    @kydb.stored
    def event_type(self) -> EventType:
        return EventType.New

    @kydb.stored
    def ts(self) -> datetime.datetime:
        return datetime.datetime.now()

    def __str__(self):
        return '{0}[{1}]:{2}'.format(self.id(), self.event_type(), self.ts())


def main():
    pass

if __name__ == '__main__':
    main()
