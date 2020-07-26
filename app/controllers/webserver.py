from flask import Flask
from flask import jsonify
from flask import render_template
from flask import request

from app.controllers.stockget import GetStockPrice
from app.models.dfcandles import DataFrameCandle
from app.models.base import Session
from utils.utils import bool_from_str
import settings


app = Flask(__name__, static_folder='../../static',
            template_folder='../../templates')


@app.teardown_appcontext
def remove_session(ex=None):
    Session.remove()


@app.route('/')
def index():
    return render_template('./index.html')


@app.route('/candle', methods=['GET'])
def cnadle_api():
    status = bool_from_str(request.args.get('status'))
    stock_code = request.args.get('stockcode')
    duration = request.args.get('duration')

    if status:
        get_stock_data = GetStockPrice(stock_code=stock_code)
        get_stock_data.save_in_database()

    df = DataFrameCandle(duration=duration)

    sma = request.args.get('sma')
    if sma:
        str_sma_period_1 = request.args.get('smaPeriod1')
        str_sma_period_2 = request.args.get('smaPeriod2')
        str_sma_period_3 = request.args.get('smaPeriod3')
        if not str_sma_period_1:
            period_1 = 7
        else:
            period_1 = abs(int(str_sma_period_1))

        if not str_sma_period_2:
            period_2 = 14
        else:
            period_2 = abs(int(str_sma_period_2))

        if not str_sma_period_3:
            period_3 = 50
        else:
            period_3 = abs(int(str_sma_period_3))
        df.add_sma(period=period_1)
        df.add_sma(period=period_2)
        df.add_sma(period=period_3)

    ema = request.args.get('ema')
    if ema:
        str_ema_period_1 = request.args.get('emaPeriod1')
        str_ema_period_2 = request.args.get('emaPeriod2')
        str_ema_period_3 = request.args.get('emaPeriod3')
        if not str_ema_period_1:
            period_1 = 7
        else:
            period_1 = abs(int(str_ema_period_1))

        if not str_ema_period_2:
            period_2 = 14
        else:
            period_2 = abs(int(str_ema_period_2))

        if not str_ema_period_3:
            period_3 = 50
        else:
            period_3 = abs(int(str_ema_period_3))
        df.add_ema(period=period_1)
        df.add_ema(period=period_2)
        df.add_ema(period=period_3)

    bbands = request.args.get('bbands')
    if bbands:
        str_n = request.args.get('bbandsN')
        str_k = request.args.get('bbandsK')
        if not str_n:
            n = 20
        else:
            n = abs(int(str_n))

        if not str_k:
            k = 2
        else:
            k = abs(int(str_k))
        df.add_bbands(n=n, k=k)

    ichimoku = request.args.get('ichimoku')
    if ichimoku:
        df.add_ichimoku()

    rsi = request.args.get('rsi')
    if rsi:
        str_period = request.args.get('rsiPeriod')
        if not str_period:
            period = 14
        else:
            period = abs(int(str_period))
        df.add_rsi(period=period)

    macd = request.args.get('macd')
    if macd:
        str_macd_fast_period = request.args.get('macdPeriod1')
        str_macd_slow_period = request.args.get('macdPeriod2')
        str_macd_signal_period = request.args.get('macdPeriod3')
        if not str_macd_fast_period:
            fast_period = 12
        else:
            fast_period = abs(int(str_macd_fast_period))

        if not str_macd_slow_period:
            slow_period = 26
        else:
            slow_period = abs(int(str_macd_slow_period))

        if not str_macd_signal_period:
            signal_period = 9
        else:
            signal_period = abs(int(str_macd_signal_period))
        df.add_macd(fast_period=fast_period,
                    slow_period=slow_period, signal_period=signal_period)

    willr = request.args.get('willr')
    if willr:
        str_period = request.args.get('willrPeriod')
        if not str_period:
            period = 14
        else:
            period = abs(int(str_period))
        df.add_willr(period=period)

    stochf = request.args.get('stochf')
    if stochf:
        str_stochf_fastk_period = request.args.get('stochfPeriod1')
        str_stochf_fastd_period = request.args.get('stochfPeriod2')
        if not str_stochf_fastk_period:
            fastk_period = 9
        else:
            fastk_period = abs(int(str_stochf_fastk_period))

        if not str_stochf_fastd_period:
            fastd_period = 3
        else:
            fastd_period = abs(int(str_stochf_fastd_period))
        df.add_stochf(fastk_period=fastk_period, fastd_period=fastd_period)

    stoch = request.args.get('stoch')
    if stoch:
        str_stoch_fastk_period = request.args.get('stochPeriod1')
        str_stoch_slowk_period = request.args.get('stochPeriod2')
        str_stoch_slowd_period = request.args.get('stochPeriod3')
        if not str_stoch_fastk_period:
            fastk_period = 9
        else:
            fastk_period = abs(int(str_stoch_fastk_period))

        if not str_stoch_slowk_period:
            slowk_period = 3
        else:
            slowk_period = abs(int(str_stoch_slowk_period))

        if not str_stoch_slowd_period:
            slowd_period = 3
        else:
            slowd_period = abs(int(str_stoch_slowd_period))
        df.add_stoch(fastk_period=fastk_period,
                     slowk_period=slowk_period, slowd_period=slowd_period)

    return jsonify(df.values), 200


def run():
    app.run(host='0.0.0.0', port=settings.web_port, threaded=True)
