This is Webapplication which gets Japanese, America stockdata and conducts technical analysis.
implement the following,

1.Implementation and execution using Flask at local environment
2.Visualization and analysis of daily data
3.Technical analysis using Ta-Lib
 →Implement SMA,EMA,BBands,Ichimoku,RSI,MACD,William%R,FastStochastics,SlowStochastics
4.Implementation of backtest
　→Each parameter is optimized by backtest, a today sign of BUY or SELL is automated
 
backtest algorithm is following
a.basktest is conducted by using yesterday data and today data
b.if backtest is passed, a profit is eveluated by trading 'open price of next day'
※Only daily data and so this backtest is the algorithm of a, b

<How to executing>
・Please executing the following command in this repository
 - docker-compose up
※neccesary of docker install and some knowledge of docker

!!Caution!!
・Althoug you can conduct backtest by using any number, take time(3~4 minutes)
・When this webpage is opened with small window, web design may be collapsed
