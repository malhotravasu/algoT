"""Different Algos returning Buy, Sell, Short, Cover Signals in response to OHLCV Data"""

from pykalman import KalmanFilter
import pandas as pd

def moving_average(ohlcv, params = None):

    if params:
        swindow = params["swindow"]
        lwindow = params["lwindow"]
    else:
        swindow = 30
        lwindow = 60

    sma = ohlcv.close.rolling(swindow).mean()
    lma = ohlcv.close.rolling(lwindow).mean()

    buy = sma > lma
    sell = sma < lma
    return (buy, sell)

def kalman(ohlcv):
    kf = KalmanFilter(
                        transition_matrices = [1],
                        observation_matrices = [1],
                        initial_state_mean = 0,
                        initial_state_covariance = 1,
                        observation_covariance=1,
                        transition_covariance=.01
                     )
    x = ohlcv["close"]
    state_means, _ = kf.filter(x.values)
    state_means = pd.Series(state_means.flatten(), index=x.index)

    sma = state_means.rolling(window = 30).mean()
    lma = state_means.rolling(window = 60).mean()
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
    
    elif algo == 'kalman':
        return kalman(ohlcv)
