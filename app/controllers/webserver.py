from flask import Flask
from flask import jsonify
from flask import render_template
from flask import request
import logging

from dict2obj import Dict2Obj

from app.controllers.ai import AI
from app.controllers.stockget import GetStockPrice
from app.models.dfcandles import DataFrameCandle
from app.models.base import Session
from utils.utils import bool_from_str
import settings


app = Flask(__name__, static_folder='../../static',
            template_folder='../../templates')

logger = logging.getLogger(__name__)


@app.teardown_appcontext
def remove_session(ex=None):
    Session.remove()


@app.route('/')
def index():
    return render_template('./index.html')


def run():
    app.run(host='0.0.0.0', port=settings.web_port, threaded=True)


@app.route('/candle', methods=['GET'])
# chart request
def cnadle_api():
    logger.info('action candle_api: accessed')
    status = bool_from_str(request.args.get('status'))
    stock_code = request.args.get('stockcode')
    duration = request.args.get('duration')
    logger.info(
        'action candle_api\n'
        '<query_params>\n'
        'status: {}\n'
        'stock_code: {}\n'
        'duration: {}'.format(status, stock_code, duration))

    if status:
        get_stock_data = GetStockPrice(stock_code=stock_code)
        get_stock_data.save_in_database()

    df = DataFrameCandle(code=stock_code, duration=duration)

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
            k = abs(float(str_k))
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

    logger.info(
        'action candle_api\n'
        '<query_params_indicator>\n'
        'sma: {}\n'
        'ema: {}\n'
        'bb: {}\n'
        'ichimoku: {}\n'
        'rsi: {}\n'
        'macd: {}\n'
        'willr: {}\n'
        'stochf: {}\n'
        'stoch: {}'.format(sma, ema, bbands, ichimoku, rsi, macd, willr, stochf, stoch))

    return jsonify(df.chart_values), 200


