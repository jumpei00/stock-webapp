日本株・米株のデータを取得しテクニカル分析を行うウェブアプリとなっています。  
以下の点を実装しています。    

１.Flaskを用いたローカル環境での実装、実行  
2.日足データの可視化(グラフ化)、分析  
3.Ta-Libを用いたテクニカル分析  
　→SMA,EMA,BBands,Ichimoku,RSI,MACD,William%R,FastStochastics,SlowStochasticsを実装しています  
4.バックテストの実装  
　→バックテストで各パラメーターの最適化を行い、当日の売り買いのサインを自動化しました。    

バックテストのアルゴリズムは以下のようになっています。  
a.前日と当日のデータを元にしてテスト  
b.バックテストに合格した場合は「翌日の始値」を売買することで利益を評価  
※日足データのみしかないためこのようなアルゴリズムにしています    

＜実行方法＞  
このレポジトリの中で以下のコマンドを打ちます  
　- docker-compose up  
※dockerのインストール、dockerの多少の知識が必要です    

！！注意点！！  
・バックテストは任意の数字でテスト可能ですが、時間がかかります(3〜4分程度)  
・小さいウィンドウで開くとデザインが崩れる可能性があります      


This is Webapplication which gets Japanese, America stockdata and conducts technical analysis.  
implement the following,    

1.Implementation and execution using Flask at local environment  
2.Visualization and analysis of daily data  
3.Technical analysis using Ta-Lib  
 →Implement SMA,EMA,BBands,Ichimoku,RSI,MACD,William%R,FastStochastics,SlowStochastics  
4.Implementation of backtest  
 →Each parameter is optimized by backtest, a today sign of BUY or SELL is automated    
 
・backtest algorithm is following  
a.basktest is conducted by using yesterday data and today data  
b.if backtest is passed, a profit is eveluated by trading 'open price of next day'  
※Only daily data and so this backtest is the algorithm of a, b    

・How to executing  
Please executing the following command in this repository  
※neccesary of docker install and some knowledge of docker  
 - docker-compose up  


!!Caution!!  
・Althoug you can conduct backtest by using any number, take time(3~4 minutes)  
・When this webpage is opened with small window, web design may be collapsed  
