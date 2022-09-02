from datetime import date
from os.path import exists
from src.importer.FTXClient import FtxClient
import pandas


class Importer:
    def __init__(self):
        self._client = FtxClient(api_key='', api_secret='')

    def _retrieve_data(self, ticker, start_time, end_time) -> []:
        data = []
        dti = pandas.date_range(start=start_time, end=end_time, freq="M")
        for day in dti:
            from_date = day.replace(day=1).timestamp()
            to_date = day.replace(hour=23, minute=59, second=59).timestamp()
            response = self._client.get_historical_prices(
                market=ticker,
                resolution=300,
                start_time=from_date,
                end_time=to_date
            )
            for i in response:
                data.append(i)
        return data

    def get_data_frame(self, ticker, from_date=None, to_date=None):
        if from_date is None:
            from_date = date.fromisoformat('2021-01-01')
        else:
            from_date = date.fromisoformat(from_date)

        if to_date is None:
            to_date = date.today()
        else:
            to_date = date.fromisoformat(to_date)

        saved_filepath = 'data/inputs/' + ticker \
                         + '_' + from_date.strftime('%Y-%m-%d') \
                         + '_' + to_date.strftime('%Y-%m-%d') \
                         + '.csv'

        if exists(path=saved_filepath):
            return pandas.read_csv(filepath_or_buffer=saved_filepath)

        date_frame = pandas.DataFrame(
            data=self._retrieve_data(ticker=ticker, start_time=from_date, end_time=to_date),
            columns=['startTime', 'open', 'high', 'low', 'close']
        )
        date_frame.to_csv(saved_filepath)

        return date_frame
