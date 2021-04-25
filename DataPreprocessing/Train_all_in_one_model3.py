from DataPreprocessing.Processing2 import SplitData,DataPipeline, GetclosePrice
import numpy as np
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

    # Generate Xtrain, Xtest, ytrain, ytest for training and testing
    Xtrain, Xtest, ytrain, ytest = SplitData(StockDict[symbol_list[0]], LabelDict[symbol_list[0]], size)
    for i in range(1,len(symbol_list)):
        X_train, X_test, y_train, y_test=SplitData(StockDict[symbol_list[i]],LabelDict[symbol_list[i]],size)
        Xtrain=np.concatenate((Xtrain,X_train),axis=0)
        Xtest = np.concatenate((Xtest, X_test), axis=0)
        ytrain = np.concatenate((ytrain, y_train), axis=0)
        ytest = np.concatenate((ytest, y_test), axis=0)


    # define and train your model here: