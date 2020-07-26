class StockGet {
    input() {
        $('#inputGet').on('click', function () {
            var stockcode = $('#inputCode').val();
            var duration = $('#inputDuration').val();
            if (stockcode == config.candlestick.stockcode) {
                config.candlestick.status = false
            }
            else {
                config.candlestick.status = true
                config.candlestick.stockcode = stockcode
            }
            config.candlestick.duration = duration
            send()
        })
    }
}

class Sma {
    input() {
        $('#inputSma').change(function () {
            if (this.checked === true) {
                config.sma.enable = true;
            } else {
                config.sma.enable = false;
            }
            send();
        });
        $("#inputSmaPeriod1").change(function () {
            config.sma.periods[0] = this.value;
            send();
        });
        $("#inputSmaPeriod2").change(function () {
            config.sma.periods[1] = this.value;
            send();
        });
        $("#inputSmaPeriod3").change(function () {
            config.sma.periods[2] = this.value;
            send();
        });
    }

    addColumns(data, dataTable) {
        for (var i = 0; i < data['smas'].length; i++) {
            var smaData = data['smas'][i];
            if (smaData.length == 0) { continue; }
            config.dataTable.index += 1;
            config.sma.indexes[i] = config.dataTable.index;
            dataTable.addColumn('number', 'SMA' + smaData["period"].toString());
            config.sma.values[i] = smaData["values"]
        }
    }

    addData(datas, i) {
        for (var j = 0; j < config.sma.values.length; j++) {
            if (config.sma.values[j][i] == 0) {
                datas.push(null);
            } else {
                datas.push(config.sma.values[j][i]);
            }
        }
    }

    drawChart(options, view) {
        for (var i = 0; i < config.sma.indexes.length; i++) {
            options.series[config.sma.indexes[i]] = { type: 'line' };
            view.columns.push(config.candlestick.numViews + config.sma.indexes[i]);
        }
    }
}

class Ema {
    input() {
        $('#inputEma').change(function () {
            if (this.checked === true) {
                config.ema.enable = true;
            } else {
                config.ema.enable = false;
            }
            send();
        });
        $("#inputEmaPeriod1").change(function () {
            config.ema.periods[0] = this.value;
            send();
        });
        $("#inputEmaPeriod2").change(function () {
            config.ema.periods[1] = this.value;
            send();
        });
        $("#inputEmaPeriod3").change(function () {
            config.ema.periods[2] = this.value;
            send();
        });
    }

    addColumns(data, dataTable) {
        for (var i = 0; i < data['emas'].length; i++) {
            var emaData = data['emas'][i];
            if (emaData.length == 0) { continue; }
            config.dataTable.index += 1;
            config.ema.indexes[i] = config.dataTable.index;
            dataTable.addColumn('number', 'EMA' + emaData["period"].toString());
            config.ema.values[i] = emaData["values"]
        }
    }

    addData(datas, i) {
        for (var j = 0; j < config.ema.values.length; j++) {
            if (config.ema.values[j][i] == 0) {
                datas.push(null);
            } else {
                datas.push(config.ema.values[j][i]);
            }
        }
    }

    drawChart(options, view) {
        for (var i = 0; i < config.ema.indexes.length; i++) {
            options.series[config.ema.indexes[i]] = { type: 'line' };
            view.columns.push(config.candlestick.numViews + config.ema.indexes[i]);
        }
    }
}

class BBands {
    input() {
        $('#inputBBands').change(function () {
            if (this.checked === true) {
                config.bbands.enable = true;
            } else {
                config.bbands.enable = false;
            }
            send();
        });
        $("#inputBBandsN").change(function () {
            config.bbands.n = this.value;
            send();
        });
        $("#inputBBandsK").change(function () {
            config.bbands.k = this.value;
            send();
        });
    }