@app.route('/trade', methods=['GET'])
# trade and backtest request
def trade_api():
    stock_code = request.args.get('stockcode')
    trade = request.args.get('trade')
    backtest = bool_from_str(request.args.get('backtest'))
    logger.info(
        'action trade_api\n'
        '<query_params>\n'
        'stock_code: {}\n'
        'trade: {}\n'
        'backtest: {}'.format(stock_code, trade, backtest))

    ai = AI(code=stock_code)

    if trade and backtest:
        ema_status, ema_params = CreateBackTestParams.ema_params(
            str_ema_short_period_low=request.args.get('emaBacktest1'),
            str_ema_short_period_up=request.args.get('emaBacktest2'),
            str_ema_long_period_low=request.args.get('emaBacktest3'),
            str_ema_long_period_up=request.args.get('emaBacktest4'))
        if not ema_status:
            return jsonify(ema_params), 400

        bb_status, bb_params = CreateBackTestParams.bb_params(
            str_n_low=request.args.get('bbandsBacktest1'),
            str_n_up=request.args.get('bbandsBacktest2'),
            str_k_low=request.args.get('bbandsBacktest3'),
            str_k_up=request.args.get('bbandsBacktest4'))
        if not bb_status:
            return jsonify(bb_status), 400

        rsi_status, rsi_params = CreateBackTestParams.rsi_params(
            str_rsi_period_low=request.args.get('rsiBacktest1'),
            str_rsi_period_up=request.args.get('rsiBacktest1'),
            str_rsi_buy_thred_low=request.args.get('rsiBacktest1'),
            str_rsi_buy_thred_up=request.args.get('rsiBacktest1'),
            str_rsi_sell_thred_low=request.args.get('rsiBacktest1'),
            str_rsi_sell_thred_up=request.args.get('rsiBacktest1'))
        if not rsi_status:
            return jsonify(rsi_params), 400

        macd_status, macd_params = CreateBackTestParams.macd_params(
            str_macd_fast_period_low=request.args.get('macdBacktest1'),
            str_macd_fast_period_up=request.args.get('macdBacktest2'),
            str_macd_slow_period_low=request.args.get('macdBacktest3'),
            str_macd_slow_period_up=request.args.get('macdBacktest4'),
            str_macd_signal_period_low=request.args.get('macdBacktest5'),
            str_macd_signal_period_up=request.args.get('macdBacktest6'))
        if not macd_status:
            return jsonify(macd_params), 400

        willr_status, willr_params = CreateBackTestParams.willr_params(
            str_willr_period_low=request.args.get('willrBacktest1'),
            str_willr_period_up=request.args.get('willrBacktest2'),
            str_willr_buy_thred_low=request.args.get('willrBacktest3'),
            str_willr_buy_thred_up=request.args.get('willrBacktest4'),
            str_willr_sell_thred_low=request.args.get('willrBacktest5'),
            str_willr_sell_thred_up=request.args.get('willrBacktest6'))
        if not willr_status:
            return jsonify(willr_params), 400

        stochf_status, stochf_params = CreateBackTestParams.stochf_params(
            str_stochf_fastk_period_low=request.args.get('stochfBacktest1'),
            str_stochf_fastk_period_up=request.args.get('stochfBacktest2'),
            str_stochf_fastd_period_low=request.args.get('stochfBacktest3'),
            str_stochf_fastd_period_up=request.args.get('stochfBacktest4'),
            str_stochf_buy_thread_low=request.args.get('stochfBacktest5'),
            str_stochf_buy_thread_up=request.args.get('stochfBacktest6'),
            str_stochf_sell_thread_low=request.args.get('stochfBacktest7'),
            str_stochf_sell_thread_up=request.args.get('stochfBacktest8'))
        if not stochf_status:
            return jsonify(stochf_params), 400

        stoch_status, stoch_params = CreateBackTestParams.stoch_params(
            str_stoch_fastk_period_low=request.args.get('stochBacktest1'),
            str_stoch_fastk_period_up=request.args.get('stochBacktest2'),
            str_stoch_slowk_period_low=request.args.get('stochBacktest3'),
            str_stoch_slowk_period_up=request.args.get('stochBacktest4'),
            str_stoch_slowd_period_low=request.args.get('stochBacktest5'),
            str_stoch_slowd_period_up=request.args.get('stochBacktest6'),
            str_stoch_buy_thread_low=request.args.get('stochBacktest7'),
            str_stoch_buy_thread_up=request.args.get('stochBacktest8'),
            str_stoch_sell_thread_low=request.args.get('stochBacktest9'),
            str_stoch_sell_thread_up=request.args.get('stochBacktest10'))
        if not stoch_status:
            return jsonify(stoch_params), 400

        test_params = Dict2Obj({
            'ema': ema_params, 'bb': bb_params, 'rsi': rsi_params,
            'macd': macd_params, 'willr': willr_params,
            'stochf': stochf_params, 'stoch': stoch_params})

        today_trade = ai.trade(test_params=test_params, backtest=backtest)

    elif trade and not backtest:
        today_trade = ai.trade()

    if today_trade is None:
        return jsonify(ai.df.trade_values), 400

    ai.df.add_params()
    ai.df.each_event = today_trade

    return jsonify(ai.df.trade_values), 400


