import configparser

conf = configparser.ConfigParser()
conf.read('settings.ini')

default = conf['stock_code']['default']
kabutan_URL = conf['stock_code']['kabutan_URL']

db_name = conf['db']['name']
db_driver = conf['db']['driver']

web_port = conf['web']['port']

backtest_period = conf['backtest']['period']
