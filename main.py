import logging

from app.controllers.webserver import run

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


if __name__ == '__main__':
    logger.info('<action=main>: webserver start')
    run()
