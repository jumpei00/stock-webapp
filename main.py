import logging
import sys

from app.models.database.stockget import GetStockPrice

logging.basicConfig(level=logging.INFO, stream=sys.stdout)
logger = logging.getLogger(__name__)


if __name__ == '__main__':
    get_stock_price = GetStockPrice(code='1570')
    print(get_stock_price.get_stock_data)
