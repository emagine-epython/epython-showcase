import math
import os
import pathlib
import random
import shutil
import tempfile

import feather
import numpy as np
import pandas as pd
from logging import getLogger
from tensorflow.keras.utils import Sequence

logger = getLogger(__name__)


class TrainSequence(Sequence):
    lookback_period = 60 * 24

    def __init__(self, train_data=None, enable_shuffle=True, batch_size=32, cache_batch=False):
        self.batch_size = batch_size
        self.train_data = train_data
        self.enable_shuffle = enable_shuffle
        self.cache_batch = cache_batch
        if cache_batch:
            self.cache_dir = self._get_cache_dir()
            logger.info(
                'All generated batches will be cached at %s', self.cache_dir)
        else:
            self.cache_dir = None

        l = train_data.shape[0] - self.lookback_period
        self.indices = np.linspace(0, l - 1, l).astype(int)
        if enable_shuffle:
            self.__shuffle_data()

    def __len__(self):
        return math.floor((self.train_data.shape[0] - self.lookback_period) / self.batch_size)

    def __getitem__(self, idx):
        if self.cache_dir:
            path = os.path.join(self.cache_dir, str(idx))
            xs_path = path + '_xs.feather'
            ys_path = path + '_ys.feather'
            if os.path.exists(xs_path):
                xs = feather.read_dataframe(xs_path).values
                ys = feather.read_dataframe(ys_path)['0'].to_numpy()
                return xs, ys

        xs = []
        ys = []
        for i in range(self.batch_size):
            t1 = self.indices[idx * self.batch_size + i]
            t2 = t1 + self.lookback_period
            x, y = self._normalise_data(self.train_data[t1:t2])
            y = 0 if y < 0.001 else 1
            xs.append(np.array([x for x in x.tolist()]))
            ys.append(y)

        if self.cache_dir:
            feather.write_dataframe(pd.DataFrame(xs), xs_path)
            feather.write_dataframe(pd.DataFrame(ys), ys_path)

        return np.array(xs), np.array(ys)

    @staticmethod
    def _get_cache_dir():
        res = '{}/angotsuka/train_seq_cache/{:032x}'.format(
            tempfile.gettempdir(),
            random.getrandbits(128))

        pathlib.Path(res).mkdir(parents=True, exist_ok=True)
        return res

    def remove_cache(self):
        if self.cache_dir:
            logger.info('Deleting cache: %s', self.cache_dir)
            shutil.rmtree(self.cache_dir)

    @classmethod
    def _normalise_data(cls, df):
        x = cls.normalise_mid(df)
        y = df.iloc[-1].position
        return x, y

    @staticmethod
    def normalise_mid(df):
        mid_max = df.mid.max()
        mid_min = df.mid.min()
        return (df.mid - mid_min) / (mid_max - mid_min)

    def on_epoch_end(self):
        self.__shuffle_data()

    def __shuffle_data(self):
        if self.enable_shuffle:
            np.random.shuffle(self.indices)
