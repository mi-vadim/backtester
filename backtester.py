import math
import pandas

from indicators.supertrend import SuperTrend
from trading import Trade


class Backtester:
    __data_frame = None
    __enable_log = None
    __trading = None
    __entries = []
    __exits = []
    __roi_list = []

    def __init__(self, data_frame, enable_log=True):
        self.__data_frame = data_frame
        self.__enable_log = enable_log
        self.__trading = Trade()

    def __add_entry_order(self, time, price):
        self.__entries.append({
            "time": time,
            "price": price,
            "balance": self.__trading.balance,
            "side": self.__trading.side
        })

    def __add_exit_order(self, time, price):
        self.__exits.append({
            "time": time,
            "price": price,
            "balance": self.__trading.balance,
            "side": self.__trading.side
        })

    def super_trend(self, period, multiplier, investment, use_tp=False):
        print(f'\n ============')
        print(f'SuperTrend Params (ATR Period = {period}, Factor = {multiplier})')

        self.__trading.reset(balance=investment, use_tp=use_tp)
        supertrend = SuperTrend(atr_period=period, factor=multiplier)
        new_df = self.__data_frame
        data_frame = new_df.join(supertrend.set_dataframe(df=new_df).calculate())

        is_uptrend = data_frame['Supertrend']
        close = data_frame['Close']
        time = data_frame['StartTime']

        for i in range(0, len(data_frame)):
            close_price = round(close[i], 6)
            if self.__trading.in_position:
                if self.__trading.side == 'long':
                    if is_uptrend[i]:
                        if self.__trading.should_close_by_tp(price=close_price):
                            self.__trading.close_by_tp(price=close_price)
                    else:
                        self.__trading.close_position(price=close_price)
                        self.__add_exit_order(time=time[i], price=close_price)

                if self.__trading.side == 'short':
                    if not is_uptrend[i]:
                        if self.__trading.should_close_by_tp(close_price):
                            self.__trading.close_by_tp(close_price)
                    else:
                        self.__trading.close_position(price=close_price)
                        self.__add_exit_order(time=time[i], price=close_price)

            if not self.__trading.in_position:
                entry_price = round(close_price, 6)
                balance = self.__trading.balance

                if is_uptrend[i]:
                    self.__trading.new_position(
                        entry_price=entry_price,
                        side='long',
                        position_size=math.floor(balance / close_price)
                    )
                    self.__add_entry_order(time=time[i], price=entry_price)
                    continue
                else:
                    self.__trading.new_position(
                        entry_price=entry_price,
                        side='short',
                        position_size=math.floor(balance / close_price)
                    )
                    self.__add_entry_order(time=time[i], price=entry_price)
                    continue

        if self.__trading.in_short_position() or self.__trading.in_long_position():
            self.__trading.close_position(close[i])
            self.__add_exit_order(time=time[i], price=close[i])

        earning = self.__trading.balance - investment
        roi = round(earning / investment * 100, 2)

        if self.__enable_log:
            _earning = round(earning, 2)
            _investment = investment
            _balance = round(self.__trading.balance, 2)
            print(f'Earning from ${_investment} is ${_earning} (ROI = {roi}%, Balance = ${_balance})')

        self.__roi_list.append((period, multiplier, roi))

    def top_results(self, count=10):
        return pandas \
            .DataFrame(self.__roi_list, columns=['ATR_period', 'Multiplier', 'ROI']) \
            .sort_values(by=['ROI'], ascending=False).head(count)
