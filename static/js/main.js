var stock = new StockGet()
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

// monitoring checkboxes and textboxes 
window.onload = function () {
    send();
    stock.input();
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