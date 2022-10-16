import pandas

from src.backtester.indicators.supertrend import SuperTrend
from src.trader.trading import Trade


class Backtester:
    __data_frame = None
    __enable_log = None
    __trading = None
    __roi_list = []

    def __init__(self, data_frame, enable_log=True):
        self.__data_frame = data_frame
        self.__enable_log = enable_log
        self.__trading = Trade()

    def super_trend(self, period, multiplier, investment, use_tp=False):
        print(f'\n ============')
        print(f'SuperTrend Params (ATR Period = {period}, Factor = {multiplier})')

        self.__trading.reset(balance=investment, use_tp=use_tp)
        supertrend = SuperTrend(atr_period=period, factor=multiplier)
        new_df = self.__data_frame
        data_frame = new_df.join(supertrend.set_dataframe(df=new_df).calculate())
        trades = []

        is_uptrend = data_frame['Supertrend']
        close = data_frame['close']
        open_prices = data_frame['open']
        high = data_frame['high']
        low = data_frame['low']
        time = data_frame['startTime']

        for i in range(0, len(data_frame)):
            close_price = round(close[i], 6)
            if self.__trading.in_position:
                self.__trading.add_trading_data(open_prices[i], high[i], close[i], low[i])
                if self.__trading.side == 'long':
                    if is_uptrend[i]:
                        if self.__trading.should_close_by_tp(price=close_price):
                            self.__trading.close_by_tp(price=close_price)
                    else:
                        trades.append(
                            self.__trading.close_position(price=close_price, time=time[i])
                        )
                if self.__trading.side == 'short':
                    if not is_uptrend[i]:
                        if self.__trading.should_close_by_tp(close_price):
                            self.__trading.close_by_tp(close_price)
                    else:
                        trades.append(
                            self.__trading.close_position(price=close_price, time=time[i])
                        )
            if not self.__trading.in_position:
                if is_uptrend[i]:
                    side = 'long'
                else:
                    side = 'short'
                self.__trading.new_position(entry_price=round(close_price, 6), side=side, time=time[i])
                self.__trading.add_trading_data(open_prices[i], high[i], close[i], low[i])

        if self.__trading.in_short_position() or self.__trading.in_long_position():
            self.__trading.add_trading_data(open_prices[i], high[i], close[i], low[i])
            trades.append(
                self.__trading.close_position(price=close[i], time=time[i])
            )

        earning = self.__trading.balance - investment
        roi = round(earning / investment * 100, 2)

        if self.__enable_log:
            _earning = round(earning, 2)
            _investment = investment
            _balance = round(self.__trading.balance, 2)
            print(f'Earning from ${_investment} is ${_earning} (ROI = {roi}%, Balance = ${_balance})')

        self.__roi_list.append((period, multiplier, roi))
        exit_df = pandas.DataFrame(
            data=trades,
            columns=['side', 'entry_time', 'entry_price', 'exit_time', 'exit_price', 'mfe', 'mae']
        )
        exit_df.to_csv("data/outputs/trading_results.csv", sep='\t')

    def top_results(self, count=3):
        return pandas \
            .DataFrame(self.__roi_list, columns=['ATR_period', 'Multiplier', 'ROI']) \
            .sort_values(by=['ROI'], ascending=False).head(count)
