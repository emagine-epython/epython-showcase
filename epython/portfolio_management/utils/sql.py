import kydb
from datetime import date, datetime
from typing import Union


class SQLMixin:
    @kydb.stored
    def sql_template_path(self) -> str:
        return ''

    def sql_template(self) -> str:
        return self.db[self.sql_template_path()]

    @kydb.stored
    def sql_kwargs(self) -> dict:
        return {}

    @staticmethod
    def _ensure_datetime(dt: Union[date, datetime]) -> datetime:
        if isinstance(dt, date):
            return datetime.combine(dt, datetime.min.time())

        return dt

    def sql(self,
            start_dt: Union[date, datetime],
            end_dt: Union[date, datetime]):
        start_dt = self._ensure_datetime(start_dt)
        end_dt = self._ensure_datetime(end_dt)

        if isinstance(end_dt, date):
            end_dt = datetime.combine(end_dt, datetime.min.time())

        kwargs = {
            'start_dt': start_dt,
            'end_dt': end_dt
        }

        for k, v in self.sql_kwargs().items():
            kwargs[k] = v

        return self.sql_template().format(**kwargs)
