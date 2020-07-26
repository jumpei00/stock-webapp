import logging
import sys

from app.controllers.webserver import run

logging.basicConfig(level=logging.INFO, stream=sys.stdout)
logger = logging.getLogger(__name__)


def append(data):
    data.append(4)


if __name__ == '__main__':
    run()
