import numpy as np
import pandas as pd
import iex_api as iex

def shares_dictionaries(symbols):
    '''
    Create dictionary of dictionaries of shares oustanding by year

    Parameters
    -----------
    symbols : (list)
            security symbols

    Returns:
    -----------
    (dict)
    keys: security symbols (str), values: shares outstanding (dict) - keys: year (int), values: shares outstanding
    '''

    shares = []

    FB_shares = {2014: ((1975722473 + 574020314)+(2236333833 + 562677981))/2, 2015:((2236333833 + 562677981)+(2294939865 + 551340611))/2, 2016:((2294939865 + 551340611) + (2355168103 + 534813231))/2, 2017:((2355168103 + 534813231) + (2395921635 + 509079123))/2, 2018:(2395921635 + 509079123)}
    shares.append(FB_shares)

    AMZN_shares = {2014: (459264535 + 464383939)/2, 2015:(464383939 + 470842035)/2, 2016:(470842035 + 477170618)/2, 2017:(477170618 + 484107183)/2, 2018: 484107183}
    shares.append(AMZN_shares)

    AAPL_shares = {2014: (899738000*7 + 5864840000)/2, 2015:(5864840000 + 5575331000)/2, 2016:( 5575331000 + 5332313000)/2, 2017:(5332313000 + 5134312000)/2, 2018: 5134312000}
    shares.append(AAPL_shares)

    NFLX_shares = {2014:(59807236*7 + 60498082*7)/2 , 2015: 428081221, 2016:(428081221 + 430411593)/2, 2017:(430411593 + 433948461)/2, 2018: 433948461}
    shares.append(NFLX_shares)

    GOOGL_shares = {2014: (286938352 + 53018898 + 340665532), 2015:(292580627 + 50199837 + 345539300), 2016:((292580627 + 50199837 + 345539300) + (297117506 + 47369687 + 346933134))/2, 2017:((297117506 + 47369687 + 346933134) + (298492525 + 46961288 + 349843717))/2, 2018: (298492525 + 46961288 + 349843717)}
    shares.append(GOOGL_shares)

    return dict(zip(symbols, shares))

def filter_dates(stock_dfs, start_date):
    '''
    Filter dictionary of dfs to start from specified date

    Parameters:
    ------------
    stock_dfs : (dict)
        keys: security symbols (str), values: closing prices (df)
    start_date : (pd.datetime object)
        starting date for filtering dfs

    Returns:
    ------------
    stock_dfs : (dict)
        keys: security symbols (str), values: closing prices from start date forward (df)
    '''
    for k, df in stock_dfs.items():
        df = df[df.index >= start_date]
        stock_dfs[k] = df

    return stock_dfs

def market_cap_data(stock_dfs, cap_dicts):
    '''
    Add market cap column of data to closing price dfs

    Parameters:
    -------------
    stock_dfs : (dict)
        keys: security symbols (str), values: closing prices (df)
    cap_dicts : (dict)
        keys: security symbols (str), values: shares outstanding (dict) - keys: year (int), values: shares outstanding (int)

    Returns:
    -------------
    stock_dfs : (dict)
        keys: security symbols, values: closing prices and market cap (df)
    '''
    for k, df in stock_dfs.items():
        years = pd.Series(index= df.index, data=df.index.year)
        cap_dict = cap_dicts[k]
        df['cap'] = years.apply(lambda x: cap_dict.get(x))
        df['cap'] = (df['cap'] * df['close'])/1e9
        stock_dfs[k] = df

    return stock_dfs

def SP_data(file_path, start_date):
    '''
    Reads csv file of SP total market cap data, transforms to df

    Parameters:
    -------------
    file_path : (str)
        location of csv file with SP cap data
    start_date : (pd.datetime object)
        starting date to filter df

    Returns:
    -------------
    dfSPcap : (df)
        index: pd.datetime series(ascending), columns: 'Cap', data: (int)
    '''
    dfSPcap = pd.read_csv(file_path)
    dfSPcap = dfSPcap[['Date', 'Total_Market_Cap']]
    dfSPcap['Date'] = pd.to_datetime(dfSPcap['Date'])
    dfSPcap['Total_Market_Cap'] = dfSPcap['Total_Market_Cap'].str.replace(',','')
    dfSPcap = pd.DataFrame(index=dfSPcap.Date, data=pd.to_numeric(dfSPcap['Total_Market_Cap'].values), columns=['Cap'])
    dfSPcap['Cap'] = dfSPcap['Cap']/1e3
    dfSPcap = dfSPcap[dfSPcap.index >= start_date]
    dfSPcap = dfSPcap.reindex(index=dfSPcap.index[::-1])

    return dfSPcap

def df_compiler(df_dict, symbols, col_name):
    '''
    Compiles df

    Parameters:
    ------------
    df_dict : (dict)
        keys: security symbols (str), values: closing prices and cap data (df)
    symbols : (list)
        security symbols (str)
    col_name : (str)
        string designating column of data to be used in df compiling

    Returns:
    ------------
    return_df: (df)
        index: pd.datetime series, columns: symbols, data: col_name values
    '''
    df_values = [df[col_name].values for df in df_dict.values()]
    data_dict = dict(zip(symbols, df_values))
    return_df = pd.DataFrame(index=df_dict['FB'].index, data=data_dict)

    return return_df

if __name__ == '__main__':

    endpoint = 'https://api.iextrading.com/1.0/stock/market/batch'
    FAANG_symbols = ['FB','AMZN','AAPL','NFLX','GOOGL']

    FAANG_dfs = iex.historical_prices(FAANG_symbols, '5y', endpoint)
    shares_dicts = shares_dictionaries()

    FAANG_dfs = market_cap_data(filter_dates(FAANG_dfs), shares_dicts)
    dfSP, dfSPcap = SP_data()

    cap_df = df_compiler(FAANG_dfs, FAANG_symbols, 'cap')
    close_df = df_compiler(FAANG_dfs, FAANG_symbols, 'close')
