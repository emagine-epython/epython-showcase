import kydb
import pandas as pd
from datetime import datetime


class TimeSeries(kydb.DbObj):
    def curve(self, start_date: datetime, end_date: datetime) -> pd.DataFrame:
        raise NotImplementedError()