    addColumns(data, dataTable) {
        var n = data['bbands']['n'];
        var k = data['bbands']['k'];
        var up = data['bbands']['up'];
        var mid = data['bbands']['mid'];
        var down = data['bbands']['down'];
        config.dataTable.index += 1;
        config.bbands.indexes[0] = config.dataTable.index;
        config.dataTable.index += 1;
        config.bbands.indexes[1] = config.dataTable.index;
        config.dataTable.index += 1;
        config.bbands.indexes[2] = config.dataTable.index;
        dataTable.addColumn('number', 'BBands Up(' + n + ',' + k + ')');
        dataTable.addColumn('number', 'BBands Mid(' + n + ',' + k + ')');
        dataTable.addColumn('number', 'BBands Down(' + n + ',' + k + ')');
        config.bbands.up = up;
        config.bbands.mid = mid;
        config.bbands.down = down;
    }

    addData(datas, i) {
        if (config.bbands.up[i] == 0) {
            datas.push(null);
        } else {
            datas.push(config.bbands.up[i]);
        }
        if (config.bbands.mid[i] == 0) {
            datas.push(null);
        } else {
            datas.push(config.bbands.mid[i]);
        }
        if (config.bbands.down[i] == 0) {
            datas.push(null);
        } else {
            datas.push(config.bbands.down[i]);
        }
    }

    drawChart(options, view) {
        for (var i = 0; i < config.bbands.indexes.length; i++) {
            options.series[config.bbands.indexes[i]] = {
                type: 'line',
                color: 'blue',
                lineWidth: 1
            };
            view.columns.push(config.candlestick.numViews + config.bbands.indexes[i])
        }
    }
}

class Ichimoku {
    input() {
        $('#inputIchimoku').change(function () {
            if (this.checked === true) {
                config.ichimoku.enable = true;
            } else {
                config.ichimoku.enable = false;
            }
            send();
        });
    }

    addColumns(data, dataTable) {
        var tenkan = data['ichimoku']['tenkan'];
        var kijun = data['ichimoku']['kijun'];
        var senkouA = data['ichimoku']['senkou_a'];
        var senkouB = data['ichimoku']['senkou_b'];
        var chikou = data['ichimoku']['chikou'];

        config.dataTable.index += 1;
        config.ichimoku.indexes[0] = config.dataTable.index;
        config.dataTable.index += 1;
        config.ichimoku.indexes[1] = config.dataTable.index;
        config.dataTable.index += 1;
        config.ichimoku.indexes[2] = config.dataTable.index;
        config.dataTable.index += 1;
        config.ichimoku.indexes[3] = config.dataTable.index;
        config.dataTable.index += 1;
        config.ichimoku.indexes[4] = config.dataTable.index;

        config.ichimoku.tenkan = tenkan;
        config.ichimoku.kijun = kijun;
        config.ichimoku.senkouA = senkouA;
        config.ichimoku.senkouB = senkouB;
        config.ichimoku.chikou = chikou;

        dataTable.addColumn('number', 'Tenkan');
        dataTable.addColumn('number', 'Kijun');
        dataTable.addColumn('number', 'SenkouA');
        dataTable.addColumn('number', 'SenkouB');
        dataTable.addColumn('number', 'Chikou');
    }

    addData(datas, i) {
        if (config.ichimoku.tenkan[i] == 0) {
            datas.push(null);
        } else {
            datas.push(config.ichimoku.tenkan[i]);
        }
        if (config.ichimoku.kijun[i] == 0) {
            datas.push(null);
        } else {
            datas.push(config.ichimoku.kijun[i]);
        }
        if (config.ichimoku.senkouA[i] == 0) {
            datas.push(null);
        } else {
            datas.push(config.ichimoku.senkouA[i]);
        }
        if (config.ichimoku.senkouB[i] == 0) {
            datas.push(null);
        } else {
            datas.push(config.ichimoku.senkouB[i]);
        }
        if (config.ichimoku.chikou[i] == 0) {
            datas.push(null);
        } else {
            datas.push(config.ichimoku.chikou[i]);
        }
    }

