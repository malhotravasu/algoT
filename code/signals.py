"""Different Algos returning Buy, Sell, Short, Cover Signals in response to OHLCV Data"""

def moving_average(ohlcv, params = None):

    if params:
        swindow = params["swindow"]
        lwindow = params["lwindow"]
    else:
        swindow = 20
        lwindow = 50

    sma = ohlcv.close.rolling(swindow).mean()
    lma = ohlcv.close.rolling(lwindow).mean()

    buy = sma > lma
    sell = sma < lma
    return (buy, sell)

def rsi(ohlcv, params=None):

    if params:
        window = params["window"]
        upper = params["upper"]
        lower = params["lower"]
    else:
        window = 14
        upper = 75
        lower = 25
    
    dup = ohlcv['close'].diff()
    ddown = ohlcv['close'].diff()
    dup[dup < 0] = 0
    ddown[ddown > 0] = 0
    upchange = dup.rolling(window).sum()
    downchange = ddown.rolling(window).sum()
    RS = upchange/abs(downchange)
    RSI = 100-(100/(1 + RS))
    
    buy = RSI <= lower
    sell = RSI >= upper
    return (buy, sell)

def evaluate(ohlcv, algo, params=None):
    if algo == 'moving_average':
        if params:
            return moving_average(ohlcv, params)
        return moving_average(ohlcv)
    
    elif algo == 'rsi':
        if params:
            return rsi(ohlcv, params)
        return rsi(ohlcv)
