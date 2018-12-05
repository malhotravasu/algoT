"""Custom Backtesting Library from Scratch"""

import pandas as pd
from signals import evaluate
from utility import get_next_stamp


class Backtest(object):
    """Main Backtesting Object"""

    def __init__(self, ohlcv, algo=None, ini_cash=10000, ini_shares=0, start=None, end=None, params=None, timedelta=None):
        """
        Backtest object constructor:
        params:
            algo: Preferred algo ("moving_average", "rsi", etc)
        """
        if timedelta:
            self.delta = pd.Timedelta(timedelta)
        else:
            self.delta = pd.Timedelta(days=1) # Default Time delta

        if start:
            start = pd.to_datetime(start)
            self.start = get_next_stamp(ohlcv.index, start, self.delta)
        else:
            self.start = ohlcv.index.min()
        if end:
            end = pd.to_datetime(end)
            self.end = get_next_stamp(ohlcv.index, end, self.delta)
        else:
            self.end = ohlcv.index.max()

        self.ohlcv = ohlcv.loc[self.start:self.end].copy()

        # Immutable Trading variable
        self.ini_cash = ini_cash
        self.ini_shares = ini_shares

        # Mutable Trading variable
        self.curr_cash = ini_cash
        self.curr_shares = ini_shares

        # Algo goes here
        if algo:
            if params:
                (self.buy, self.sell) = evaluate(self.ohlcv, algo, params)
            else:
                (self.buy, self.sell) = evaluate(self.ohlcv, algo)
            self._ready = True
        else:
            self._ready = False

    def run_backtest(self, buy_type, buy_param, sell_type, sell_param):
        """ Run backtest here """
        if not self._ready:
            raise Exception("Signals for trading not ready yet. Set manually or specify algo when initialising.")
        
        self.reset()
        ohlcv = self.ohlcv

        ohlcv['buy'] = self.buy
        ohlcv['sell'] = self.sell
        
        trades = []
        for timestamp, row in ohlcv[(ohlcv['buy'] == True) | (ohlcv['sell'] == True)].iterrows():
            trade = {}
            next_timestamp = get_next_stamp(ohlcv.index, timestamp, self.delta)
            trade_price = ohlcv.loc[next_timestamp]['open']
            trade['timestamp'] = next_timestamp
            trade['share_price'] =  trade_price

            if row['buy']:
                number = self.evaluate_buy(buy_type, buy_param, trade_price)
                if (self.curr_cash < (number * trade_price)):
                    continue
                self.curr_shares += number
                self.curr_cash -= number * trade_price
                trade['owned_shares'] = self.curr_shares
                trade['remaining_cash'] = self.curr_cash
                trade['type'] = 'buy'
            
            else:
                number = self.evaluate_sell(sell_type, sell_param, trade_price)
                if (self.curr_shares < number):
                    continue
                self.curr_shares -= number
                self.curr_cash += number * trade_price
                trade['owned_shares'] = self.curr_shares
                trade['remaining_cash'] = self.curr_cash
                trade['type'] = 'sell'

            trades.append(trade)
        trades_df = pd.DataFrame(trades).set_index('timestamp') # Convert to pandas DataFrame
        self.trades_df = trades_df
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

    def evaluate_buy(self, type, param, buy_price):
        if type == "percent_cash":
            return (param*self.curr_cash) // (buy_price*100)
        elif type == "absolute":
            return param
        elif type == "percent_shares":
            return (param*self.curr_shares) // 100
        elif type == "full_stakes":
            return self.curr_cash // buy_price

    def evaluate_sell(self, type, param, sell_price):
        if type == 'percent_shares':
            return (param*self.curr_shares) // 100
        elif type == 'absolute':
            return param
        elif type == 'percent_portfolio':
            portfolio_value = self.curr_cash + self.curr_shares*sell_price
            return (param*portfolio_value) // 100
        elif type == "full_stakes":
            return self.curr_shares

    def reset(self):
        self.curr_cash = self.ini_cash
        self.curr_shares = self.ini_shares
