google.charts.load('current', { 'packages': ['corechart', 'controls'] });

var config = {
    candlestick: {
        status: true,
        stockcode: 'VOO',
        duration: '365',
        numViews: 5,
    },
    dataTable: {
        index: 0,
        value: null
    },
    sma: {
        enable: false,
        indexes: [],
        periods: [],
        values: []
    },
    ema: {
        enable: false,
        indexes: [],
        periods: [],
        values: []
    },
    bbands: {
        enable: false,
        indexes: [],
        n: 20,
        k: 2,
        up: [],
        mid: [],
        down: []
    },
    ichimoku: {
        enable: false,
        indexes: [],
        tenkan: [],
        kijun: [],
        senkouA: [],
        senkouB: [],
        chikou: []
    },
    volume: {
        enable: false,
        index: [],
        values: []
    },
    rsi: {
        enable: false,
        indexes: { 'up': 0, 'value': 0, 'down': 0 },
        period: 14,
        up: 70,
        values: [],
        down: 30
    },
    macd: {
        enable: false,
        indexes: [],
        periods: [],
        values: []
    },
    willr: {
        enable: false,
        indexes: { 'up': 0, 'value': 0, 'down': 0 },
        period: 14,
        up: -30,
        values: [],
        down: -70
    },
    stochf: {
        enable: false,
        indexes: { 'up': 0, 'value': [], 'down': 0 },
        periods: [],
        up: 70,
        values: [],
        down: 30
    },
    stoch: {
        enable: false,
        indexes: { 'up': 0, 'value': [], 'down': 0 },
        periods: [],
        up: 70,
        values: [],
        down: 30
    },
    events: {
        enable: false,
        index: 0,
        ema: {
            enable: false,
            index: 0,
            indexes: [],
            values: [],
            first: null
        },
        bbands: {
            enable: false,
            index: 0,
            indexes: [],
            values: [],
            first: null
        },
        ichimoku: {
            enable: false,
            index: 0,
            indexes: [],
            values: [],
            first: null
        },
        rsi: {
            enable: false,
            index: 0,
            indexes: [],
            values: [],
            first: null
        },
        macd: {
            enable: false,
            index: 0,
            indexes: [],
            values: [],
            first: null
        },
        willr: {
            enable: false,
            index: 0,
            indexes: [],
            values: [],
            first: null
        },
        stochf: {
            enable: false,
            index: 0,
            indexes: [],
            values: [],
            first: null
        },
        stoch: {
            enable: false,
            index: 0,
            indexes: [],
            values: [],
            first: null
        }
    }
};

var trade_config = {
    trade: {
        status: true,
        backtest: false
    }
}

var trade_results = {
    backtest: {
        enable: false,
        code: '',
        date: '',
        ema: {
            performance: 100,
            short_period: 0,
            long_period: 0
        },
        bbands: {
            performance: 100,
            n: 0,
            k: 0
        },
        ichimoku: {
            performance: 100,
        },
        rsi: {
            performance: 100,
            period: 0,
            buy_thread: 0,
            sell_thread: 0
        },
        macd: {
            performance: 100,
            fast_period: 0,
            slow_period: 0,
            signal_period: 0
        },
        willr: {
            performance: 100,
            period: 0,
            buy_thread: 0,
            sell_thread: 0
        },
        stochf: {
            performance: 100,
            fastk_period: 0,
            fastd_period: 0,
            buy_thread: 0,
            sell_thread: 0
        },
        stoch: {
            performance: 100,
            fastk_period: 0,
            slowk_period: 0,
            slowd_perod: 0,
            buy_thread: 0,
            sell_thread: 0,
        }
    },
    today: {
        ema_trade: '',
        bb_trade: '',
        ichimoku_trade: '',
        rsi_trade: '',
        macd_trade: '',
        willr_trade: '',
        stochf_trade: '',
        stoch_trade: ''
    }
}

