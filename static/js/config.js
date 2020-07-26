google.charts.load('current', { 'packages': ['corechart', 'controls'] });

var config = {
    candlestick: {
        status: true,
        stockcode: '1570',
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
};

function initConfigValues() {
    config.candlestick.status = false
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
}