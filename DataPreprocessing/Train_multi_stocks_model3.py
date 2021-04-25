from DataPreprocessing.Processing2 import SplitData,DataPipeline, GetclosePrice
if __name__ == '__main__':
    # Specify the stocks you want.
    symbol_list = ['AAPL','TSLA','AMZN','GOOG','BLNK','PLTR','SNAP']
    period = "1y"
    interval = "1d"
    #size of databrick(eg.49 days/hours as a databrick for training)
    size=49
    # return a dictionary of stocks, and a dictionary of labels----{stock_symbol:stock_data;label symbol:label_data}
    StockDict, LabelDict=DataPipeline(symbol_list,period,interval)

    # get price list for testing set to calculate NAV
    StockPriceDic=GetclosePrice(symbol_list,period,interval,size)

    for symbol in symbol_list:
        X_train, X_test, y_train, y_test=SplitData(StockDict[symbol],LabelDict[symbol],size)

        # define and train your model(for each stock) here: