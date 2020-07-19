import logging
import sys

# from app.models.database.dfcandles import DataFrameCandle
from app.controllers.webserver import run

logging.basicConfig(level=logging.INFO, stream=sys.stdout)
logger = logging.getLogger(__name__)


if __name__ == '__main__':
    run()
