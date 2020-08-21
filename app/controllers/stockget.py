from bs4 import BeautifulSoup
import logging
import pandas as pd
import pandas_datareader.data as web
import re
import requests

from app.models.candle import StockData
import constants
import settings

logger = logging.getLogger(__name__)


class StooqDataGetError(Exception):
    'failed getting stock data from stooq'


class KabutanDataGetError(Exception):
    'failed web scraping of kabutan page'


class GetStockPrice(object):
    def __init__(self, stock_code=settings.stock_code_default):
        self.code = stock_code
        self.kabutan_URL = settings.kabutan_URL
        self.kabutan_col_dic = constants.KABUTAN_COL_DIC
        self.kabutan_col_list = constants.KABUTAN_COL_LIST

    @property
    def get_stock_data(self):
        if re.search(r'\d', self.code) is not None:
            code = '{}.JP'.format(self.code)
            stooq_data = self.get_from_stooq(code=code)
            kabutan_data = self.get_from_kabutan()
            add_stock_data = pd.concat([kabutan_data, stooq_data])
            return add_stock_data

        stock_data = self.get_from_stooq(code=self.code)
        return stock_data

    def get_from_stooq(self, code):
        try:
            stooq_data = web.DataReader(name=code, data_source='stooq')
        except StooqDataGetError as stooq_error:
            logger.warning(
                '<action=GetStockPrice->>get_from_stooq>: {}'.format(stooq_error))
            raise
        return stooq_data

    def get_from_kabutan(self):
        try:
            html = requests.get(self.kabutan_URL)

            # Get stock data from kabutan.jp
            soup = BeautifulSoup(html.text, 'html.parser')
            table = soup.findAll('table', {'class': 'stock_kabuka0'})[0]
            rows = table.findAll('tr')
        except KabutanDataGetError as kabutan_error:
            logger.warning(
                '<action=GetStockPrice->>get_from_kabutan>: {}'.format(kabutan_error))
            raise

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
        logger.info(
            '<action=GetStockPrice->>save_in_database>: start getting stockdata')
        stock_data = self.get_stock_data
        StockData.create(stock_df=stock_data)
        logger.info(
            '<action=GetStockPrice->>save_in_database>: end getting stockdata and saved in database')
