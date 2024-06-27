import pandas as pd
import yfinance as yf
import ta
import pandas_ta
import talib
import re
from discord import SyncWebhook
from myBot import url
class indicator():
    name=''
    min=max=0
    value=0.0
    def __init__(self,name,min,max):
        self.name = name 
        self.min = min 
        self.max = max
    def set_value(self,value):
        self.value = value

def simple_ma(df, days):
    df['MA' + str(days)] = talib.MA(df['Close'], timeperiod=days).iloc[-1]

def exp_ma(df, days):
    df['EMA' + str(days)] = talib.EMA(df['Close'], timeperiod=days).iloc[-1]

def sort_helper(indicator,buy,sell,neutral):
    if re.match(r'E?MA\d',indicator.name):
        if indicator.value < indicator.min:
            buy.append(indicator.name)
        elif indicator.value > indicator.max:
            sell.append(indicator.name)
        else:
            neutral.append(indicator.name)
    else:
        if indicator.value < indicator.min:
            sell.append(indicator.name)
        elif indicator.value > indicator.max:
            buy.append(indicator.name)
        else:
            neutral.append(indicator.name)

def main():
    # init vars
    ticker = 'TSM'
    # tickers = ['TSM','AAPL','GME',]
    # tickers = ['PLTR','GOOG','SRPT','AREB']
    # for ticker in tickers:
    print(ticker)
    buy = []
    sell = []
    neutral = []
    ma_values = [5,10,20,50,100,200]
    # download stock info
    df = yf.download(ticker, period='max', interval='1d', progress=False)
    cp_df = yf.download(ticker, period='1d', interval='1m', progress=False)
    cp = cp_df['Close'].iloc[-1]
    # instantiate indicators
    indicators = [
        indicator('rsi',40,50),
        indicator('stoch',45,55),
        indicator('stochrsi',45,55),
        indicator('macd',0,0),
        indicator('willr',-60,-35),
        indicator('cci',-50,50),
        indicator('ultosc',50,50),
        indicator('roc',0,0),
    ]
    for i in ma_values:
        indicators.append(indicator('MA' + str(i),cp,cp))
    for i in ma_values:
        indicators.append(indicator('EMA' + str(i),cp,cp))
    # calculate indicators
    indicators[0].set_value(talib.RSI(df['Close']).iloc[-1])
    stoch_k,stoch_d = talib.STOCH(df['High'], df['Low'], df['Close'], fastk_period=9, slowd_period=6)
    # stoch = stoch_k.iloc[-1] + stoch_d.iloc[-1]
    indicators[1].set_value(stoch_k.iloc[-1])
    stochrsi_k,stochrsi_d = talib.STOCHRSI(df['Close'])
    indicators[2].set_value(stochrsi_d.iloc[-1])
    indicators[3].set_value(ta.trend.MACD(close=df['Close'], window_slow=26, window_fast=12).macd().iloc[-1])
    indicators[4].set_value(talib.WILLR(df['High'], df['Low'], df['Close']).iloc[-1])
    indicators[5].set_value(talib.CCI(df['High'], df['Low'], df['Close'], timeperiod=14).iloc[-1])
    indicators[6].set_value(talib.ULTOSC(df['High'], df['Low'], df['Close']).iloc[-1])
    indicators[7].set_value(talib.ROC(df['Close'],timeperiod=14).iloc[-1])
    for _, (i,ma_value) in enumerate(zip(range(8,8+len(ma_values)),ma_values)):
        indicators[i].set_value(talib.MA(df['Close'], timeperiod=ma_value).iloc[-1])
    for _, (i,ma_value) in enumerate(zip(range(14,14+len(ma_values)),ma_values)):
        indicators[i].set_value(talib.EMA(df['Close'], timeperiod=ma_value).iloc[-1])    
    # examine for buy/sell indicators
    for i in indicators:
        sort_helper(i,buy,sell,neutral)
    # print results
    # for i in indicators:
    #     if i.name.__contains__('stoch'):
    #         print(i.name, i.value)
    file=open('trend.txt','r')
    with open('trend.txt','r') as f:
        contents = f.read()
    if 'sell' in contents and len(buy) >= len(indicators)-3:
        with open('trend.txt', 'w') as f:
            f.write('buy')
            webhook = SyncWebhook.from_url(url)
            webhook.send(ticker + ": strong buy")
    elif 'buy' in contents and len(sell) >= len(indicators)-3:
        with open('trend.txt', 'w') as f:
            f.write('sell')
            webhook = SyncWebhook.from_url(url)
            webhook.send(ticker + ": strong sell")
        # if len(buy) == len(indicators):
        #     results = 'Strong buy'
        # elif len(sell) == len(indicators):
        #     results = 'Strong sell'
    print(
f"""    
buy: {buy}
sell: {sell}
neutral: {neutral}
"""
    )
        # pd.set_option('float_format', '{:f}'.format)
        # print(ticker)
        # print('----------------------------')
        # print(df.iloc[-1].drop(['Open', 'Close', 'High', 'Low', 'Adj Close', 'Volume']))

if __name__ == '__main__':
    main()
# TODO
# bear/bull
# highs/lows
# adx/dmi+/dmi-
        # indicators[4].set_value(talib.ADX(df['High'],df['Low'],df['Close'], timeperiod=30).iloc[-1])
# stochrsi/stoch
