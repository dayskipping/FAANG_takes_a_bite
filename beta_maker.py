import numpy as np
import pandas as pd
import iex_api as iex
import scipy.stats as scs

def returns_maker(close_df, type='reg'):
    '''
    Takes df of closing prices and transforms to returns/log returns

    Parameters:
    ------------
    close_df : (df)
        df of closing prices
    type : (str), optional
        pass in 'log' for log returns

    Returns:
    ------------
    returns_df : (df)
        df of returns/log returns with first entry dropped
    '''
    if type == 'log':
        returns_df = np.log(close_df/close_df.shift(1)).dropna()
    else:
        returns_df = (close_df/close_df.shift(1) - 1).dropna()

    return returns_df


def total_return_from_returns(returns_series):
    '''
    Takes returns series and multiplies out for total return calculation

    Parameters:
    ------------
    returns_series: (int, pd.Series)
        Series of returns

    Returns:
    ------------
    (int, pd.Series)
        Total return over period provided
    '''
    return (returns_series + 1).prod() - 1

def monthly_returns_from_returns(returns_df):
    '''
    Takes daily returns series and transforms into monthly returns

    Parameters:
    -------------
    returns_df: (df)
        df of daily returns

    Returns:
    -------------
    monthly_returns_df : (df)
        df of monthly returns
    '''

    monthly_returns_df = returns_df.groupby((returns_df.index.year, returns_df.index.month))\
                        .apply(total_return_from_returns)

    return monthly_returns_df

def beta_maker(stock_close, market_close, freq, periods, type='reg'):
    '''
    Takes closing prices for market and securities, returns dict of rolling betas for freq and period specified

    Parameters:
    -------------
    stock_close: (dict)
        keys: security symbols, values: dfs of closing prices
    market_close: (dict)
        key: market symbol, value: df of closing prices
    freq: (str)
        frequency of returns series used, 'monthly' or 'daily'
    periods: (int)
        number of periods included in calculation
    type: (str)
        'reg'(default) for regular returns, 'log' for log returns

    Returns:
    -------------
    rolling_beta: (df)
        index: year/month, columns: symbols, data: rolling beta values
    '''

    stock_returns = {}
    rolling_betas = {}
    # rolling_beta_reg = {}
    if freq == 'monthly':
        for stock, df in stock_close.items():
            stock_returns[stock] =  monthly_returns_from_returns(returns_maker(df, type))
        for df in market_close.values():
            market_returns =  monthly_returns_from_returns(returns_maker(df, type))
    elif freq == 'daily':
        for stock, df in stock_close.items():
            stock_returns[stock] = returns_maker(df, type)
        for df in market_close.values():
            market_returns = returns_maker(df, type)
    for symbol in stock_returns.keys():
        rolling_betas[symbol] = (stock_returns[symbol].rolling(window=periods).cov(market_returns)/\
                                        market_returns.rolling(window=periods, center=False).var()).dropna()
        beta_dict = {col:rolling_betas[col].rename(columns={'close':col}) for col in rolling_betas.keys()}
        beta_df = pd.DataFrame(data={col:beta_dict[col][col].values for col in beta_dict.keys()}, index=beta_dict[list(beta_dict.keys())[0]].index)

        # alternative method using linear regression
        # b, a, r, p, e = scs.linregress(market_returns.close.values[-36:],stock_returns[symbol].close.values[-36:])
        # rolling_beta_reg[symbol] = b

    return beta_df

if __name__ == '__main__':

    endpoint = 'https://api.iextrading.com/1.0/stock/market/batch'
    FAANG_symbols = ['FB, AMZN, AAPL, NFLX, GOOGL']

    SPY_close = iex.historical_prices(['SPY'], '5y', endpoint)
    FAANG_close = iex.historical_prices(FAANG_symbols, '5y', endpoint)
    rolling_betas = beta_maker(FAANG_close, SPY_close, 'monthly', 36)

    beta_list = []
    for betas in rolling_betas.values():
        beta_list.append(betas['close'][-1])
    FAANG_betas = pd.DataFrame(index=rolling_betas.keys(), data=beta_list, columns=['Beta'])

# beta_list = []
# for symbol in FAANG_monthly_returns.columns:
#     stock_beta = np.cov(FAANG_monthly_returns[symbol], SP_monthly_returns)[0][1]/np.var(SP_monthly_returns)
#     beta_list.append(stock_beta)
# FAANG_betas = pd.DataFrame(index=FAANG_monthly_returns.columns, data=beta_list, columns=['Beta'])
#
# rolling_beta = {}
# for symbol in FAANG_monthly_returns.columns:
#     rolling_beta[symbol] = (FAANG_monthly_returns[symbol].rolling(window=36).cov(SP_monthly_returns)/SP_monthly_returns.rolling(window=36, center=False).var()).dropna()
