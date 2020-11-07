import kydb
import datetime


class PositionMixin(kydb.DbObj):

    @kydb.stored
    def sync_points(self):
        return {}

    def add(self, items, item, item_type):
        assert(isinstance(item, item_type))
        if item not in items:
            if isinstance(item, str):
                items.add(item)
            else:
                items.add(item.id())
            return True
        return False

    def delete(self, items, item_id):
        item = [x for x in items if x.id() == item_id]
        if item:
            items.remove(item[0])
            return True
        return False

    def get(self, items, item_id):
        item = [x for x in items if x.id() == item_id]
        if item:
            return item[0]
        return None

    def eod(self, date=None):
        pass

    def child_eod(self, eod_items, date=None) -> dict:
        if not date:
            date = datetime.datetime.today()
        tmp_eod_items = {}
        for k, v in self.eodItems.items():
            tmp_eod_items[k].append(v.eod_process(date))
        return tmp_eod_items

    @kydb.stored
    def balance(self) -> dict:
        return {}

    def positions(self) -> dict:
        return {}

    def child_positions(self, position_items) -> dict:
        tmp_eod_items = {}
        for item in position_items:
            if item.id() not in tmp_eod_items:
                tmp_eod_items[item.id()] = item.positions()
            else:
                tmp_eod_items[item.id()].update(item.positions())
        return tmp_eod_items