function initConfigValues() {
    config.candlestick.status = false;
    config.dataTable.index = 0;
    config.sma.indexes = [];
    config.sma.values = [];
    config.ema.indexes = [];
    config.ema.values = [];
    config.bbands.indexes = [];
    config.bbands.up = [];
    config.bbands.mid = [];
    config.bbands.down = [];
    config.ichimoku.indexes = [];
    config.ichimoku.tenkan = [];
    config.ichimoku.kijun = [];
    config.ichimoku.senkouA = [];
    config.ichimoku.senkouB = [];
    config.ichimoku.chikou = [];
    config.volume.index = [];
    config.rsi.indexes = [];
    config.macd.indexes = [];
    config.macd.periods = [];
    config.macd.values = [];
    config.willr.values = [];
    config.stochf.periods = [];
    config.stochf.values = [];
    config.stoch.periods = [];
    config.stoch.values = [];
    config.events.index = 0;
    config.events.ema.index = 0;
    config.events.ema.indexes = [];
    config.events.ema.values = [];
    config.events.bbands.index = 0;
    config.events.bbands.indexes = [];
    config.events.bbands.values = [];
    config.events.ichimoku.index = 0;
    config.events.ichimoku.indexes = [];
    config.events.ichimoku.values = [];
    config.events.rsi.index = 0;
    config.events.rsi.indexes = [];
    config.events.rsi.values = [];
    config.events.macd.index = 0;
    config.events.macd.indexes = [];
    config.events.macd.values = [];
    config.events.willr.index = 0;
    config.events.willr.indexes = [];
    config.events.willr.values = [];
    config.events.stochf.index = 0;
    config.events.stochf.indexes = [];
    config.events.stochf.values = [];
    config.events.stoch.index = 0;
    config.events.stoch.indexes = [];
    config.events.stoch.values = [];
}

function initTradeConfigValues() {
    trade_config.trade.status = false;
    trade_config.trade.backtest = false;
}

function tradeResultsReset() {
    trade_results.backtest.enable = false
    trade_results.backtest.code = ''
    trade_results.backtest.date = ''
    trade_results.backtest.ema.performance = 0
    trade_results.backtest.ema.short_period = 0
    trade_results.backtest.ema.long_period = 0
    trade_results.backtest.bbands.performance = 0
    trade_results.backtest.bbands.n = 0
    trade_results.backtest.bbands.k = 0
    trade_results.backtest.ichimoku.performance = 0
    trade_results.backtest.rsi.performance = 0
    trade_results.backtest.rsi.period = 0
    trade_results.backtest.rsi.buy_thread = 0
    trade_results.backtest.rsi.sell_thread = 0
    trade_results.backtest.macd.performance = 0
    trade_results.backtest.macd.fast_period = 0
    trade_results.backtest.macd.slow_period = 0
    trade_results.backtest.macd.signal_period = 0
    trade_results.backtest.willr.performance = 0
    trade_results.backtest.willr.period = 0
    trade_results.backtest.willr.buy_thread = 0
    trade_results.backtest.willr.sell_thread = 0
    trade_results.backtest.stochf.performance = 0
    trade_results.backtest.stochf.fastk_period = 0
    trade_results.backtest.stochf.fastd_period = 0
    trade_results.backtest.stochf.buy_thread = 0
    trade_results.backtest.stochf.sell_thread = 0
    trade_results.backtest.stoch.performance = 0
    trade_results.backtest.stoch.fastk_period = 0
    trade_results.backtest.stoch.slowk_period = 0
    trade_results.backtest.stoch.slowd_period = 0
    trade_results.backtest.stoch.buy_thread = 0
    trade_results.backtest.stoch.sell_thread = 0
    trade_results.today.ema_trade = ''
    trade_results.today.bb_trade = ''
    trade_results.today.ichimoku_trade = ''
    trade_results.today.rsi_trade = ''
    trade_results.today.macd_trade = ''
    trade_results.today.willr_trade = ''
    trade_results.today.stochf_trade = ''
    trade_results.today.stoch_trade = ''
}

function eventsEnable() {
    if (config.events.ema.enable == true ||
        config.events.bbands.enable == true ||
        config.events.ichimoku.enable == true ||
        config.events.rsi.enable == true ||
        config.events.macd.enable == true ||
        config.events.willr.enable == true ||
        config.events.stochf.enable == true ||
        config.events.stoch.enable == true) {
        config.events.enable = true
    }
    else {
        config.events.enable = false
    }
}