    drawChart(options, view) {
        for (var i = 0; i < config.ichimoku.indexes.length; i++) {
            options.series[config.ichimoku.indexes[i]] = {
                type: 'line',
                lineWidth: 1
            };
            view.columns.push(config.candlestick.numViews + config.ichimoku.indexes[i]);
        }
    }
}

class Volume {
    input() {
        $('#inputVolume').change(function () {
            if (this.checked === true) {
                config.volume.enable = true;
                drawChart(config.dataTable.value);
            } else {
                config.volume.enable = false;
                $('#volume_div').remove();
            }
        });
    }

    drawChart(charts) {
        if ($('#volume_div').length == 0) {
            $('#technical_div').append(
                "<div id='volume_div' class='bottom_chart'>" +
                "<span class='technical_title'>Volume</span>" +
                "<div id='volume_chart'></div>" +
                "</div>")
        }
        var volumeChart = new google.visualization.ChartWrapper({
            'chartType': 'ColumnChart',
            'containerId': 'volume_chart',
            'options': {
                'hAxis': { 'slantedText': false },
                'legend': { 'position': 'none' },
                'series': {}
            },
            'view': {
                'columns': [{ 'type': 'string' }, 5]
            }
        });
        charts.push(volumeChart)
    }
}

class Rsi {
    input() {
        $('#inputRsi').change(function () {
            if (this.checked === true) {
                config.rsi.enable = true;
            } else {
                config.rsi.enable = false;
                $('#rsi_div').remove();
            }
            send();
        });
        $("#inputRsiPeriod").change(function () {
            config.rsi.period = this.value;
            send();
        });
    }

    addColumns(data, dataTable) {
        config.dataTable.index += 1;
        config.rsi.indexes['up'] = config.dataTable.index;
        config.dataTable.index += 1;
        config.rsi.indexes['value'] = config.dataTable.index;
        config.dataTable.index += 1;
        config.rsi.indexes['down'] = config.dataTable.index;
        config.rsi.period = data['rsi']['period'];
        config.rsi.values = data['rsi']['values'];
        dataTable.addColumn('number', 'RSI Thread');
        dataTable.addColumn('number', 'RSI(' + config.rsi.period + ')');
        dataTable.addColumn('number', 'RSI Thread');
    }

    addData(datas, i) {
        datas.push(config.rsi.up);
        if (config.rsi.values[i] == 0) {
            datas.push(null);
        } else {
            datas.push(config.rsi.values[i]);
        }
        datas.push(config.rsi.down);
    }

    drawChart(charts) {
        if ($('#rsi_div').length == 0) {
            $('#technical_div').append(
                "<div id='rsi_div' class='bottom_chart'>" +
                "<span class='technical_title'>RSI</span>" +
                "<div id='rsi_chart'></div>" +
                "</div>")
        }
        var up = config.candlestick.numViews + config.rsi.indexes['up'];
        var value = config.candlestick.numViews + config.rsi.indexes['value'];
        var down = config.candlestick.numViews + config.rsi.indexes['down'];
        var rsiChart = new google.visualization.ChartWrapper({
            'chartType': 'LineChart',
            'containerId': 'rsi_chart',
            'options': {
                'hAxis': { 'slantedText': false },
                'legend': { 'position': 'none' },
                'series': {
                    0: { color: 'black', lineWidth: 1 },
                    1: { color: '#e2431e' },
                    2: { color: 'black', lineWidth: 1 }
                }
            },
            'view': {
                'columns': [{ 'type': 'string' }, up, value, down]
            }
        });
        charts.push(rsiChart)
    }
}

