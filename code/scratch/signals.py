"""Different Algos returning Buy, Sell, Short, Cover Signals in response to OHLCV Data"""

import pandas as pd

def moving_average(ohlcv, swindow=20, lwindow=50):
    sma = ohlcv.close.rolling(swindow).mean()
    lma = ohlcv.close.rolling(lwindow).mean()
    buy = sma > lma
    sell = sma < lma
    return buy, sell

def rsi(ohlcv, window=14, upper=70, lower=30):
    dup = ohlcv['close'].diff()
    ddown = ohlcv['close'].diff()
    dup[dup < 0] = 0
    ddown[ddown > 0] = 0
    upchange = dup.rolling(window).sum()
    downchange = ddown.rolling(window).sum()
    RS = upchange/abs(downchange)
    RSI = 100-(100/(1 + RS))
    sell = RSI > upper
    buy = RSI < lower
    return buy, sell

def evaluate(ohlcv, algo, params=None):
    if algo=='moving_average':
        if params:
            return moving_average(ohlcv, params['swindow'], params['lwindow'])
        return moving_average(ohlcv)
    elif algo=='rsi':
        if params:
            return rsi(ohlcv, params['window'], params['upper'], params['lower'])
        return rsi(ohlcv)
