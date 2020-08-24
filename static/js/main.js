var stock = new StockGet()
var backtest = new BackTest()
var sma = new Sma()
var ema = new Ema()
var bbands = new BBands()
var ichimoku = new Ichimoku()
var volume = new Volume()
var rsi = new Rsi()
var macd = new Macd()
var willr = new Willr()
var stochf = new Stochf()
var stoch = new Stoch()

// send to webserver by using ajax
function send() {
    // decide to params for sending by GET methods
    var params = {
        "status": config.candlestick.status,
        "stockcode": config.candlestick.stockcode,
        "duration": config.candlestick.duration
    }

    if (config.sma.enable == true) {
        params["sma"] = true;
        params["smaPeriod1"] = config.sma.periods[0];
        params["smaPeriod2"] = config.sma.periods[1];
        params["smaPeriod3"] = config.sma.periods[2];
    }

    if (config.ema.enable == true) {
        params["ema"] = true;
        params["emaPeriod1"] = config.ema.periods[0];
        params["emaPeriod2"] = config.ema.periods[1];
        params["emaPeriod3"] = config.ema.periods[2];
    }

    if (config.bbands.enable == true) {
        params["bbands"] = true;
        params["bbandsN"] = config.bbands.n;
        params["bbandsK"] = config.bbands.k;
    }

    if (config.ichimoku.enable == true) {
        params["ichimoku"] = true;
    }

    if (config.rsi.enable == true) {
        params["rsi"] = true;
        params["rsiPeriod"] = config.rsi.period;
    }

    if (config.macd.enable == true) {
        params["macd"] = true;
        params["macdPeriod1"] = config.macd.periods[0];
        params["macdPeriod2"] = config.macd.periods[1];
        params["macdPeriod3"] = config.macd.periods[2];
    }

    if (config.willr.enable == true) {
        params["willr"] = true;
        params["willrPeriod"] = config.willr.period;
    }

    if (config.stochf.enable == true) {
        params["stochf"] = true;
        params["stochfPeriod1"] = config.stochf.periods[0];
        params["stochfPeriod2"] = config.stochf.periods[1];
    }

    if (config.stoch.enable == true) {
        params["stoch"] = true;
        params["stochPeriod1"] = config.stoch.periods[0];
        params["stochPeriod2"] = config.stoch.periods[1];
        params["stochPeriod3"] = config.stoch.periods[2];
    }

    if (config.events.enable == true) {
        params["events"] = true;
        params["EmaEventsEnable"] = config.events.ema.enable;
        params["BBandsEventsEnable"] = config.events.bbands.enable;
        params["IchimokuEventsEnable"] = config.events.ichimoku.enable;
        params["RsiEventsEnable"] = config.events.rsi.enable;
        params["MacdEventsEnable"] = config.events.macd.enable;
        params["WillrEventsEnable"] = config.events.willr.enable;
        params["StochfEventsEnable"] = config.events.stochf.enable;
        params["StochEventsEnable"] = config.events.stoch.enable;
    }

    // ajax(methods is GET)
    $.get("/candle", params).done(function (data) {
        initConfigValues();
        var dataTable = new google.visualization.DataTable();
        // add columns of candles
        dataTable.addColumn('date', 'Date');
        dataTable.addColumn('number', 'Low');
        dataTable.addColumn('number', 'Open');
        dataTable.addColumn('number', 'Close');
        dataTable.addColumn('number', 'High');
        dataTable.addColumn('number', 'Volume');
        var googleChartData = [];
        var candles = data['candles'];

        // add columns of indicators
        if (data["smas"] != undefined) {
            sma.addColumns(data, dataTable);
        }

        if (data["emas"] != undefined) {
            ema.addColumns(data, dataTable);
        }

        if (data['bbands'] != undefined) {
            bbands.addColumns(data, dataTable);
        }

        if (data['ichimoku'] != undefined) {
            ichimoku.addColumns(data, dataTable)
        }

        if (data['events'] != undefined) {
            if (data['events']['ema_event'] != undefined) {
                ema.addEventColums(data, dataTable)
            }
            if (data['events']['bb_event'] != undefined) {
                bbands.addEventColums(data, dataTable)
            }
            if (data['events']['ichimoku_event'] != undefined) {
                ichimoku.addEventColums(data, dataTable)
            }
            if (data['events']['rsi_event'] != undefined) {
                rsi.addEventColums(data, dataTable)
            }
            if (data['events']['macd_event'] != undefined) {
                macd.addEventColums(data, dataTable)
            }
            if (data['events']['willr_event'] != undefined) {
                willr.addEventColums(data, dataTable)
            }
            if (data['events']['stochf_event'] != undefined) {
                stochf.addEventColums(data, dataTable)
            }
            if (data['events']['stoch_event'] != undefined) {
                stoch.addEventColums(data, dataTable)
            }
        }

        if (data['rsi'] != undefined) {
            rsi.addColumns(data, dataTable)
        }

        if (data['macd'] != undefined) {
            macd.addColumns(data, dataTable)
        }

        if (data['willr'] != undefined) {
            willr.addColumns(data, dataTable)
        }

        if (data['stochf'] != undefined) {
            stochf.addColumns(data, dataTable)
        }

        if (data['stoch'] != undefined) {
            stoch.addColumns(data, dataTable)
        }

        // add datas of candles and indicators
        for (var i = 0; i < candles.length; i++) {
            var candle = candles[i];
            var date = new Date(candle.date);
            // add candles data
            var datas = [date, candle.low, candle.open, candle.close, candle.high, candle.volume];

            // add indicators
            if (data["smas"] != undefined) {
                sma.addData(datas, i)
            }

            if (data["emas"] != undefined) {
                ema.addData(datas, i)
            }

            if (data["bbands"] != undefined) {
                bbands.addData(datas, i)
            }

            if (data["ichimoku"] != undefined) {
                ichimoku.addData(datas, i)
            }

            if (data["events"] != undefined) {
                if (data['events']['ema_event'] != undefined) {
                    ema.addEventData(datas, candle)
                }
                if (data['events']['bb_event'] != undefined) {
                    bbands.addEventData(datas, candle)
                }
                if (data['events']['ichimoku_event'] != undefined) {
                    ichimoku.addEventData(datas, candle)
                }
                if (data['events']['rsi_event'] != undefined) {
                    rsi.addEventData(datas, candle)
                }
                if (data['events']['macd_event'] != undefined) {
                    macd.addEventData(datas, candle)
                }
                if (data['events']['willr_event'] != undefined) {
                    willr.addEventData(datas, candle)
                }
                if (data['events']['stochf_event'] != undefined) {
                    stochf.addEventData(datas, candle)
                }
                if (data['events']['stoch_event'] != undefined) {
                    stoch.addEventData(datas, candle)
                }
            }

            if (data["rsi"] != undefined) {
                rsi.addData(datas, i)
            }

            if (data["macd"] != undefined) {
                macd.addData(datas, i)
            }

            if (data["willr"] != undefined) {
                willr.addData(datas, i)
            }

            if (data["stochf"] != undefined) {
                stochf.addData(datas, i)
            }

            if (data["stoch"] != undefined) {
                stoch.addData(datas, i)
            }

            googleChartData.push(datas);
        }

        dataTable.addRows(googleChartData);
        drawChart(dataTable);
    })
}

