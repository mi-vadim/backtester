import pandas

from backtester import Backtester

data_frame = pandas.read_csv('data/CRV-PERP.csv', index_col=None)
backtester = Backtester(data_frame=data_frame)

try:
    period = int(input("Enter period: "))
    multiplier = float(input("Enter multiplier: "))
except ValueError:
    period = 0
    multiplier = 0.0
    print('ERROR: You should input only numbers!!!')

if period > 0 and multiplier > 0:
    backtester.super_trend(period=period, multiplier=multiplier, investment=1000, use_tp=False)
else:
    for period, multiplier in [(x, y / 10) for x in range(1, 2) for y in range(10, 11)]:
        backtester.super_trend(period=period, multiplier=multiplier, investment=1000, use_tp=False)
    print(backtester.top_results())

