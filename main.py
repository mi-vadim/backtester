from src.backtester.backtester import Backtester
from src.importer.importer import Importer

importer = Importer()
ticker = input('Enter ticker from FTX (Example: BTC-PERP): ')
start_date = input('Enter start date of backtest (Example: 2022-01-01): ')
resolution_in_seconds = input('Enter resolution for chart data in seconds (Example 3600 (1H)): ')

if ticker == '':
    raise NameError('NotEnteredTicker')

if start_date == '':
    start_date = '2021-01-01'

backtester = Backtester(
    data_frame=importer.get_data_frame(ticker=ticker, from_date=start_date, resolution=resolution_in_seconds)
)

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
    for period, multiplier in [(x, y / 10) for x in range(1, 15) for y in range(10, 120)]:
        backtester.super_trend(period=period, multiplier=multiplier, investment=1000, use_tp=False)
    print(backtester.top_results())

