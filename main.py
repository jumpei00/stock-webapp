import logging
import sys

from app.controllers.webserver import run


logging.basicConfig(level=logging.INFO, stream=sys.stdout)
logger = logging.getLogger(__name__)


if __name__ == '__main__':
    logger.info('#####action: main -> webserver start#####')
    run()
