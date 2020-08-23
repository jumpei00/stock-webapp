class StockGet {
    get() {
        $('#inputGet').on('click', function () {
            var stockcode = $('#inputCode').val();
            var duration = $('#inputDuration').val();
            if (stockcode == config.candlestick.stockcode) {
                config.candlestick.status = false
                config.candlestick.duration = duration
                send()
            }
            else {
                config.candlestick.status = true
                config.candlestick.stockcode = stockcode
                config.candlestick.duration = duration
                trade_config.trade.status = true
                send()
                trade()
            }
        })
    }
}

class BackTest {
    go() {
        $('#backtestGo').on('click', function () {
            var stockcode = $('#inputCode').val();
            var duration = $('#inputDuration').val();
            if (stockcode == config.candlestick.stockcode) {
                trade_config.trade.status = true
                trade_config.trade.backtest = true
                trade()
            }
            else {
                config.candlestick.status = true
                config.candlestick.stockcode = stockcode
                config.candlestick.duration = duration
                trade_config.trade.status = true
                trade_config.trade.backtest = true
                send()
                trade()
            }
        })
    }

    register() {
        $('#BackTestStockCode').text(trade_results.backtest.code);
        $('#BackTestDate').text(trade_results.backtest.date);
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
        $(document).on('change', '#tradeEma', function () {
            if (this.checked === true) {
                config.events.enable = true;
                config.events.ema.enable = true;
            }
            else {
                config.events.ema.enable = false;
                eventsEnable()
                $('#EmaNowProfit').text('')
            }
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

    addEventColums(data, dataTable) {
        var profit;
        config.dataTable.index += 1;
        config.events.ema.indexes[0] = config.dataTable.index;
        config.dataTable.index += 1;
        config.events.ema.indexes[1] = config.dataTable.index;
        config.events.index += 1;
        config.events.ema.index = config.events.index

        config.events.ema.values = data['events']['ema_event']['signals'];
        if (config.events.ema.values != undefined) {
            config.events.ema.first = config.events.ema.values.shift();
        }

        dataTable.addColumn('number', 'Marker');
        dataTable.addColumn({ type: 'string', role: 'annotation' });

        if (data['events']['ema_event']['profit'] != undefined) {
            profit = data['events']['ema_event']['profit']
            $('#EmaNowProfit').text(profit)
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

    addEventData(datas, candle) {
        var event = config.events.ema.first
        if (event == undefined) {
            datas.push(null);
            datas.push(null);
        }
        else if (event.signal_date == candle.date) {
            datas.push(candle.high);
            datas.push('(ema)' + event.side);
            config.events.ema.first = config.events.ema.values.shift();
        }
        else {
            datas.push(null);
            datas.push(null);
        }
    }

    drawChart(options, view) {
        for (var i = 0; i < config.ema.indexes.length; i++) {
            options.series[config.ema.indexes[i]] = { type: 'line' };
            view.columns.push(config.candlestick.numViews + config.ema.indexes[i]);
        }
    }

    drawEvents(options, view) {
        options.series[config.events.ema.indexes[0] - config.events.ema.index + 1] = {
            'type': 'line',
            tooltip: 'none',
            enableInteractivity: false,
            lineWidth: 0
        };
        view.columns.push(config.candlestick.numViews + config.events.ema.indexes[0]);
        view.columns.push(config.candlestick.numViews + config.events.ema.indexes[1]);
    }

    drawParams() {
        if (trade_results.backtest.enable == true) {
            if ($('#EmaParams').children('div').length == 2) {
                $('#EmaParams').prepend(
                    '<div id="EmaResults" class="alert alert-danger p-1 m-1" role="alert">' +
                    '[Results] Performace: <span id="EmaPerformance"></span><br>' +
                    '<span class="alert alert-dark p-1 m-1" role="alert">Short: <span id="EmaShort"></span></span>' +
                    '<span class="alert alert-dark p-1 m-1" role="alert">Long: <span id="EmaLong"></span></span>' +
                    '</div>'
                )
                $('#EmaEvents').append(
                    '<input id="tradeEma" type="checkbox">'
                )
            }
            $('#EmaPerformance').text(trade_results.backtest.ema.performance)
            $('#EmaShort').text(trade_results.backtest.ema.short_period)
            $('#EmaLong').text(trade_results.backtest.ema.long_period)
        }
        else if (trade_results.backtest.enable == false) {
            $('#EmaResults').remove()
            $('#tradeEma').remove()
        }
    }

    drawSignal() {
        var today_signal = trade_results.today.ema_trade
        if (today_signal == '') {
            $('#EmaSignal').text(today_signal)
        }
        else if (today_signal == 'NO_TRADE') {
            $('#EmaSignal').text(today_signal)
            $('#EmaSignal').addClass('text-success')
        }
        else if (today_signal == 'BUY') {
            $('#EmaSignal').text(today_signal)
            $('#EmaSignal').addClass('text-danger')
        }
        else if (today_signal == 'SELL') {
            $('#EmaSignal').text(today_signal)
            $('#EmaSignal').addClass('text-primary')
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
        $(document).on('change', '#tradeBBands', function () {
            if (this.checked === true) {
                config.events.enable = true;
                config.events.bbands.enable = true;
            }
            else {
                config.events.bbands.enable = false;
                eventsEnable()
                $('#BBandsNowProfit').text('')
            }
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

    addEventColums(data, dataTable) {
        var profit;
        config.dataTable.index += 1;
        config.events.bbands.indexes[0] = config.dataTable.index;
        config.dataTable.index += 1;
        config.events.bbands.indexes[1] = config.dataTable.index;
        config.events.index += 1;
        config.events.bbands.index = config.events.index

        config.events.bbands.values = data['events']['bb_event']['signals'];
        if (config.events.bbands.values != undefined) {
            config.events.bbands.first = config.events.bbands.values.shift();
        }

        dataTable.addColumn('number', 'Marker');
        dataTable.addColumn({ type: 'string', role: 'annotation' });

        if (data['events']['bb_event']['profit'] != undefined) {
            profit = data['events']['bb_event']['profit']
            $('#BBandsNowProfit').text(profit)
        }
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

    addEventData(datas, candle) {
        var event = config.events.bbands.first
        if (event == undefined) {
            datas.push(null);
            datas.push(null);
        }
        else if (event.signal_date == candle.date) {
            datas.push(candle.high);
            datas.push('(bb)' + event.side);
            config.events.bbands.first = config.events.bbands.values.shift();
        }
        else {
            datas.push(null);
            datas.push(null);
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

    drawEvents(options, view) {
        options.series[config.events.bbands.indexes[0] - config.events.bbands.index + 1] = {
            'type': 'line',
            tooltip: 'none',
            enableInteractivity: false,
            lineWidth: 0
        };
        view.columns.push(config.candlestick.numViews + config.events.bbands.indexes[0]);
        view.columns.push(config.candlestick.numViews + config.events.bbands.indexes[1]);
    }

    drawParams() {
        if (trade_results.backtest.enable == true) {
            if ($('#BBandsParams').children('div').length == 2) {
                $('#BBandsParams').prepend(
                    '<div id="BBandsResults" class="alert alert-danger p-1 m-1" role="alert">' +
                    '[Results] Performace: <span id="BBandsPerformance"></span><br>' +
                    '<span class="alert alert-dark p-1 m-1" role="alert">N: <span id="BBandsN"></span></span>' +
                    '<span class="alert alert-dark p-1 m-1" role="alert">K: <span id="BBandsK"></span></span>' +
                    '</div>'
                )
                $('#BBandsEvents').append(
                    '<input id="tradeBBands" type="checkbox">'
                )
            }
            $('#BBandsPerformance').text(trade_results.backtest.bbands.performance)
            $('#BBandsN').text(trade_results.backtest.bbands.n)
            $('#BBandsK').text(trade_results.backtest.bbands.k)
        }

        else if (trade_results.backtest.enable == false) {
            $('#BBandsResults').remove()
            $('#tradeBBands').remove()
        }
    }

    drawSignal() {
        var today_signal = trade_results.today.bb_trade
        if (today_signal == '') {
            $('#BBandsSignal').text(today_signal)
        }
        else if (today_signal == 'NO_TRADE') {
            $('#BBandsSignal').text(today_signal)
            $('#BBandsSignal').addClass('text-success')
        }
        else if (today_signal == 'BUY') {
            $('#BBandsSignal').text(today_signal)
            $('#BBandsSignal').addClass('text-danger')
        }
        else if (today_signal == 'SELL') {
            $('#BBandsSignal').text(today_signal)
            $('#BBandsSignal').addClass('text-primary')
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
        $(document).on('change', '#tradeIchimoku', function () {
            if (this.checked === true) {
                config.events.enable = true;
                config.events.ichimoku.enable = true;
            }
            else {
                config.events.ichimoku.enable = false;
                eventsEnable()
                $('#IchimokuNowProfit').text('')
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

    addEventColums(data, dataTable) {
        var profit;
        config.dataTable.index += 1;
        config.events.ichimoku.indexes[0] = config.dataTable.index;
        config.dataTable.index += 1;
        config.events.ichimoku.indexes[1] = config.dataTable.index;
        config.events.index += 1;
        config.events.ichimoku.index = config.events.index

        config.events.ichimoku.values = data['events']['ichimoku_event']['signals'];
        if (config.events.ichimoku.values != undefined) {
            config.events.ichimoku.first = config.events.ichimoku.values.shift();
        }

        dataTable.addColumn('number', 'Marker');
        dataTable.addColumn({ type: 'string', role: 'annotation' });

        if (data['events']['ichimoku_event']['profit'] != undefined) {
            profit = data['events']['ichimoku_event']['profit']
            $('#IchimokuNowProfit').text(profit)
        }
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

    addEventData(datas, candle) {
        var event = config.events.ichimoku.first
        if (event == undefined) {
            datas.push(null);
            datas.push(null);
        }
        else if (event.signal_date == candle.date) {
            datas.push(candle.high);
            datas.push('(ichi)' + event.side);
            config.events.ichimoku.first = config.events.ichimoku.values.shift();
        }
        else {
            datas.push(null);
            datas.push(null);
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

    drawEvents(options, view) {
        options.series[config.events.ichimoku.indexes[0] - config.events.ichimoku.index + 1] = {
            'type': 'line',
            tooltip: 'none',
            enableInteractivity: false,
            lineWidth: 0
        };
        view.columns.push(config.candlestick.numViews + config.events.ichimoku.indexes[0]);
        view.columns.push(config.candlestick.numViews + config.events.ichimoku.indexes[1]);
    }

    drawParams() {
        if (trade_results.backtest.enable == true) {
            if ($('#IchimokuParams').children('div').length == 0) {
                $('#IchimokuParams').append(
                    '<div id="IchimokuResults" class="alert alert-danger p-1 m-1" role="alert">' +
                    '[Results] Performace: <span id="ichimokuPerformance"></span>' +
                    '</div>'
                )
                $('#IchimokuEvents').append(
                    '<input id="tradeIchimoku" type="checkbox">'
                )
            }
            $('#ichimokuPerformance').text(trade_results.backtest.ichimoku.performance)
        }

        else if (trade_results.backtest.enable == false) {
            $('#IchimokuResults').remove()
            $('#tradeIchimoku').remove()
        }
    }

    drawSignal() {
        var today_signal = trade_results.today.ichimoku_trade
        if (today_signal == '') {
            $('#IchimokuSignal').text(today_signal)
        }
        else if (today_signal == 'NO_TRADE') {
            $('#IchimokuSignal').text(today_signal)
            $('#IchimokuSignal').addClass('text-success')
        }
        else if (today_signal == 'BUY') {
            $('#IchimokuSignal').text(today_signal)
            $('#IchimokuSignal').addClass('text-danger')
        }
        else if (today_signal == 'SELL') {
            $('#IchimokuSignal').text(today_signal)
            $('#IchimokuSignal').addClass('text-primary')
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
        $(document).on('change', '#tradeRsi', function () {
            if (this.checked === true) {
                config.events.enable = true;
                config.events.rsi.enable = true;
            }
            else {
                config.events.rsi.enable = false;
                eventsEnable()
                $('#RsiNowProfit').text('')
            }
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

    addEventColums(data, dataTable) {
        var profit;
        config.dataTable.index += 1;
        config.events.rsi.indexes[0] = config.dataTable.index;
        config.dataTable.index += 1;
        config.events.rsi.indexes[1] = config.dataTable.index;
        config.events.index += 1;
        config.events.rsi.index = config.events.index

        config.events.rsi.values = data['events']['rsi_event']['signals'];
        if (config.events.rsi.values != undefined) {
            config.events.rsi.first = config.events.rsi.values.shift();
        }

        dataTable.addColumn('number', 'Marker');
        dataTable.addColumn({ type: 'string', role: 'annotation' });

        if (data['events']['rsi_event']['profit'] != undefined) {
            profit = data['events']['rsi_event']['profit']
            $('#RsiNowProfit').text(profit)
        }
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

    addEventData(datas, candle) {
        var event = config.events.rsi.first
        if (event == undefined) {
            datas.push(null);
            datas.push(null);
        }
        else if (event.signal_date == candle.date) {
            datas.push(candle.high);
            datas.push('(rsi)' + event.side);
            config.events.rsi.first = config.events.rsi.values.shift();
        }
        else {
            datas.push(null);
            datas.push(null);
        }
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

    drawEvents(options, view) {
        options.series[config.events.rsi.indexes[0] - config.events.rsi.index + 1] = {
            'type': 'line',
            tooltip: 'none',
            enableInteractivity: false,
            lineWidth: 0
        };
        view.columns.push(config.candlestick.numViews + config.events.rsi.indexes[0]);
        view.columns.push(config.candlestick.numViews + config.events.rsi.indexes[1]);
    }

    drawParams() {
        if (trade_results.backtest.enable == true) {
            if ($('#RsiParams').children('div').length == 3) {
                $('#RsiParams').prepend(
                    '<div id="RsiResults" class="alert alert-danger p-1 m-1" role="alert">' +
                    '[Results] Performace: <span id="RsiPerfomance"></span><br>' +
                    '<span class="alert alert-dark p-1 m-1" role="alert">Period: <span id="RsiPeriod"></span></span>' +
                    '<span class="alert alert-dark p-1 m-1" role="alert">BuyThread: <span id="RsiBuyThread"></span></span>' +
                    '<span class="alert alert-dark p-1 m-1" role="alert">SellThread: <span id="RsiSellThread"></span></span>' +
                    '</div>'
                )
                $('#RsiEvents').append(
                    '<input id="tradeRsi" type="checkbox">'
                )
            }
            $('#RsiPerfomance').text(trade_results.backtest.rsi.performance)
            $('#RsiPeriod').text(trade_results.backtest.rsi.period)
            $('#RsiBuyThread').text(trade_results.backtest.rsi.buy_thread)
            $('#RsiSellThread').text(trade_results.backtest.rsi.sell_thread)
        }

        else if (trade_results.backtest.enable == false) {
            $('#RsiResults').remove()
            $('#tradeRsi').remove()
        }
    }

    drawSignal() {
        var today_signal = trade_results.today.rsi_trade
        if (today_signal == '') {
            $('#RsiSignal').text(today_signal)
        }
        else if (today_signal == 'NO_TRADE') {
            $('#RsiSignal').text(today_signal)
            $('#RsiSignal').addClass('text-success')
        }
        else if (today_signal == 'BUY') {
            $('#RsiSignal').text(today_signal)
            $('#RsiSignal').addClass('text-danger')
        }
        else if (today_signal == 'SELL') {
            $('#RsiSignal').text(today_signal)
            $('#RsiSignal').addClass('text-primary')
        }
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
        $(document).on('change', '#tradeMacd', function () {
            if (this.checked === true) {
                config.events.enable = true;
                config.events.macd.enable = true;
            }
            else {
                config.events.macd.enable = false;
                eventsEnable()
                $('#MacdNowProfit').text('')
            }
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

    addEventColums(data, dataTable) {
        var profit;
        config.dataTable.index += 1;
        config.events.macd.indexes[0] = config.dataTable.index;
        config.dataTable.index += 1;
        config.events.macd.indexes[1] = config.dataTable.index;
        config.events.index += 1;
        config.events.macd.index = config.events.index

        config.events.macd.values = data['events']['macd_event']['signals'];
        if (config.events.macd.values != undefined) {
            config.events.macd.first = config.events.macd.values.shift();
        }

        dataTable.addColumn('number', 'Marker');
        dataTable.addColumn({ type: 'string', role: 'annotation' });

        if (data['events']['macd_event']['profit'] != undefined) {
            profit = data['events']['macd_event']['profit']
            $('#MacdNowProfit').text(profit)
        }
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

    addEventData(datas, candle) {
        var event = config.events.macd.first
        if (event == undefined) {
            datas.push(null);
            datas.push(null);
        }
        else if (event.signal_date == candle.date) {
            datas.push(candle.high);
            datas.push('(macd)' + event.side);
            config.events.macd.first = config.events.macd.values.shift();
        }
        else {
            datas.push(null);
            datas.push(null);
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

    drawEvents(options, view) {
        options.series[config.events.macd.indexes[0] - config.events.macd.index + 1] = {
            'type': 'line',
            tooltip: 'none',
            enableInteractivity: false,
            lineWidth: 0
        };
        view.columns.push(config.candlestick.numViews + config.events.macd.indexes[0]);
        view.columns.push(config.candlestick.numViews + config.events.macd.indexes[1]);
    }

    drawParams() {
        if (trade_results.backtest.enable == true) {
            if ($('#MacdParams').children('div').length == 3) {
                $('#MacdParams').prepend(
                    '<div id="MacdResults" class="alert alert-danger p-1 m-1" role="alert">' +
                    '[Results] Performace: <span id="MacdPerformance"></span><br>' +
                    '<span class="alert alert-dark p-1 m-1" role="alert">FastPeriod: <span id="MacdFast"></span></span>' +
                    '<span class="alert alert-dark p-1 m-1" role="alert">SlowPeriod: <span id="MacdSlow"></span></span>' +
                    '<span class="alert alert-dark p-1 m-1" role="alert">SignalPeriod: <span id="MacdSignalPeriod"></span></span>' +
                    '</div>'
                )
                $('#MacdEvents').append(
                    '<input id="tradeMacd" type="checkbox">'
                )
            }
            $('#MacdPerformance').text(trade_results.backtest.macd.performance)
            $('#MacdFast').text(trade_results.backtest.macd.fast_period)
            $('#MacdSlow').text(trade_results.backtest.macd.slow_period)
            $('#MacdSignalPeriod').text(trade_results.backtest.macd.signal_period)
        }

        else if (trade_results.backtest.enable == false) {
            $('#MacdResults').remove()
            $('#tradeMacd').remove()
        }
    }

    drawSignal() {
        var today_signal = trade_results.today.macd_trade
        if (today_signal == '') {
            $('#MacdSignal').text(today_signal)
        }
        else if (today_signal == 'NO_TRADE') {
            $('#MacdSignal').text(today_signal)
            $('#MacdSignal').addClass('text-success')
        }
        else if (today_signal == 'BUY') {
            $('#MacdSignal').text(today_signal)
            $('#MacdSignal').addClass('text-danger')
        }
        else if (today_signal == 'SELL') {
            $('#MacdSignal').text(today_signal)
            $('#MacdSignal').addClass('text-primary')
        }
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
        $(document).on('change', '#tradeWillr', function () {
            if (this.checked === true) {
                config.events.enable = true;
                config.events.willr.enable = true;
            }
            else {
                config.events.willr.enable = false;
                eventsEnable()
                $('#WillrNowProfit').text('')
            }
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

    addEventColums(data, dataTable) {
        var profit;
        config.dataTable.index += 1;
        config.events.willr.indexes[0] = config.dataTable.index;
        config.dataTable.index += 1;
        config.events.willr.indexes[1] = config.dataTable.index;
        config.events.index += 1;
        config.events.willr.index = config.events.index

        config.events.willr.values = data['events']['willr_event']['signals'];
        if (config.events.willr.values != undefined) {
            config.events.willr.first = config.events.willr.values.shift();
        }

        dataTable.addColumn('number', 'Marker');
        dataTable.addColumn({ type: 'string', role: 'annotation' });

        if (data['events']['willr_event']['profit'] != undefined) {
            profit = data['events']['willr_event']['profit']
            $('#WillrNowProfit').text(profit)
        }
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

    addEventData(datas, candle) {
        var event = config.events.willr.first
        if (event == undefined) {
            datas.push(null);
            datas.push(null);
        }
        else if (event.signal_date == candle.date) {
            datas.push(candle.high);
            datas.push('(wr)' + event.side);
            config.events.willr.first = config.events.willr.values.shift();
        }
        else {
            datas.push(null);
            datas.push(null);
        }
    }

    drawChart(charts) {
        if ($('#willr_div').length == 0) {
            1
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

    drawEvents(options, view) {
        options.series[config.events.willr.indexes[0] - config.events.willr.index + 1] = {
            'type': 'line',
            tooltip: 'none',
            enableInteractivity: false,
            lineWidth: 0
        };
        view.columns.push(config.candlestick.numViews + config.events.willr.indexes[0]);
        view.columns.push(config.candlestick.numViews + config.events.willr.indexes[1]);
    }

    drawParams() {
        if (trade_results.backtest.enable == true) {
            if ($('#WillrParams').children('div').length == 3) {
                $('#WillrParams').prepend(
                    '<div id="WillrResults" class="alert alert-danger p-1 m-1" role="alert">' +
                    '[Results] Performace: <span id="WillrPerformance"></span><br>' +
                    '<span class="alert alert-dark p-1 m-1" role="alert">Period: <span id="WillrPeriod"></span></span>' +
                    '<span class="alert alert-dark p-1 m-1" role="alert">BuyThread: <span id="WillrBuyThread"></span></span>' +
                    '<span class="alert alert-dark p-1 m-1" role="alert">SellThread: <span id="WillrSellThread"></span></span>' +
                    '</div>'
                )
                $('#WillrEvents').append(
                    '<input id="tradeWillr" type="checkbox">'
                )
            }
            $('#WillrPerformance').text(trade_results.backtest.willr.performance)
            $('#WillrPeriod').text(trade_results.backtest.willr.period)
            $('#WillrBuyThread').text(trade_results.backtest.willr.buy_thread)
            $('#WillrSellThread').text(trade_results.backtest.willr.sell_thread)
        }

        else if (trade_results.backtest.enable == false) {
            $('#WillrResults').remove()
            $('#tradeWillr').remove()
        }
    }

    drawSignal() {
        var today_signal = trade_results.today.willr_trade
        if (today_signal == '') {
            $('#WillrSignal').text(today_signal)
        }
        else if (today_signal == 'NO_TRADE') {
            $('#WillrSignal').text(today_signal)
            $('#WillrSignal').addClass('text-success')
        }
        else if (today_signal == 'BUY') {
            $('#WillrSignal').text(today_signal)
            $('#WillrSignal').addClass('text-danger')
        }
        else if (today_signal == 'SELL') {
            $('#WillrSignal').text(today_signal)
            $('#WillrSignal').addClass('text-primary')
        }
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
        $(document).on('change', '#tradeStochf', function () {
            if (this.checked === true) {
                config.events.enable = true;
                config.events.stochf.enable = true;
            }
            else {
                config.events.stochf.enable = false;
                eventsEnable()
                $('#StochfNowProfit').text('')
            }
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

    addEventColums(data, dataTable) {
        var profit;
        config.dataTable.index += 1;
        config.events.stochf.indexes[0] = config.dataTable.index;
        config.dataTable.index += 1;
        config.events.stochf.indexes[1] = config.dataTable.index;
        config.events.index += 1;
        config.events.stochf.index = config.events.index

        config.events.stochf.values = data['events']['stochf_event']['signals'];
        if (config.events.stochf.values != undefined) {
            config.events.stochf.first = config.events.stochf.values.shift();
        }

        dataTable.addColumn('number', 'Marker');
        dataTable.addColumn({ type: 'string', role: 'annotation' });

        if (data['events']['stochf_event']['profit'] != undefined) {
            profit = data['events']['stochf_event']['profit']
            $('#StochfNowProfit').text(profit)
        }
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

    addEventData(datas, candle) {
        var event = config.events.stochf.first
        if (event == undefined) {
            datas.push(null);
            datas.push(null);
        }
        else if (event.signal_date == candle.date) {
            datas.push(candle.high);
            datas.push('(stcf)' + event.side);
            config.events.stochf.first = config.events.stochf.values.shift();
        }
        else {
            datas.push(null);
            datas.push(null);
        }
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

    drawEvents(options, view) {
        options.series[config.events.stochf.indexes[0] - config.events.stochf.index + 1] = {
            'type': 'line',
            tooltip: 'none',
            enableInteractivity: false,
            lineWidth: 0
        };
        view.columns.push(config.candlestick.numViews + config.events.stochf.indexes[0]);
        view.columns.push(config.candlestick.numViews + config.events.stochf.indexes[1]);
    }

    drawParams() {
        if (trade_results.backtest.enable == true) {
            if ($('#StochfParams').children('div').length == 1) {
                $('#StochfParams').prepend(
                    '<div id="StochfResults" class="alert alert-danger p-1 m-1" role="alert">' +
                    '[Results] Performace: <span id="StochfPerformance"></span><br>' +
                    '<span class="alert alert-dark p-1 m-1" role="alert">FastkPeriod: <span id="StochfFastk"></span></span>' +
                    '<span class="alert alert-dark p-1 m-1" role="alert">FastdPeriod: <span id="StochfFastd"></span></span>' +
                    '<span class="alert alert-dark p-1 m-1" role="alert">BuyThread: <span id="StochfBuyThread"></span></span>' +
                    '<span class="alert alert-dark p-1 m-1" role="alert">SellThread: <span id="StochfSellThread"></span></span>' +
                    '</div>'
                )
                $('#StochfEvents').append(
                    '<input id="tradeStochf" type="checkbox">'
                )
            }
            $('#StochfPerformance').text(trade_results.backtest.stochf.performance)
            $('#StochfFastk').text(trade_results.backtest.stochf.fastk_period)
            $('#StochfFastd').text(trade_results.backtest.stochf.fastd_period)
            $('#StochfBuyThread').text(trade_results.backtest.stochf.buy_thread)
            $('#StochfSellThread').text(trade_results.backtest.stochf.sell_thread)
        }

        else if (trade_results.backtest.enable == false) {
            $('#StochfResults').remove()
            $('#tradeStochf').remove()
        }
    }

    drawSignal() {
        var today_signal = trade_results.today.stochf_trade
        if (today_signal == '') {
            $('#StochfSignal').text(today_signal)
        }
        else if (today_signal == 'NO_TRADE') {
            $('#StochfSignal').text(today_signal)
            $('#StochfSignal').addClass('text-success')
        }
        else if (today_signal == 'BUY') {
            $('#StochfSignal').text(today_signal)
            $('#StochfSignal').addClass('text-danger')
        }
        else if (today_signal == 'SELL') {
            $('#StochfSignal').text(today_signal)
            $('#StochfSignal').addClass('text-primary')
        }
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
        $(document).on('change', '#tradeStoch', function () {
            if (this.checked === true) {
                config.events.enable = true;
                config.events.stoch.enable = true;
            }
            else {
                config.events.stoch.enable = false;
                eventsEnable()
                $('#StochNowProfit').text('')
            }
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

    addEventColums(data, dataTable) {
        var profit;
        config.dataTable.index += 1;
        config.events.stoch.indexes[0] = config.dataTable.index;
        config.dataTable.index += 1;
        config.events.stoch.indexes[1] = config.dataTable.index;
        config.events.index += 1;
        config.events.stoch.index = config.events.index

        config.events.stoch.values = data['events']['stoch_event']['signals'];
        if (config.events.stoch.values != undefined) {
            config.events.stoch.first = config.events.stoch.values.shift();
        }

        dataTable.addColumn('number', 'Marker');
        dataTable.addColumn({ type: 'string', role: 'annotation' });

        if (data['events']['stoch_event']['profit'] != undefined) {
            profit = data['events']['stoch_event']['profit']
            $('#StochNowProfit').text(profit)
        }
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

    addEventData(datas, candle) {
        var event = config.events.stoch.first
        if (event == undefined) {
            datas.push(null);
            datas.push(null);
        }
        else if (event.signal_date == candle.date) {
            datas.push(candle.high);
            datas.push('(stc)' + event.side);
            config.events.stoch.first = config.events.stoch.values.shift();
        }
        else {
            datas.push(null);
            datas.push(null);
        }
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

    drawEvents(options, view) {
        options.series[config.events.stoch.indexes[0] - config.events.stoch.index + 1] = {
            'type': 'line',
            tooltip: 'none',
            enableInteractivity: false,
            lineWidth: 0
        };
        view.columns.push(config.candlestick.numViews + config.events.stoch.indexes[0]);
        view.columns.push(config.candlestick.numViews + config.events.stoch.indexes[1]);
    }

    drawParams() {
        if (trade_results.backtest.enable == true) {
            if ($('#StochParams').children('div').length == 1) {
                $('#StochParams').prepend(
                    '<div id="StochResults" class="alert alert-danger p-1 m-1" role="alert">' +
                    '[Results] Performace: <span id="StochPerformance"></span><br>' +
                    '<div class="mb-1">' +
                    '<span class="alert alert-dark p-1 m-1" role="alert">FastkPeriod: <span id="StochFastk"></span></span>' +
                    '<span class="alert alert-dark p-1 m-1" role="alert">SlowkPeriod: <span id="StochSlowk"></span></span>' +
                    '<span class="alert alert-dark p-1 m-1" role="alert">SlowdPeriod: <span id="StochSlowd"></span></span>' +
                    '</div>' +
                    '<div class="mt-2">' +
                    '<span class="alert alert-dark p-1 m-1" role="alert">BuyThread: <span id="StochBuyThread"></span></span>' +
                    '<span class="alert alert-dark p-1 m-1" role="alert">SellThread: <span id="StochSellThread"></span></span>' +
                    '</div>' +
                    '</div>'
                )
                $('#StochEvents').append(
                    '<input id="tradeStoch" type="checkbox">'
                )
            }
            $('#StochPerformance').text(trade_results.backtest.stoch.performance)
            $('#StochFastk').text(trade_results.backtest.stoch.fastk_period)
            $('#StochSlowk').text(trade_results.backtest.stoch.slowk_period)
            $('#StochSlowd').text(trade_results.backtest.stoch.slowd_period)
            $('#StochBuyThread').text(trade_results.backtest.stoch.buy_thread)
            $('#StochSellThread').text(trade_results.backtest.stoch.sell_thread)
        }

        else if (trade_results.backtest.enable == false) {
            $('#StochResults').remove()
            $('#tradeStoch').remove()
        }
    }

    drawSignal() {
        var today_signal = trade_results.today.stoch_trade
        if (today_signal == '') {
            $('#StochSignal').text(today_signal)
        }
        else if (today_signal == 'NO_TRADE') {
            $('#StochSignal').text(today_signal)
            $('#StochSignal').addClass('text-success')
        }
        else if (today_signal == 'BUY') {
            $('#StochSignal').text(today_signal)
            $('#StochSignal').addClass('text-danger')
        }
        else if (today_signal == 'SELL') {
            $('#StochSignal').text(today_signal)
            $('#StochSignal').addClass('text-primary')
        }
    }
}