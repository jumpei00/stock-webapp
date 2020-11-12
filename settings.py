import configparser

conf = configparser.ConfigParser()
conf.read('settings.ini')

stock_code_default = conf['stock_code']['default']
kabutan_URL = conf['stock_code']['kabutan_URL']

db_name = conf['db']['name']
db_driver = conf['db']['driver']

web_ip = conf['web']['ip']
web_port = int(conf['web']['port'])

duration_defalut = int(conf['duration']['default'])
duration_backtest = int(conf['duration']['backtest'])
