import pandas as pd
import time
from pandas import to_datetime

class Backtest(object):
    """Main Backtesting Object"""

    def __init__(self, ohlcv, ini_cash, fin_cash, ini_shares, fin_shares, freq, start, end):
        self.ohlcv = ohlcv
        self.start = to_datetime(start)
        self.end = to_datetime(end)
        self.ini_cash = ini_cash
        self.ini_shatres = ini_shares
        self.ohlcv = ohlcv.loc[start:end]

    # def _evaluate_signals(self, algo):
    #     pass
    #     self.signals = signals
    #     return signals
    
    def run_backtest(self, signals):
        # Trades: {index:'datetime, type:'b,s,s,c', number:'', price:''}
        self.trades = trades
        return summarize(trades)
    
    def summarize(self, trades):
        """
        Summarizes the backtest
            report: (Dict with these Params)
                duration_analyzed
                trades_analyzed
                simple_return
                cash
                share_value
                portfolio_value
                number_of_trades
        """
        summary = {}
        summary['duration_analyzed'] = self.end - self.start
        summary['number_of_trades'] = len(trades)
        self.summary = summary
        return summary

    def get_summary(self):
        return self.summary
        