// draw charts
function drawChart(dataTable) {
    var chartDiv = document.getElementById('chart_div');
    var charts = [];
    var dashboard = new google.visualization.Dashboard(chartDiv);
    var mainChart = new google.visualization.ChartWrapper({
        chartType: 'ComboChart',
        containerId: 'chart_div',
        options: {
            hAxis: { 'slantedText': false },
            legend: { 'position': 'none' },
            candlestick: {
                fallingColor: { strokeWidth: 0, fill: '#a52714' },
                risingColor: { strokeWidth: 0, fill: '#0f9d58' }
            },
            seriesType: "candlesticks",
            series: {}
        },
        view: {
            columns: [
                {
                    calc: function (d, rowIndex) {
                        return d.getFormattedValue(rowIndex, 0);
                    },
                    type: 'string'

                }, 1, 2, 3, 4
            ]

        }
    });
    charts.push(mainChart);
    var options = mainChart.getOptions();
    var view = mainChart.getView();

    // draw indicators
    if (config.sma.enable == true) {
        sma.drawChart(options, view)
    }

    if (config.ema.enable == true) {
        ema.drawChart(options, view)
    }

    if (config.bbands.enable == true) {
        bbands.drawChart(options, view)
    }

    if (config.ichimoku.enable == true) {
        ichimoku.drawChart(options, view)
    }

    if (config.volume.enable == true) {
        volume.drawChart(charts)
    }

    if (config.rsi.enable == true) {
        rsi.drawChart(charts)
    }

    if (config.macd.enable == true) {
        macd.drawChart(charts)
    }

    if (config.willr.enable == true) {
        willr.drawChart(charts)
    }

    if (config.stochf.enable == true) {
        stochf.drawChart(charts)
    }

    if (config.stoch.enable == true) {
        stoch.drawChart(charts)
    }

    if (config.events.enable == true) {
        if (config.events.ema.enable == true && config.events.ema.indexes.length > 0) {
            ema.drawEvents(options, view)
        }
        if (config.events.bbands.enable == true && config.events.bbands.indexes.length > 0) {
            bbands.drawEvents(options, view)
        }
        if (config.events.ichimoku.enable == true && config.events.ichimoku.indexes.length > 0) {
            ichimoku.drawEvents(options, view)
        }
        if (config.events.rsi.enable == true && config.events.rsi.indexes.length > 0) {
            rsi.drawEvents(options, view)
        }
        if (config.events.macd.enable == true && config.events.macd.indexes.length > 0) {
            macd.drawEvents(options, view)
        }
        if (config.events.willr.enable == true && config.events.willr.indexes.length > 0) {
            willr.drawEvents(options, view)
        }
        if (config.events.stochf.enable == true && config.events.stochf.indexes.length > 0) {
            stochf.drawEvents(options, view)
        }
        if (config.events.stoch.enable == true && config.events.stoch.indexes.length > 0) {
            stoch.drawEvents(options, view)
        }
    }

    var controlWrapper = new google.visualization.ControlWrapper({
        'controlType': 'ChartRangeFilter',
        'containerId': 'filter_div',
        'options': {
            'filterColumnIndex': 0,
            'ui': {
                'chartType': 'LineChart',
                'chartView': {
                    'columns': [0, 4]
                }
            }
        }
    });

    dashboard.bind(controlWrapper, charts);
    dashboard.draw(dataTable);
}

