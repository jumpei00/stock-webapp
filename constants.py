KABUTAN_COL_DIC = {0: 'Date', 1: 'Open', 2: 'High', 3: 'Low', 4: 'Close', 5: 'Volume'}
KABUTAN_COL_LIST = ['Open', 'High', 'Low', 'Close', 'Volume']

BACKTEST = 'backtest'
EMA = 'ema'
BBANDS = 'bbands'
ICHIMOKU = 'ichimoku'
RSI = 'rsi'
MACD = 'macd'
WILLR = 'willr'
STOCHF = 'stochf'
STOCH = 'stoch'

BASE_LIST = [EMA, BBANDS, ICHIMOKU, RSI, MACD, WILLR, STOCHF, STOCH]

TOTAL = 0.0
BEFORE_SELL = 0.0

BUY = 'BUY'
SELL = 'SELL'
NO_TRADE = 'NO_TRADE'

PARAMS_COL_NAMES = [
    'code',
    'ema_performance', 'ema_short_period', 'ema_long_period',
    'bb_performance', 'bb_n', 'bb_k',
    'ichimoku_performance',
    'rsi_performance', 'rsi_period', 'rsi_buy_thread', 'rsi_sell_thread',
    'macd_performance', 'macd_fast_period', 'macd_slow_period', 'macd_signal_period',
    'willr_performance', 'willr_period', 'willr_buy_thread', 'willr_sell_thread',
    'stochf_performance', 'stochf_fastk_period', 'stochf_fastd_period',
    'stochf_buy_thread', 'stochf_sell_thread',
    'stoch_performance', 'stoch_fastk_period', 'stoch_slowk_period', 'stoch_slowd_period',
    'stoch_buy_thread', 'stoch_sell_thread']

SIGNAL_EVENTS = {
    'ema_event': None,
    'bb_event': None,
    'ichimoku_event': None,
    'rsi_event': None,
    'macd_event': None,
    'willr_event': None,
    'stochf_event': None,
    'stoch_event': None
}

TODAY_TRADES = {
    'ema_trade': NO_TRADE,
    'bb_trade': NO_TRADE,
    'ichimoku': NO_TRADE,
    'rsi_trade': NO_TRADE,
    'macd_trade': NO_TRADE,
    'willr_trade': NO_TRADE,
    'stochf_trade': NO_TRADE,
    'stoch_trade': NO_TRADE
}
