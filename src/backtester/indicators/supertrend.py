import numpy as np
import pandas as pd


class SuperTrend:
    __atr_period = None
    __factor = None
    __tr = None
    __atr = None
    __high = None
    __low = None
    __close = None
    __df = None

    def __init__(self, atr_period, factor):
        self.__atr_period = atr_period
        self.__factor = factor

    def __calculate_tr(self):
        price_diffs = [
            self.__high - self.__low,
            self.__high - self.__close.shift(),
            self.__close.shift() - self.__low
        ]
        true_range = pd.concat(price_diffs, axis=1)
        self.__tr = true_range.abs().max(axis=1)

    def set_dataframe(self, df):
        self.__df = df
        self.__high = df['High']
        self.__low = df['Low']
        self.__close = df['Close']
        return self

    def calculate(self):
        self.__calculate_tr()

        hl2 = (self.__high + self.__low) / 2
        atr = self.__tr.ewm(
            alpha=1 / self.__atr_period,
            min_periods=self.__atr_period
        ).mean()

        upperband = hl2 + (self.__factor * atr)
        lowerband = hl2 - (self.__factor * atr)

        # initialize Supertrend column to True
        supertrend = [True] * len(self.__df)

        for i in range(1, len(self.__df.index)):
            curr = i
            prev = i - 1

            if self.__close[curr] > upperband[prev]:
                supertrend[curr] = True
            elif self.__close[curr] < lowerband[prev]:
                supertrend[curr] = False
            else:
                supertrend[curr] = supertrend[prev]

                if supertrend[curr] is True and lowerband[curr] < lowerband[prev]:
                    lowerband[curr] = lowerband[prev]

                if supertrend[curr] is False and upperband[curr] > upperband[prev]:
                    upperband[curr] = upperband[prev]

            if supertrend[curr] is True:
                upperband[curr] = np.nan
            else:
                lowerband[curr] = np.nan

        return pd.DataFrame(data={
            'Supertrend': supertrend,
            'Lowerband': lowerband,
            'Upperband': upperband
        }, index=self.__df.index)
