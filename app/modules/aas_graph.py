import numpy as np
from streamz.dataframe import PeriodicDataFrame
import pandas as pd
import hvplot.pandas
import hvplot.streamz
import time
import asyncio
import holoviews as hv
from holoviews.element.tiles import EsriImagery
from holoviews.selection import link_selections
import matplotlib.pyplot as plt
import panel as pn


class AASGraph:
    def __init__(self, update_cb=None) -> None:
        self.data = pd.DataFrame({'time': pd.Series(dtype='int'),
                                  'value': pd.Series(dtype='float'),
                                  'rate': pd.Series(dtype='float')
                                  })
        self.capacity = 1000
        self.window_size = 100
        self.update_cb = update_cb

    def add_rate_point(self, time, value):
        self.data = self.data[-self.window_size:]
        if len(self.data) > self.window_size-1 and self.data.value.iloc[-1] < 0:
            print("ZERO:", self.data.time.iloc[-1])
            return
        prev_value = self.capacity if self.data.empty else self.data.value.iloc[-1]
        self.data = pd.concat([self.data, pd.DataFrame([[time, prev_value - value, value]], columns=["time", "value", "rate"])])
        self.estimate_zero()
        

    def get_data(self):
        return (self.data.time.to_list(), self.data.value.to_list(), self.data.rate.to_list())

    def get_bounds(self):
        dt = self.get_data()
        times = sorted(list(dt[0]))
        values = sorted(list(dt[1]))
        return ((times[0], times[-1]), (values[0], values[-1]))

    def estimate_zero(self):
        if len(self.data) > self.window_size:
            dp = self.data.iloc[-1]
            mean_der = -self.data.rate.mean()
            zero = (mean_der*dp.time - dp.value)/mean_der
            print("est Zero:", zero)