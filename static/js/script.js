google.charts.load('current', { 'packages': ['corechart', 'controls'] });

var config = {
    stock_code: {
        default: 'VOO'
    }
}

function send_to_webserver() {
    var params = {
        "stock_code": config.stock_code.default
    }

    $.get("/candle", params).done(function (data) {
        var dataTable = new google.visualization.DataTable();
        var google_chart_data = [];
        var candles = data['candles'];

        for (var i = 0; i < candles.length; i++) {
            var candle = candles[i];
            var date = new Date(candle.date);
            var datas = [date, candle.low, candle.open, candle.close, candle.high, candle.volume];
            google_chart_data.push(datas)
        }

        dataTable.addColumn('date', 'Date');
        dataTable.addColumn('number', 'Low');
        dataTable.addColumn('number', 'Open');
        dataTable.addColumn('number', 'Close');
        dataTable.addColumn('number', 'High');
        dataTable.addColumn('number', 'Volume');
        dataTable.addRows(google_chart_data);
        drawChart(dataTable);
    })
}

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

window.onload = function () {
    send_to_webserver()
}