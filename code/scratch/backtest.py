"""Custom Backtesting Library from Scratch"""

import pandas as pd
from pandas import to_datetime
from signals import evaluate


class Backtest(object):
    """Main Backtesting Object"""

    def __init__(self, ohlcv, ini_cash, start=None, end=None, ini_shares=0, algo=None, params=None):
        """
        Backtest object constructor:
        params:
            algo: Preferred algo (moving_average, rsi, etc)
        """
        start = to_datetime(start)
        end = to_datetime(end)
        if start:
            self.start = self.get_closest_stamp(ohlcv.index, start, pd.Timedelta(days=1), 'start')
        else:
            self.start = ohlcv.index.min()
        if end:
            self.end = self.get_closest_stamp(ohlcv.index, end, pd.Timedelta(days=1), 'end')
        else:
            self.end = ohlcv.index.max()

        # Initialising Data
        if isinstance(ohlcv, pd.DataFrame):
            self.ohlcv = ohlcv.loc[self.start:self.end].copy()
        elif isinstance(ohlcv, str) and ohlcv=='default':
            pass # Set self.ohlcv to Default Data Bundle (To be decided later)

        # Immutable Trading variable
        self.ini_cash = ini_cash
        self.ini_shares = ini_shares

        # Mutable Trading variable
        self.curr_cash = ini_cash
        self.curr_shares = ini_shares
        
        # Algo goes here
        if algo:
            if params:
                self.buy, self.sell = evaluate(self.ohlcv, algo, params)
            else:
                self.buy, self.sell = evaluate(self.ohlcv, algo)

    def run_backtest(self, number, buy=None, sell=None):
        """ Run backtest here """
        self.reset()
        ohlcv = self.ohlcv
        ohlcv['buy'] = buy if buy else self.buy
        ohlcv['sell'] = sell if sell else self.sell
        trades = []
        delta = pd.Timedelta(days=1) #  To be replace with a state variable 
        for index, row in ohlcv[(ohlcv['buy'] == True) | (ohlcv['sell'] == True)].iterrows():
            if index == self.end:
                continue
            else:
                trade = {}
                trade['timestamp'] = index
                trade['share_price'] = row['close']
                if(row['buy']):
                    self.curr_shares += number
                    self.curr_cash -= number * (ohlcv.loc[self.get_closest_stamp(self.ohlcv.index, index, delta)]['open'])
                    trade['owned_shares'] = self.curr_shares
                    trade['remaining_cash'] = self.curr_cash
                    trade['type'] = 'buy'
                elif(row['sell']):
                    self.curr_shares -= number
                    self.curr_cash += number * (ohlcv.loc[self.get_closest_stamp(self.ohlcv.index, index, delta)]['open'])
                    trade['owned_shares'] = self.curr_shares
                    trade['remaining_cash'] = self.curr_cash
                    trade['type'] = 'sell'
                trades.append(trade)
        trades_df = pd.DataFrame(trades).set_index('timestamp') # Convert to pandas DataFrame
        return self._summarize(trades_df)

    def _summarize(self, trades):
        """
        Summarizes the backtest
            summary: (Dict with these Params)
                duration_analyzed
                number_of_trades
                simple_return
                remaining_cash
                owned_shares
                portfolio_value
        """
        summary = {}
        ini_portfolio = self.ini_cash + (self.ohlcv.loc[self.start]['open'] * self.ini_shares)
        final_portfolio = self.curr_cash + (self.ohlcv.loc[self.end]['close'] * self.curr_shares)

        summary['duration_analyzed'] = str(self.end - self.start)
        summary['number_of_trades'] = len(trades)
        summary['simple_return'] = str(100 * (final_portfolio - ini_portfolio) / ini_portfolio) + ' %'
        summary['remaining_cash'] = self.curr_cash
        summary['owned_shares'] = self.curr_shares
        summary['portfolio_value'] = final_portfolio
        self._summary = summary
        return summary

    def summary(self):
        """ Access summary """
        if self._summary:
            return self._summary
        raise KeyError('Run the Algorithm first!')

    def get_closest_stamp(self, index, timestamp, delta, type='start'):
        if type == 'start':
            closest = timestamp
            while closest not in index:
                closest += delta
            return closest
        elif type == 'end':
            closest = timestamp
            while closest not in index:
                closest -= delta
            return closest

    def reset(self):
        self.curr_cash = self.ini_cash
        self.curr_shares = self.ini_shares
