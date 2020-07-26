from bs4 import BeautifulSoup
import logging
import pandas as pd
import pandas_datareader.data as web
import re
import requests

from app.models.candle import StockData
import settings

logger = logging.getLogger(__name__)


class GetStockPrice(object):
    def __init__(self, stock_code=settings.stock_code_default):
        self.code = stock_code
        self.kabutan_URL = settings.kabutan_URL
        self.kabutan_col_dic = {0: 'Date', 1: 'Open',
                                2: 'High', 3: 'Low', 4: 'Close', 5: 'Volume'}
        self.kabutan_col_list = ['Open', 'High', 'Low', 'Close', 'Volume']

    @property
    def get_stock_data(self):
        if re.search(r'\d', self.code) is not None:
            code = '{}.JP'.format(self.code)
            stooq_data = self.get_from_stooq(code=code)
            kabutan_data = self.get_from_kabutan()
            return pd.concat([kabutan_data, stooq_data])
        return self.get_from_stooq(code=self.code)

    def get_from_stooq(self, code):
        stooq_data = web.DataReader(name=code, data_source='stooq')
        return stooq_data

    def get_from_kabutan(self):
        html = requests.get(self.kabutan_URL)

        # Get stock data from kabutan.jp
        soup = BeautifulSoup(html.text, 'html.parser')
        table = soup.findAll('table', {'class': 'stock_kabuka0'})[0]
        rows = table.findAll('tr')

        cell_list = []
        for cell in rows[1].findAll(['td', 'th']):
            cell_list.append(cell.get_text().replace(',', ''))
        del cell_list[5:7]

        # formatting the got stock data
        kabutan_data = pd.DataFrame(cell_list).T
        kabutan_data.rename(columns=self.kabutan_col_dic, inplace=True)
        kabutan_data[self.kabutan_col_list] = \
            kabutan_data[self.kabutan_col_list].apply(pd.to_numeric)
        kabutan_data['Date'] = \
            pd.to_datetime(kabutan_data['Date'], yearfirst=True)
        kabutan_data.set_index('Date', inplace=True)

        return kabutan_data

    def save_in_database(self):
        stock_data = self.get_stock_data
        StockData.create(stock_df=stock_data)
