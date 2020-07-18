import logging
import sys

from app.models.database.candle import StockData

logging.basicConfig(level=logging.INFO, stream=sys.stdout)
logger = logging.getLogger(__name__)


if __name__ == '__main__':
    print(StockData.values)