// backtest
function trade() {
    var params = {
        "status": config.candlestick.status,
        "stockcode": config.candlestick.stockcode,
        "trade": trade_config.trade.status,
        "backtest": trade_config.trade.backtest
    }

    if (params["backtest"] == true) {
        params["emaBacktest1"] = $('#inputEMAShortPeriod1').val();
        params["emaBacktest2"] = $('#inputEMAShortPeriod2').val();
        params["emaBacktest3"] = $('#inputEMALongPeriod1').val();
        params["emaBacktest4"] = $('#inputEMALongPeriod2').val();

        params["bbandsBacktest1"] = $('#inputBBandsNPeriod1').val();
        params["bbandsBacktest2"] = $('#inputBBandsNPeriod2').val();
        params["bbandsBacktest3"] = $('#inputBBandsKPeriod1').val();
        params["bbandsBacktest4"] = $('#inputBBandsKPeriod2').val();

        params["rsiBacktest1"] = $('#inputRsiPeriod1').val();
        params["rsiBacktest2"] = $('#inputRsiPeriod2').val();
        params["rsiBacktest3"] = $('#inputRsiBuyThread1').val();
        params["rsiBacktest4"] = $('#inputRsiBuyThread2').val();
        params["rsiBacktest5"] = $('#inputRsiSellThread1').val();
        params["rsiBacktest6"] = $('#inputRsiSellThread2').val();

        params["macdBacktest1"] = $('#inputMacdFastPeriod1').val();
        params["macdBacktest2"] = $('#inputMacdFastPeriod2').val();
        params["macdBacktest3"] = $('#inputMacdSlowPeriod1').val();
        params["macdBacktest4"] = $('#inputMacdSlowPeriod2').val();
        params["macdBacktest5"] = $('#inputMacdSignalPeriod1').val();
        params["macdBacktest6"] = $('#inputMacdSignalPeriod2').val();
        
        params["willrBacktest1"] = $('#inputWillrPeriod1').val();
        params["willrBacktest2"] = $('#inputWillrPeriod2').val();
        params["willrBacktest3"] = $('#inputWillrBuyThread1').val();
        params["willrBacktest4"] = $('#inputWillrBuyThread2').val();
        params["willrBacktest5"] = $('#inputWillrSellThread1').val();
        params["willrBacktest6"] = $('#inputWillrSellThread2').val();

        params["stochfBacktest1"] = $('#inputStochfFastkPeriod1').val();
        params["stochfBacktest2"] = $('#inputStochfFastkPeriod2').val();
        params["stochfBacktest3"] = $('#inputStochfFastdPeriod1').val();
        params["stochfBacktest4"] = $('#inputStochfFastdPeriod2').val();
        params["stochfBacktest5"] = $('#inputStochfBuyThread1').val();
        params["stochfBacktest6"] = $('#inputStochfBuyThread2').val();
        params["stochfBacktest7"] = $('#inputStochfSellThread1').val();
        params["stochfBacktest8"] = $('#inputStochfSellThread2').val();
        
        params["stochBacktest1"] = $('#inputStochFastkPeriod1').val();
        params["stochBacktest2"] = $('#inputStochFastkPeriod2').val();
        params["stochBacktest3"] = $('#inputStochSlowkPeriod1').val();
        params["stochBacktest4"] = $('#inputStochSlowkPeriod2').val();
        params["stochBacktest5"] = $('#inputStochSlowdPeriod1').val();
        params["stochBacktest6"] = $('#inputStochSlowdPeriod2').val();
        params["stochBacktest7"] = $('#inputStochBuyThread1').val();
        params["stochBacktest8"] = $('#inputStochBuyThread2').val();
        params["stochBacktest9"] = $('#inputStochSellThread1').val();
        params["stochBacktest10"] = $('#inputStochSellThread2').val();
    }

    $.get("/trade", params).done(function (data) {
        initTradeConfigValues()

        if (data['params'] != undefined) {
            trade_results.backtest.enable = true;
            trade_results.backtest.code = data['params']['code'];
            trade_results.backtest.date = data['params']['date'];

            trade_results.backtest.ema.performance = data['params']['ema_performance'];
            trade_results.backtest.ema.short_period = data['params']['ema_short_period'];
            trade_results.backtest.ema.long_period = data['params']['ema_long_period'];

            trade_results.backtest.bbands.performance = data['params']['bb_performance'];
            trade_results.backtest.bbands.n = data['params']['bb_n'];
            trade_results.backtest.bbands.k = data['params']['bb_k'];

            trade_results.backtest.ichimoku.performance = data['params']['ichimoku_performance'];

            trade_results.backtest.rsi.performance = data['params']['rsi_performance'];
            trade_results.backtest.rsi.period = data['params']['rsi_period'];
            trade_results.backtest.rsi.buy_thread = data['params']['rsi_buy_thread'];
            trade_results.backtest.rsi.sell_thread = data['params']['rsi_sell_thread'];

            trade_results.backtest.macd.performance = data['params']['macd_performance'];
            trade_results.backtest.macd.fast_period = data['params']['macd_fast_period'];
            trade_results.backtest.macd.slow_period = data['params']['macd_slow_period'];
            trade_results.backtest.macd.signal_period = data['params']['macd_signal_period'];

            trade_results.backtest.willr.performance = data['params']['willr_performance'];
            trade_results.backtest.willr.period = data['params']['willr_period'];
            trade_results.backtest.willr.buy_thread = data['params']['willr_buy_thread'];
            trade_results.backtest.willr.sell_thread = data['params']['willr_sell_thread'];

            trade_results.backtest.stochf.performance = data['params']['stochf_performance'];
            trade_results.backtest.stochf.fastk_period = data['params']['stochf_fastk_period'];
            trade_results.backtest.stochf.fastd_period = data['params']['stochf_fastd_period'];
            trade_results.backtest.stochf.buy_thread = data['params']['stochf_buy_thread'];
            trade_results.backtest.stochf.sell_thread = data['params']['stochf_sell_thread'];

            trade_results.backtest.stoch.performance = data['params']['stoch_performance'];
            trade_results.backtest.stoch.fastk_period = data['params']['stoch_fastk_period'];
            trade_results.backtest.stoch.slowk_period = data['params']['stoch_slowk_period'];
            trade_results.backtest.stoch.slowd_period = data['params']['stoch_slowd_period'];
            trade_results.backtest.stoch.buy_thread = data['params']['stoch_buy_thread'];
            trade_results.backtest.stoch.sell_thread = data['params']['stoch_sell_thread'];
        }

        if (data['trade'] != undefined) {
            trade_results.today.ema_trade = data['trade']['ema_trade'];
            trade_results.today.bb_trade = data['trade']['bb_trade'];
            trade_results.today.ichimoku_trade = data['trade']['ichimoku'];
            trade_results.today.rsi_trade = data['trade']['rsi_trade'];
            trade_results.today.macd_trade = data['trade']['macd_trade'];
            trade_results.today.willr_trade = data['trade']['willr_trade'];
            trade_results.today.stochf_trade = data['trade']['stochf_trade'];
            trade_results.today.stoch_trade = data['trade']['stoch_trade'];
        }

        drawTrade()
    })
}

function drawTrade() {
    backtest.register();
    ema.drawParams();
    bbands.drawParams();
    ichimoku.drawParams();
    rsi.drawParams();
    macd.drawParams();
    willr.drawParams();
    stochf.drawParams();
    stoch.drawParams();

    ema.drawSignal();
    bbands.drawSignal();
    ichimoku.drawSignal();
    rsi.drawSignal();
    macd.drawSignal();
    willr.drawSignal();
    stochf.drawSignal();
    stoch.drawSignal();
    
    tradeResultsReset()
}

// monitoring checkboxes and textboxes 
window.onload = function () {
    send();
    trade();
    stock.get();
    backtest.go();
    sma.input();
    ema.input();
    bbands.input();
    ichimoku.input();
    volume.input();
    rsi.input();
    macd.input();
    willr.input();
    stochf.input();
    stoch.input();
}