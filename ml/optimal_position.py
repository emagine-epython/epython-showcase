import kydb
from datetime import date
import pandas as pd
import numpy as np
from tsdb.base import TimeSeries


class OptimalPositionGenerator:
    start_date: date
    end_date: date
    tsdb: TimeSeries

    def __init__(self, tsdb: TimeSeries, start_date: date,
                 end_date: date):
        self.tsdb = tsdb
        self.start_date = start_date
        self.end_date = end_date

    def get_market_data(self) -> pd.DataFrame:
        return self.tsdb.curve(self.start_date, self.end_date)

    @staticmethod
    def add_future_lines(df: pd.DataFrame) -> pd.DataFrame:
        df = df.copy()
        forward_looking = 60 * 5
        rolling_window = forward_looking - 2
        for x in ('min', 'max'):
            roll = df.mid.rolling(rolling_window)
            df['future_' + x] = getattr(roll, x)().shift(-forward_looking)

        return df[~df.future_max.isna()]

    @staticmethod
    def get_optimal_positions(df: pd.DataFrame) -> pd.DataFrame:
        df = df.copy()
        df['position'] = np.NAN
        df.loc[df.bid > df.future_max, 'position'] = -1.
        df.loc[df.ask < df.future_min, 'position'] = 1.
        df = df.fillna(method='ffill').fillna(0.)
        return df

    def generate(self):
        df: pd.DataFrame = self.get_market_data()
        df = self.add_future_lines(df)
        return self.get_optimal_positions(df)
