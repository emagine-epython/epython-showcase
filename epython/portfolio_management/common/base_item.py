import kydb
import datetime
import uuid


class BaseItem(kydb.DbObj):

    @kydb.stored
    def id(self) -> str:
        return ''

    @kydb.stored
    def name(self) -> str:
        return ''

    @kydb.stored
    def updated(self) -> datetime.datetime:
        return datetime.datetime.min

    @staticmethod
    def generate_id():
        return uuid.uuid4()


class Factory(kydb.DbObj):
    @staticmethod
    def create(type_name, **kwargs):
        new_id = BaseItem.generate_id()
        new_object = kwargs['db'].new(type_name, new_id, id=new_id)
        for k, v in kwargs.items():
            if k == 'db':
                continue
            if hasattr(new_object, k):
                attr = getattr(new_object, k)
                attr.setvalue(v)
        return new_object
