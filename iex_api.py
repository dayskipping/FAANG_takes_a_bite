import requests
import pandas as pd
import numpy as np

def _single_query(endpoint, payload):
    '''
    Single GET request from API

    Parameters:
    ------------
    endpoint : (str)
        URL of API
    payload : (dict)
        keys:values of API parameters

    Returns:
    ------------
    response_dict : (dict)
        dictionary of response data from API
    '''
    response = requests.get(endpoint, params=payload)
    if response.status_code == 200:
        print('Request successful')
        response_dict = dict(response.json())
        return response_dict
    else:
        print('Not available')
        return None

def historical_prices(ticker_list, range, endpoint):
    '''
    Retrieve historical prices of selected securities with a certain range

    Parameters:
    ------------
    ticker_list : (str)
        comma separated symbols
    range : (str)
        API specific range values ie. '1m', 'ytd', '1y'
    endpoint : (str)
        URL of API

    Returns:
    ------------
    df_dict : (dict)
            keys: security symbols , values: dataframes of closing prices over range provided
    '''

    keys = ['symbols', 'types', 'range']
    values = [ticker_list,['chart'],[range]]
    params = dict(zip(keys,values))
    stock_dict = _single_query(endpoint, params)
    df_dict = {}
    for ticker in ticker_list[0].split(', '):
        price_list = [price_dict['close']for price_dict in stock_dict[ticker]['chart']]
        date_list = [pd.to_datetime(price_dict['date']) for price_dict in stock_dict[ticker]['chart']]
        stock_df = pd.DataFrame(data=price_list,columns=['close'], index=date_list)
        df_dict[ticker] = stock_df

    return df_dict

if __name__=='__main__':

    endpoint = 'https://api.iextrading.com/1.0/stock/market/batch'
    FAANG_symbols = ['FB, AMZN, AAPL, NFLX, GOOGL']
    range = '5y'

    FAANG_dfs = historical_prices(FAANG_symbols, range, endpoint)
