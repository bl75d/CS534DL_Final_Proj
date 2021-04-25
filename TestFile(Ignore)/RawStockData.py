# https://pypi.org/project/yfinance/
# https://pypi.org/project/stock-dataframe/
from stock_dataframe import StockDataFrame
import yfinance as yf
import pandas as pd
# It only contains open close high low and volume features.
def generate_df(company,period,interval):
    rawdata = yf.download(  # or pdr.get_data_yahoo(...
            # tickers list or string as well
            tickers = company,

            # use "period" instead of start/end
            # valid periods: 1d,5d,1mo,3mo,6mo,1y,2y,5y,10y,ytd,max
            # (optional, default is '1mo')
            # period = "ytd",
            period=period,

            # fetch data by interval (including intraday if period < 60 days)
            # valid intervals: 1m,2m,5m,15m,30m,60m,90m,1h,1d,5d,1wk,1mo,3mo
            # (optional, default is '1d')
            interval = interval,

            # group by ticker (to access via data['SPY'])
            # (optional, default is 'column')
            group_by = 'ticker',

            # adjust all OHLC automatically
            # (optional, default is False)
            # auto_adjust = True,

            # download pre/post regular market hours data
            # (optional, default is False)
            prepost = True,

            # use threads for mass downloading? (True/False/Integer)
            # (optional, default is True)
            threads = True,

            # proxy URL scheme use use when downloading?
            # (optional, default is None)
            proxy = None
        )
    rawdata['Amount']=rawdata['Adj Close']*rawdata['Volume']
    rawdata.columns=['open','high','low','close','adj','volume','amount']
    data=rawdata[['open','close','high','low','volume','amount']]
    return data

def to_df(stock_df):
    df = pd.DataFrame(stock_df)
    return df

def generate_stdf(data):
    stockdf=StockDataFrame.retype(pd.DataFrame(data))
    return stockdf

# generate a list of stock data
def stock(symbol_list,period,interval):
    data=[]
    for symbol in symbol_list:
        stockdata = generate_df(symbol,period,interval)
        stockdf= generate_stdf(stockdata)
        columns = ['open','close','high','low','volume','amount']
        stock=stockdf[columns]
        data.append(to_df(stock))
    # data is a list of stocks, each element in list is a pd.dataframe of a stock
    return data

if __name__ == '__main__':
    # get the stock data by calling stock() function
    symbol_list,period,interval=["AAPL","AMZN","TSLA","GOOG"],'1y','1d'
    # return a list of stock data
    # each element in the list is a stock dataframe,including such features:
    stockdata=stock(symbol_list,period,interval)
    print(stockdata[0])