class CreateBackTestParams(object):
    @ staticmethod
    def ema_params(str_ema_short_period_low, str_ema_short_period_up,
                   str_ema_long_period_low, str_ema_long_period_up):
        # evaluate short period params
        if not str_ema_short_period_low:
            message = 'Error: Not low short period of EMA'
            logger.warning(
                'action trade_api -> CreateBackTestParams -> ema_params: {}'.format(message))
            return False, {'message': message}
        else:
            short_period_low = abs(int(str_ema_short_period_low))

        if not str_ema_short_period_up:
            logger.warning(
                'action trade_api -> CreateBackTestParams -> ema_params: {}'.format(message))
            message = 'Error: Not up short period of EMA'
            return False, {'message': message}
        else:
            short_period_up = abs(int(str_ema_short_period_up))

        # evaluate long period params
        if not str_ema_long_period_low:
            logger.warning(
                'action trade_api -> CreateBackTestParams -> ema_params: {}'.format(message))
            message = 'Error: Not low long period of EMA'
            return False, {'message': message}
        else:
            long_period_low = abs(int(str_ema_long_period_low))

        if not str_ema_long_period_up:
            logger.warning(
                'action trade_api -> CreateBackTestParams -> ema_params: {}'.format(message))
            message = 'Error: Not up long period of EMA'
            return False, {'message': message}
        else:
            long_period_up = abs(int(str_ema_long_period_up))

        # compare large number of params
        if short_period_low > short_period_up:
            logger.warning(
                'action trade_api -> CreateBackTestParams -> ema_params: {}'.format(message))
            message = 'Error: low short period of EMA is large more than up short period of EMA'
            return False, {'message': message}
        if long_period_low > long_period_up:
            logger.warning(
                'action trade_api -> CreateBackTestParams -> ema_params: {}'.format(message))
            message = 'Error: low long period of EMA is large more than up long period of EMA'
            return False, {'message': message}

        logger.info(
            'action trade_api\n'
            '<ema-params>\n'
            'short_period_low: {}\n'
            'short_period_up: {}\n'
            'long_period_low :{}\n'
            'long_period_up :{}'.format(short_period_low, short_period_up, long_period_low, long_period_up))

        ema_params = Dict2Obj(
            {'ema1': short_period_low, 'ema2': short_period_up,
             'ema3': long_period_low, 'ema4': long_period_up})

        return True, ema_params

    @ staticmethod
    def bb_params(str_n_low, str_n_up, str_k_low, str_k_up):
        # evaluate n params
        if not str_n_low:
            message = 'Error: Not low n of BBands'
            logger.warning(
                'action trade_api -> CreateBackTestParams -> bb_params: {}'.format(message))
            return False, {'message': message}
        else:
            n_low = abs(int(str_n_low))

        if not str_n_up:
            message = 'Error: Not up n of BBands'
            logger.warning(
                'action trade_api -> CreateBackTestParams -> bb_params: {}'.format(message))
            return False, {'message': message}
        else:
            n_up = abs(int(str_n_up))

        # evaluate k params
        if not str_k_low:
            message = 'Error: Not low k of BBands'
            logger.warning(
                'action trade_api -> CreateBackTestParams -> bb_params: {}'.format(message))
            return False, {'message': message}
        else:
            k_low = abs(float(str_k_low))

        if not str_k_up:
            message = 'Error: Not up k of BBands'
            logger.warning(
                'action trade_api -> CreateBackTestParams -> bb_params: {}'.format(message))
            return False, {'message': 'Error: Not up long period of EMA'}
        else:
            k_up = abs(float(str_k_up))

        # compare large number of params
        if n_low > n_up:
            message = 'Error: low n of BBands is large more than up n of BBands'
            logger.warning(
                'action trade_api -> CreateBackTestParams -> bb_params: {}'.format(message))
            return False, {'message': message}
        if k_low > k_up:
            message = 'Error: low k of BBands is large more than up k of BBands'
            logger.warning(
                'action trade_api -> CreateBackTestParams -> bb_params: {}'.format(message))
            return False, {'message': message}

        logger.info(
            'action trade_api\n'
            '<bb-params>\n'
            'n_low: {}\n'
            'n_up: {}\n'
            'k_low :{}\n'
            'k_up :{}'.format(n_low, n_up, k_low, k_up))

        bb_params = Dict2Obj(
            {'bb1': n_low, 'bb2': n_up, 'bb3': k_low, 'bb4': k_up})

        return True, bb_params

    @ staticmethod
    def rsi_params(str_rsi_period_low, str_rsi_period_up,
                   str_rsi_buy_thred_low, str_rsi_buy_thred_up,
                   str_rsi_sell_thred_low, str_rsi_sell_thred_up):
        # evaluate period params
        if not str_rsi_period_low:
            message = 'Error: Not low period of RSI'
            logger.warning(
                'action trade_api -> CreateBackTestParams -> rsi_params: {}'.format(message))
            return False, {'message': message}
        else:
            rsi_period_low = abs(int(str_rsi_period_low))

        if not str_rsi_period_up:
            message = 'Error: Not up period of RSI'
            logger.warning(
                'action trade_api -> CreateBackTestParams -> rsi_params: {}'.format(message))
            return False, {'message': message}
        else:
            rsi_period_up = abs(int(str_rsi_period_up))

        # evaluate buy thread params
        if not str_rsi_buy_thred_low:
            message = 'Error: Not low buy thread of RSI'
            logger.warning(
                'action trade_api -> CreateBackTestParams -> rsi_params: {}'.format(message))
            return False, {'message': message}
        else:
            rsi_buy_thread_low = abs(int(str_rsi_buy_thred_low))

        if not str_rsi_buy_thred_up:
            message = 'Error: Not up buy thread of RSI'
            logger.warning(
                'action trade_api -> CreateBackTestParams -> rsi_params: {}'.format(message))
            return False, {'message': message}
        else:
            rsi_buy_thread_up = abs(int(str_rsi_buy_thred_up))

        # evaluate sell thread params
        if not str_rsi_sell_thred_low:
            message = 'Error: Not low sell thread of RSI'
            logger.warning(
                'action trade_api -> CreateBackTestParams -> rsi_params: {}'.format(message))
            return False, {'message': message}
        else:
            rsi_sell_thread_low = abs(int(str_rsi_sell_thred_low))

        if not str_rsi_sell_thred_up:
            message = 'Error: Not up sell thread of RSI'
            logger.warning(
                'action trade_api -> CreateBackTestParams -> rsi_params: {}'.format(message))
            return False, {'message': message}
        else:
            rsi_sell_thread_up = abs(int(str_rsi_sell_thred_up))

        # compare large number of params
        if rsi_period_low > rsi_period_up:
            message = 'Error: low period of RSI is large more than up period of RSI'
            logger.warning(
                'action trade_api -> CreateBackTestParams -> rsi_params: {}'.format(message))
            return False, {'message': message}
        if rsi_buy_thread_low > rsi_buy_thread_up:
            message = 'Error: low buy thread of RSI is large more than up buy thread of RSI'
            logger.warning(
                'action trade_api -> CreateBackTestParams -> rsi_params: {}'.format(message))
            return False, {'message': message}
        if rsi_sell_thread_low > rsi_sell_thread_up:
            message = 'Error: low sell thread of RSI is large more than up sell thread of RSI'
            logger.warning(
                'action trade_api -> CreateBackTestParams -> rsi_params: {}'.format(message))
            return False, {'message': message}

        logger.info(
            'action trade_api\n'
            '<rsi-params>\n'
            'rsi_period_low: {}\n'
            'rsi_period_up: {}\n'
            'rsi_buy_thread_low :{}\n'
            'rsi_buy_thread_up :{}\n'
            'rsi_sell_thread_low :{}\n'
            'rsi_sell_thread_up :{}'.format(
                rsi_period_low, rsi_period_up,
                rsi_buy_thread_low, rsi_buy_thread_up,
                rsi_sell_thread_low, rsi_sell_thread_up))

        rsi_params = Dict2Obj(
            {'rsi1': rsi_period_low, 'rsi2': rsi_period_up,
             'rsi3': rsi_buy_thread_low, 'rsi4': rsi_buy_thread_up,
             'rsi5': rsi_sell_thread_low, 'rsi6': rsi_sell_thread_up})

        return True, rsi_params

    @ staticmethod
    def macd_params(str_macd_fast_period_low, str_macd_fast_period_up,
                    str_macd_slow_period_low, str_macd_slow_period_up,
                    str_macd_signal_period_low, str_macd_signal_period_up):
        # evaluate fast period params
        if not str_macd_fast_period_low:
            message = 'Error: Not low fast period of MACD'
            logger.warning(
                'action trade_api -> CreateBackTestParams -> macd_params: {}'.format(message))
            return False, {'message': message}
        else:
            macd_fast_period_low = abs(int(str_macd_fast_period_low))

        if not str_macd_fast_period_up:
            message = 'Error: Not up fast period of MACD'
            logger.warning(
                'action trade_api -> CreateBackTestParams -> macd_params: {}'.format(message))
            return False, {'message': message}
        else:
            macd_fast_period_up = abs(int(str_macd_fast_period_up))

        # evaluate slow period params
        if not str_macd_slow_period_low:
            message = 'Error: Not low slow period of MACD'
            logger.warning(
                'action trade_api -> CreateBackTestParams -> macd_params: {}'.format(message))
            return False, {'message': message}
        else:
            macd_slow_period_low = abs(int(str_macd_slow_period_low))

        if not str_macd_slow_period_up:
            message = 'Error: Not up slow period of MACD'
            logger.warning(
                'action trade_api -> CreateBackTestParams -> macd_params: {}'.format(message))
            return False, {'message': message}
        else:
            macd_slow_period_up = abs(int(str_macd_slow_period_up))

        # evaluate signal period params
        if not str_macd_signal_period_low:
            message = 'Error: Error: Not low signal period of MACD'
            logger.warning(
                'action trade_api -> CreateBackTestParams -> macd_params: {}'.format(message))
            return False, {'message': message}
        else:
            macd_signal_period_low = abs(int(str_macd_signal_period_low))

        if not str_macd_signal_period_up:
            message = 'Error: Not up signal period of MACD'
            logger.warning(
                'action trade_api -> CreateBackTestParams -> macd_params: {}'.format(message))
            return False, {'message': message}
        else:
            macd_signal_period_up = abs(int(str_macd_signal_period_up))

        # compare large number of params
        if macd_fast_period_low > macd_fast_period_up:
            message = 'Error: low fast period of MACD is large more than up fast period of MACD'
            logger.warning(
                'action trade_api -> CreateBackTestParams -> macd_params: {}'.format(message))
            return False, {'message': message}
        if macd_slow_period_low > macd_slow_period_up:
            message = 'Error: low slow period of MACD is large more than up slow period of MACD'
            logger.warning(
                'action trade_api -> CreateBackTestParams -> macd_params: {}'.format(message))
            return False, {'message': message}
        if macd_signal_period_low > macd_signal_period_up:
            message = 'Error: low signal period of MACD is large more than up signal period of MACD'
            logger.warning(
                'action trade_api -> CreateBackTestParams -> macd_params: {}'.format(message))
            return False, {'message': message}

        logger.info(
            'action trade_api\n'
            '<macd-params>\n'
            'fast_period_low: {}\n'
            'fast_period_up: {}\n'
            'slow_period_low :{}\n'
            'slow_period_up :{}\n'
            'signal_period_low :{}\n'
            'signal_period_up :{}'.format(
                macd_fast_period_low, macd_fast_period_up,
                macd_slow_period_low, macd_slow_period_up,
                macd_signal_period_low, macd_signal_period_up))

        macd_params = Dict2Obj(
            {'macd1': macd_fast_period_low, 'macd2': macd_fast_period_up,
             'macd3': macd_slow_period_low, 'macd4': macd_slow_period_up,
             'macd5': macd_signal_period_low, 'macd6': macd_signal_period_up})

        return True, macd_params

    @ staticmethod
    def willr_params(str_willr_period_low, str_willr_period_up,
                     str_willr_buy_thred_low, str_willr_buy_thred_up,
                     str_willr_sell_thred_low, str_willr_sell_thred_up):
        # evaluate period params
        if not str_willr_period_low:
            message = 'Error: Not low period of WILLR'
            logger.warning(
                'action trade_api -> CreateBackTestParams -> willr_params: {}'.format(message))
            return False, {'message': message}
        else:
            willr_period_low = abs(int(str_willr_period_low))

        if not str_willr_period_up:
            message = 'Error: Not up period of WILLR'
            logger.warning(
                'action trade_api -> CreateBackTestParams -> willr_params: {}'.format(message))
            return False, {'message': message}
        else:
            willr_period_up = abs(int(str_willr_period_up))

        # evaluate buy thread params
        if not str_willr_buy_thred_low:
            message = 'Error: Not low buy thread of WILLR'
            logger.warning(
                'action trade_api -> CreateBackTestParams -> willr_params: {}'.format(message))
            return False, {'message': message}
        else:
            willr_buy_thread_low = -abs(int(str_willr_buy_thred_low))

        if not str_willr_buy_thred_up:
            message = 'Error: Not up buy thread of WILLR'
            logger.warning(
                'action trade_api -> CreateBackTestParams -> willr_params: {}'.format(message))
            return False, {'message': message}
        else:
            willr_buy_thread_up = -abs(int(str_willr_buy_thred_up))

        # evaluate sell thread params
        if not str_willr_sell_thred_low:
            message = 'Error: Not low sell thread of WILLR'
            logger.warning(
                'action trade_api -> CreateBackTestParams -> willr_params: {}'.format(message))
            return False, {'message': message}
        else:
            willr_sell_thread_low = -abs(int(str_willr_sell_thred_low))

        if not str_willr_sell_thred_up:
            message = 'Error: Not up sell thread of WILLR'
            logger.warning(
                'action trade_api -> CreateBackTestParams -> willr_params: {}'.format(message))
            return False, {'message': message}
        else:
            willr_sell_thread_up = -abs(int(str_willr_sell_thred_up))

        # compare large number of params
        if willr_period_low > willr_period_up:
            message = 'Error: low period of WILLR is large more than up period of WILLR'
            logger.warning(
                'action trade_api -> CreateBackTestParams -> willr_params: {}'.format(message))
            return False, {'message': message}
        if willr_buy_thread_low > willr_buy_thread_up:
            message = 'Error: low buy thread of WILLR is large more than up buy thread of WILLR'
            logger.warning(
                'action trade_api -> CreateBackTestParams -> willr_params: {}'.format(message))
            return False, {'message': message}
        if willr_sell_thread_low > willr_sell_thread_up:
            message = 'Error: low sell thread of WILLR is large more than up sell thread of WILLR'
            logger.warning(
                'action trade_api -> CreateBackTestParams -> willr_params: {}'.format(message))
            return False, {'message': message}

        logger.info(
            'action trade_api\n'
            '<willr-params>\n'
            'willr_period_low: {}\n'
            'willr_period_up: {}\n'
            'willr_buy_thread_low :{}\n'
            'willr_buy_thread_up :{}\n'
            'willr_sell_thread_low :{}\n'
            'willr_sell_thread_up :{}'.format(
                willr_period_low, willr_period_up,
                willr_buy_thread_low, willr_buy_thread_up,
                willr_sell_thread_low, willr_sell_thread_up))

        willr_params = Dict2Obj(
            {'willr1': willr_period_low, 'willr2': willr_period_up,
             'willr3': willr_buy_thread_low, 'willr4': willr_buy_thread_up,
             'willr5': willr_sell_thread_low, 'willr6': willr_sell_thread_up})

        return True, willr_params

    @ staticmethod
    def stochf_params(str_stochf_fastk_period_low, str_stochf_fastk_period_up,
                      str_stochf_fastd_period_low, str_stochf_fastd_period_up,
                      str_stochf_buy_thread_low, str_stochf_buy_thread_up,
                      str_stochf_sell_thread_low, str_stochf_sell_thread_up):
        # evaluate fastk params
        if not str_stochf_fastk_period_low:
            message = 'Error: Not low fastk period of STOCHF'
            logger.warning(
                'action trade_api -> CreateBackTestParams -> stochf_params: {}'.format(message))
            return False, {'message': message}
        else:
            stochf_fastk_period_low = abs(int(str_stochf_fastk_period_low))

        if not str_stochf_fastk_period_up:
            message = 'Error: Not up fastk period of STOCHF'
            logger.warning(
                'action trade_api -> CreateBackTestParams -> stochf_params: {}'.format(message))
            return False, {'message': message}
        else:
            stochf_fastk_period_up = abs(int(str_stochf_fastk_period_up))

        # evaluate fastd params
        if not str_stochf_fastd_period_low:
            message = 'Error: Not low fastd period of STOCHF'
            logger.warning(
                'action trade_api -> CreateBackTestParams -> stochf_params: {}'.format(message))
            return False, {'message': message}
        else:
            stochf_fastd_period_low = abs(int(str_stochf_fastd_period_low))

        if not str_stochf_fastd_period_up:
            message = 'Error: Not up fastd period of STOCHF'
            logger.warning(
                'action trade_api -> CreateBackTestParams -> stochf_params: {}'.format(message))
            return False, {'message': message}
        else:
            stochf_fastd_period_up = abs(int(str_stochf_fastd_period_up))

        # evaluate buy thread params
        if not str_stochf_buy_thread_low:
            message = 'Error: Not low buy thread of STOCHF'
            logger.warning(
                'action trade_api -> CreateBackTestParams -> stochf_params: {}'.format(message))
            return False, {'message': message}
        else:
            stochf_buy_thread_low = abs(int(str_stochf_buy_thread_low))

        if not str_stochf_buy_thread_up:
            message = 'Error: Not up buy thread of STOCHF'
            logger.warning(
                'action trade_api -> CreateBackTestParams -> stochf_params: {}'.format(message))
            return False, {'message': message}
        else:
            stochf_buy_thread_up = abs(int(str_stochf_buy_thread_up))

        # evaluate sell thread params
        if not str_stochf_sell_thread_low:
            message = 'Error: Not low sell thread of STOCHF'
            logger.warning(
                'action trade_api -> CreateBackTestParams -> stochf_params: {}'.format(message))
            return False, {'message': message}
        else:
            stochf_sell_thread_low = abs(int(str_stochf_sell_thread_low))

        if not str_stochf_sell_thread_up:
            message = 'Error: Not up sell thread of STOCHF'
            logger.warning(
                'action trade_api -> CreateBackTestParams -> stochf_params: {}'.format(message))
            return False, {'message': message}
        else:
            stochf_sell_thread_up = abs(int(str_stochf_sell_thread_up))

        # compare large number of params
        if stochf_fastk_period_low > stochf_fastk_period_up:
            message = 'Error: low fastk period of STOCHF is large more than up fastk period of STOCHF'
            logger.warning(
                'action trade_api -> CreateBackTestParams -> stochf_params: {}'.format(message))
            return False, {'message': message}
        if stochf_fastd_period_low > stochf_fastd_period_up:
            message = 'Error: low fastd period of STOCHF is large more than up fastd period of STOCHF'
            logger.warning(
                'action trade_api -> CreateBackTestParams -> stochf_params: {}'.format(message))
            return False, {'message': message}
        if stochf_buy_thread_low > stochf_buy_thread_up:
            message = 'Error: low buy thread of STOCHF is large more than up buy thread of STOCHF'
            logger.warning(
                'action trade_api -> CreateBackTestParams -> stochf_params: {}'.format(message))
            return False, {'message': message}
        if stochf_sell_thread_low > stochf_sell_thread_up:
            message = 'Error: low sell thread of STOCHF is large more than up sell thread of STOCHF'
            logger.warning(
                'action trade_api -> CreateBackTestParams -> stochf_params: {}'.format(message))
            return False, {'message': message}

        logger.info(
            'action trade_api\n'
            '<stochf-params>\n'
            'stochf_fastk_period_low: {}\n'
            'stochf_fastk_period_up: {}\n'
            'stochf_fastd_period_low :{}\n'
            'stochf_fastd_period_up :{}\n'
            'stochf_buy_thread_low :{}\n'
            'stochf_buy_thread_up :{}\n'
            'stochf_sell_thread_low :{}\n'
            'stochf_sell_thread_up :{}'.format(
                stochf_fastk_period_low, stochf_fastk_period_up,
                stochf_fastd_period_low, stochf_fastd_period_up,
                stochf_buy_thread_low, stochf_buy_thread_up,
                stochf_sell_thread_low, stochf_sell_thread_up))

        stochf_params = Dict2Obj(
            {'stochf1': stochf_fastk_period_low, 'stochf2': stochf_fastk_period_up,
             'stochf3': stochf_fastd_period_low, 'stochf4': stochf_fastd_period_up,
             'stochf5': stochf_buy_thread_low, 'stochf6': stochf_buy_thread_up,
             'stochf7': stochf_sell_thread_low, 'stochf8': stochf_sell_thread_up})

        return True, stochf_params

    @ staticmethod
    def stoch_params(str_stoch_fastk_period_low, str_stoch_fastk_period_up,
                     str_stoch_slowk_period_low, str_stoch_slowk_period_up,
                     str_stoch_slowd_period_low, str_stoch_slowd_period_up,
                     str_stoch_buy_thread_low, str_stoch_buy_thread_up,
                     str_stoch_sell_thread_low, str_stoch_sell_thread_up):
        # evaluate fastk params
        if not str_stoch_fastk_period_low:
            message = 'Error: Not low fastk period of STOCH'
            logger.warning(
                'action trade_api -> CreateBackTestParams -> stoch_params: {}'.format(message))
            return False, {'message': message}
        else:
            stoch_fastk_period_low = abs(int(str_stoch_fastk_period_low))

        if not str_stoch_fastk_period_up:
            message = 'Error: Not up fastk period of STOCH'
            logger.warning(
                'action trade_api -> CreateBackTestParams -> stoch_params: {}'.format(message))
            return False, {'message': message}
        else:
            stoch_fastk_period_up = abs(int(str_stoch_fastk_period_up))

        # evaluate slowk params
        if not str_stoch_slowk_period_low:
            message = 'Error: Not low slowk period of STOCH'
            logger.warning(
                'action trade_api -> CreateBackTestParams -> stoch_params: {}'.format(message))
            return False, {'message': message}
        else:
            stoch_slowk_period_low = abs(int(str_stoch_slowk_period_low))

        if not str_stoch_slowk_period_up:
            message = 'Error: Not up slowk period of STOCH'
            logger.warning(
                'action trade_api -> CreateBackTestParams -> stoch_params: {}'.format(message))
            return False, {'message': message}
        else:
            stoch_slowk_period_up = abs(int(str_stoch_slowk_period_up))

        # evaluate slowd params
        if not str_stoch_slowd_period_low:
            message = 'Error: Not low slowd period of STOCH'
            logger.warning(
                'action trade_api -> CreateBackTestParams -> stoch_params: {}'.format(message))
            return False, {'message': message}
        else:
            stoch_slowd_period_low = abs(int(str_stoch_slowd_period_low))

        if not str_stoch_slowd_period_up:
            message = 'Error: Not up slowd period of STOCH'
            logger.warning(
                'action trade_api -> CreateBackTestParams -> stoch_params: {}'.format(message))
            return False, {'message': message}
        else:
            stoch_slowd_period_up = abs(int(str_stoch_slowd_period_up))

        # evaluate buy thread params
        if not str_stoch_buy_thread_low:
            message = 'Error: Not low buy thread of STOCH'
            logger.warning(
                'action trade_api -> CreateBackTestParams -> stoch_params: {}'.format(message))
            return False, {'message': message}
        else:
            stoch_buy_thread_low = abs(int(str_stoch_buy_thread_low))

        if not str_stoch_buy_thread_up:
            message = 'Error: Not up buy thread of STOCH'
            logger.warning(
                'action trade_api -> CreateBackTestParams -> stoch_params: {}'.format(message))
            return False, {'message': message}
        else:
            stoch_buy_thread_up = abs(int(str_stoch_buy_thread_up))

        # evaluate sell thread params
        if not str_stoch_sell_thread_low:
            message = 'Error: Not low sell thread of STOCH'
            logger.warning(
                'action trade_api -> CreateBackTestParams -> stoch_params: {}'.format(message))
            return False, {'message': message}
        else:
            stoch_sell_thread_low = abs(int(str_stoch_sell_thread_low))

        if not str_stoch_sell_thread_up:
            message = 'Error: Not up sell thread of STOCH'
            logger.warning(
                'action trade_api -> CreateBackTestParams -> stoch_params: {}'.format(message))
            return False, {'message': message}
        else:
            stoch_sell_thread_up = abs(int(str_stoch_sell_thread_up))

        # compare large number of params
        if stoch_fastk_period_low > stoch_fastk_period_up:
            message = 'Error: low fastk period of STOCH is large more than up fastk period of STOCH'
            logger.warning(
                'action trade_api -> CreateBackTestParams -> stoch_params: {}'.format(message))
            return False, {'message': message}
        if stoch_slowk_period_low > stoch_slowk_period_up:
            message = 'Error: low slowk period of STOCH is large more than up slowk period of STOCH'
            logger.warning(
                'action trade_api -> CreateBackTestParams -> stoch_params: {}'.format(message))
            return False, {'message': message}
        if stoch_slowd_period_low > stoch_slowd_period_up:
            message = 'Error: low slowd period of STOCH is large more than up slowd period of STOCH'
            logger.warning(
                'action trade_api -> CreateBackTestParams -> stoch_params: {}'.format(message))
            return False, {'message': message}
        if stoch_buy_thread_low > stoch_buy_thread_up:
            message = 'Error: low buy thread of STOCH is large more than up buy thread of STOCH'
            logger.warning(
                'action trade_api -> CreateBackTestParams -> stoch_params: {}'.format(message))
            return False, {'message': message}
        if stoch_sell_thread_low > stoch_sell_thread_up:
            message = 'Error: low sell thread of STOCH is large more than up sell thread of STOCH'
            logger.warning(
                'action trade_api -> CreateBackTestParams -> stoch_params: {}'.format(message))
            return False, {'message': message}

        logger.info(
            'action trade_api\n'
            '<stoch-params>\n'
            'stoch_fastk_period_low: {}\n'
            'stoch_fastk_period_up: {}\n'
            'stoch_slowk_period_low: {}\n'
            'stoch_slowk_period_up: {}\n'
            'stoch_slowd_period_low :{}\n'
            'stoch_slowd_period_up :{}\n'
            'stoch_buy_thread_low :{}\n'
            'stoch_buy_thread_up :{}\n'
            'stoch_sell_thread_low :{}\n'
            'stoch_sell_thread_up :{}'.format(
                stoch_fastk_period_low, stoch_fastk_period_up,
                stoch_slowk_period_low, stoch_slowk_period_up,
                stoch_slowd_period_low, stoch_slowd_period_up,
                stoch_buy_thread_low, stoch_buy_thread_up,
                stoch_sell_thread_low, stoch_sell_thread_up))

        stoch_params = Dict2Obj(
            {'stoch1': stoch_fastk_period_low, 'stoch2': stoch_fastk_period_up,
             'stoch3': stoch_slowk_period_low, 'stoch4': stoch_slowk_period_up,
             'stoch5': stoch_slowd_period_low, 'stoch6': stoch_slowd_period_up,
             'stoch7': stoch_buy_thread_low, 'stoch8': stoch_buy_thread_up,
             'stoch9': stoch_sell_thread_low, 'stoch10': stoch_sell_thread_up})

        return True, stoch_params
