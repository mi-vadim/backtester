import pandas

from backtester import Backtester

data_frame = pandas.read_csv('data/FTT-PERP.csv', index_col=None)
backtester = Backtester(data_frame=data_frame)

for period, multiplier in [(x, y / 10) for x in range(1, 15) for y in range(10, 120)]:
    backtester.super_trend(period=period, multiplier=multiplier, investment=1000, use_tp=False)

print(backtester.top_results())

