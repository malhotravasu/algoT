"""Custom Backtesting Library from Scratch"""

import pandas as pd
from pandas import to_datetime

class Backtest(object):
    """Main Backtesting Object"""

    def __init__(self, ohlcv, start, end, ini_cash, ini_shares=0, freq=None):
        self.start = to_datetime(start)
        self.end = to_datetime(end)
        self.ohlcv = ohlcv.loc[start:end]
        self.ini_cash = ini_cash
        self.ini_shares = ini_shares
        self.curr_cash = ini_cash
        self.curr_shares = ini_shares

    # def _evaluate_signals(self, algo):
    #     pass
    #     self.signals = signals
    #     return signals

    def run_backtest(self, signals):
        # Run backtest
        # self._summarize(trades)
        # return self.summary()
        pass
        
    def _summarize(self, trades):
        """
        Summarizes the backtest
            report: (Dict with these Params)
                duration_analyzed
                number_of_trades
                simple_return
                remaining_cash
                owned_shares
                portfolio_value
        """
        summary = {}
        ini_portfolio = self.ini_cash + (self.ohlcv.loc[self.start]['Open'] * self.ini_shares)
        final_portfolio = self.curr_cash + (self.ohlcv.loc[self.end]['Close'] * self.curr_shares)

        summary['duration_analyzed'] = self.end - self.start
        summary['number_of_trades'] = len(trades)
        summary['simple_return'] = 100 * (final_portfolio - ini_portfolio) / ini_portfolio
        summary['remaining_cash'] = self.curr_cash
        summary['owned_shares'] = self.curr_shares
        summary['portfolio_value'] = final_portfolio
        self._summary = summary
        return summary

    def summary(self):
        if self._summary:
            return self._summary
        raise KeyError('Run the Algorithm first!')