class Macd {
    input() {
        $('#inputMacd').change(function () {
            if (this.checked === true) {
                config.macd.enable = true;
            } else {
                $('#macd_div').remove();
                config.macd.enable = false;
            }
            send();
        });
        $("#inputMacdPeriod1").change(function () {
            config.macd.periods[0] = this.value;
            send();
        });
        $("#inputMacdPeriod2").change(function () {
            config.macd.periods[1] = this.value;
            send();
        });
        $("#inputMacdPeriod3").change(function () {
            config.macd.periods[2] = this.value;
            send();
        });
    }

    addColumns(data, dataTable) {
        var macdData = data['macd'];
        var fast_period = macdData["fast_period"].toString();
        var slow_period = macdData["slow_period"].toString();
        var signal_period = macdData["signal_period"].toString();
        var macd = macdData["macd"];
        var macd_signal = macdData["macd_signal"];
        var macd_hist = macdData["macd_hist"];

        config.dataTable.index += 1;
        config.macd.indexes[0] = config.dataTable.index;
        config.dataTable.index += 1;
        config.macd.indexes[1] = config.dataTable.index;
        config.dataTable.index += 1;
        config.macd.indexes[2] = config.dataTable.index;
        var speriods = '(' + fast_period + ',' + slow_period + ',' + signal_period + ')';
        dataTable.addColumn('number', 'MD' + speriods);
        dataTable.addColumn('number', 'MS' + speriods);
        dataTable.addColumn('number', 'HT' + speriods);
        config.macd.values[0] = macd;
        config.macd.values[1] = macd_signal;
        config.macd.values[2] = macd_hist;
        config.macd.periods[0] = fast_period;
        config.macd.periods[1] = slow_period;
        config.macd.periods[2] = signal_period;
    }

    addData(datas, i) {
        for (var j = 0; j < config.macd.values.length; j++) {
            if (config.macd.values[j][i] == 0) {
                datas.push(null);
            } else {
                datas.push(config.macd.values[j][i]);
            }
        }
    }

    drawChart(charts) {
        if (config.macd.indexes.length == 0) { return }
        if ($('#macd_div').length == 0) {
            $('#technical_div').append(
                "<div id='macd_div'>" +
                "<span class='technical_title'>MACD</span>" +
                "<div id='macd_chart'></div>" +
                "</div>")
        }
        var macdColumns = [{ 'type': 'string' }];

        macdColumns.push(config.candlestick.numViews + config.macd.indexes[2]);
        macdColumns.push(config.candlestick.numViews + config.macd.indexes[0]);
        macdColumns.push(config.candlestick.numViews + config.macd.indexes[1]);
        var macdChart = new google.visualization.ChartWrapper({
            'chartType': 'ComboChart',
            'containerId': 'macd_chart',
            'options': {
                legend: { 'position': 'none' },
                seriesType: "bars",
                series: {
                    1: { type: 'line', lineWidth: 1 },
                    2: { type: 'line', lineWidth: 1 }
                }
            },
            'view': {
                'columns': macdColumns
            }
        });
        charts.push(macdChart)
    }
}

class Willr {
    input() {
        $('#inputWillr').change(function () {
            if (this.checked === true) {
                config.willr.enable = true;
            } else {
                config.willr.enable = false;
                $('#willr_div').remove();
            }
            send();
        });
        $("#inputWillrPeriod").change(function () {
            config.willr.period = this.value;
            send();
        });
    }

    addColumns(data, dataTable) {
        config.dataTable.index += 1;
        config.willr.indexes['up'] = config.dataTable.index;
        config.dataTable.index += 1;
        config.willr.indexes['value'] = config.dataTable.index;
        config.dataTable.index += 1;
        config.willr.indexes['down'] = config.dataTable.index;
        config.willr.period = data['willr']['period'];
        config.willr.values = data['willr']['values'];
        dataTable.addColumn('number', '%R Thread');
        dataTable.addColumn('number', '%R(' + config.willr.period + ')');
        dataTable.addColumn('number', '%R Thread');
    }

    addData(datas, i) {
        datas.push(config.willr.up);
        if (config.willr.values[i] == 0) {
            datas.push(null);
        } else {
            datas.push(config.willr.values[i]);
        }
        datas.push(config.willr.down);
    }

