import kydb
import datetime
import uuid

ROOT_PATH = 'portfolio_management'


class BaseItem(kydb.DbObj):

    def path(self):
        return '{0}/{1}/{2}'.format(ROOT_PATH,
                                    type(self).__name__.split('.')[-1] if '.' in type(self).__name__ else type(self).__name__,
                                    self.id())

    @kydb.stored
    def id(self) -> str:
        return ''

    @kydb.stored
    def name(self) -> str:
        return ''

    @kydb.stored
    def updated(self) -> datetime.datetime:
        return datetime.datetime.now()

    @staticmethod
    def generate_id():
        return str(uuid.uuid4())


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
        print('new_object.path(): {0}'.format(new_object.path()))
        kwargs['db'][new_object.path()] = new_object
        return new_object
