import logging
import sys

# from app.models.candle import StockData
# from app.controllers.stockget import GetStockPrice
from app.controllers.webserver import run

logging.basicConfig(level=logging.INFO, stream=sys.stdout)
logger = logging.getLogger(__name__)


if __name__ == '__main__':
    # data = GetStockPrice().get_stock_data
    # StockData.create(data)
    run()