    drawChart(charts) {
        if ($('#willr_div').length == 0) {
            $('#technical_div').append(
                "<div id='willr_div' class='bottom_chart'>" +
                "<span class='technical_title'>Williams%R</span>" +
                "<div id='willr_chart'></div>" +
                "</div>")
        }
        var up = config.candlestick.numViews + config.willr.indexes['up'];
        var value = config.candlestick.numViews + config.willr.indexes['value'];
        var down = config.candlestick.numViews + config.willr.indexes['down'];
        var willrChart = new google.visualization.ChartWrapper({
            'chartType': 'LineChart',
            'containerId': 'willr_chart',
            'options': {
                'hAxis': { 'slantedText': false },
                'legend': { 'position': 'none' },
                'series': {
                    0: { color: 'black', lineWidth: 1 },
                    1: { color: '#e2431e' },
                    2: { color: 'black', lineWidth: 1 }
                }
            },
            'view': {
                'columns': [{ 'type': 'string' }, up, value, down]
            }
        });
        charts.push(willrChart)
    }
}

class Stochf {
    input() {
        $('#inputStochf').change(function () {
            if (this.checked === true) {
                config.stochf.enable = true;
            } else {
                $('#stochf_div').remove();
                config.stochf.enable = false;
            }
            send();
        });
        $("#inputStochfPeriod1").change(function () {
            config.stochf.periods[0] = this.value;
            send();
        });
        $("#inputStochfPeriod2").change(function () {
            config.stochf.periods[1] = this.value;
            send();
        });
    }

    addColumns(data, dataTable) {
        var stochfData = data['stochf'];
        var fastk_period = stochfData["fastk_period"].toString();
        var fastd_period = stochfData["fastd_period"].toString();
        var fastk = stochfData["fastk"];
        var fastd = stochfData["fastd"];

        config.dataTable.index += 1;
        config.stochf.indexes['up'] = config.dataTable.index;
        config.dataTable.index += 1;
        config.stochf.indexes['value'][0] = config.dataTable.index;
        config.dataTable.index += 1;
        config.stochf.indexes['value'][1] = config.dataTable.index;
        config.dataTable.index += 1;
        config.stochf.indexes['down'] = config.dataTable.index;

        config.stochf.values[0] = fastk;
        config.stochf.values[1] = fastd;
        config.stochf.periods[0] = fastk_period;
        config.stochf.periods[1] = fastd_period;

        dataTable.addColumn('number', '%K_%D Thread');
        dataTable.addColumn('number', '%K(' + fastk_period + ')');
        dataTable.addColumn('number', '%D(' + fastd_period + ')');
        dataTable.addColumn('number', '%K_%D Thread');
    }

    addData(datas, i) {
        datas.push(config.stochf.up);
        for (var j = 0; j < config.stochf.values.length; j++) {
            if (config.stochf.values[j][i] == 0) {
                datas.push(null);
            } else {
                datas.push(config.stochf.values[j][i]);
            }
        }
        datas.push(config.stochf.down);
    }

    drawChart(charts) {
        if ($('#stochf_div').length == 0) {
            $('#technical_div').append(
                "<div id='stochf_div' class='bottom_chart'>" +
                "<span class='technical_title'>Fast Stochastic</span>" +
                "<div id='stochf_chart'></div>" +
                "</div>")
        }
        var up = config.candlestick.numViews + config.stochf.indexes['up'];
        var value_1 = config.candlestick.numViews + config.stochf.indexes['value'][0];
        var value_2 = config.candlestick.numViews + config.stochf.indexes['value'][1];
        var down = config.candlestick.numViews + config.stochf.indexes['down'];
        var stochfChart = new google.visualization.ChartWrapper({
            'chartType': 'LineChart',
            'containerId': 'stochf_chart',
            'options': {
                'hAxis': { 'slantedText': false },
                'legend': { 'position': 'none' },
                'series': {
                    0: { color: 'black', lineWidth: 1 },
                    1: { color: '#e2431e' },
                    2: { color: '#000080' },
                    3: { color: 'black', lineWidth: 1 }
                }
            },
            'view': {
                'columns': [{ 'type': 'string' }, up, value_1, value_2, down]
            }
        });
        charts.push(stochfChart)
    }
}

