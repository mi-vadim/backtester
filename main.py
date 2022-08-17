import pandas

from backtester import Backtester

data_frame = pandas.read_csv('data/NEAR-PERP.csv', index_col=None)
backtester = Backtester(data_frame=data_frame)

for period, multiplier in [(x, y / 10) for x in range(1, 15) for y in range(10, 120)]:
    backtester.super_trend(period=period, multiplier=multiplier, investment=1000)

print(backtester.top_results())

