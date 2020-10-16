import kydb
import pandas as pd
from datetime import datetime


class TimeSeries(kydb.DbObj):
    def curve(self, start_date: datetime, end_date: datetime) -> pd.DataFrame:
        """Get timeseries data between `start_date` and `end_date`

        :param start_date: The start date
        :param end_data: The end date

Example:

::

        ts = db['/symbols/fxcm/minutely/USDJPY']
        ts.curve(datetime(2017, 5, 1), datetime(2017, 5, 3)).head()

"""
        raise NotImplementedError()