class Stoch {
    input() {
        $('#inputStoch').change(function () {
            if (this.checked === true) {
                config.stoch.enable = true;
            } else {
                $('#stoch_div').remove();
                config.stoch.enable = false;
            }
            send();
        });
        $("#inputStochPeriod1").change(function () {
            config.stoch.periods[0] = this.value;
            send();
        });
        $("#inputStochPeriod2").change(function () {
            config.stoch.periods[1] = this.value;
            send();
        });
        $("#inputStochPeriod3").change(function () {
            config.stoch.periods[2] = this.value;
            send();
        });
    }

    addColumns(data, dataTable) {
        var stochData = data['stoch'];
        var fastk_period = stochData["fastk_period"].toString();
        var slowk_period = stochData["slowk_period"].toString();
        var slowd_period = stochData["slowd_period"].toString();
        var slowk = stochData["slowk"];
        var slowd = stochData["slowd"];

        config.dataTable.index += 1;
        config.stoch.indexes['up'] = config.dataTable.index;
        config.dataTable.index += 1;
        config.stoch.indexes['value'][0] = config.dataTable.index;
        config.dataTable.index += 1;
        config.stoch.indexes['value'][1] = config.dataTable.index;
        config.dataTable.index += 1;
        config.stoch.indexes['down'] = config.dataTable.index;

        config.stoch.values[0] = slowk;
        config.stoch.values[1] = slowd;
        config.stoch.periods[0] = fastk_period;
        config.stoch.periods[1] = slowk_period;
        config.stoch.periods[2] = slowd_period;

        dataTable.addColumn('number', 'slow%K_slow%D Thread');
        dataTable.addColumn('number', 'slow%K(' + fastk_period + ',' + slowk_period + ',' + ')');
        dataTable.addColumn('number', 'slow%D(' + slowd_period + ')');
        dataTable.addColumn('number', 'slow%K_slow%D Thread');
    }

    addData(datas, i) {
        datas.push(config.stoch.up);
        for (var j = 0; j < config.stoch.values.length; j++) {
            if (config.stoch.values[j][i] == 0) {
                datas.push(null);
            } else {
                datas.push(config.stoch.values[j][i]);
            }
        }
        datas.push(config.stoch.down);
    }

    drawChart(charts) {
        if ($('#stoch_div').length == 0) {
            $('#technical_div').append(
                "<div id='stoch_div' class='bottom_chart'>" +
                "<span class='technical_title'>Slow Stochastic</span>" +
                "<div id='stoch_chart'></div>" +
                "</div>")
        }
        var up = config.candlestick.numViews + config.stoch.indexes['up'];
        var value_1 = config.candlestick.numViews + config.stoch.indexes['value'][0];
        var value_2 = config.candlestick.numViews + config.stoch.indexes['value'][1];
        var down = config.candlestick.numViews + config.stoch.indexes['down'];
        var stochChart = new google.visualization.ChartWrapper({
            'chartType': 'LineChart',
            'containerId': 'stoch_chart',
            'options': {
                'hAxis': { 'slantedText': false },
                'legend': { 'position': 'none' },
                'series': {
                    0: { color: 'black', lineWidth: 1 },
                    1: { color: '#e2431e' },
                    2: { color: '#000080' },
                    3: { color: 'black', lineWidth: 1 }
                }
            },
            'view': {
                'columns': [{ 'type': 'string' }, up, value_1, value_2, down]
            }
        });
        charts.push(stochChart)
    }
}