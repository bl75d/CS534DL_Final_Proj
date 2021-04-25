# CS534DL_Final_Proj
## Project Structure:
### There are 3 directories: DataPreprocessing, ModelEvaluation, and TestFile(ignore);Only focus on DataPreprocessing directory; Write your code for model training under TrainTrain_all_in_one_model3.py or Train_multi_stocks_model3.py;
> TrainTrain_all_in_one_model3.py: combine all stocks data together and train them with only one model.(Try one model first)
> Train_multi_stocks_model3.py: build and train models for each stock.

## Project goals:
### The first goal is to use the past n days data to predict next day's price

>1.Put your model file under the comment in Train_all_in_one_model3.py to get a list of stock data, each element in the list is one year daily stock dataframe including features listed below:
       ['open', 'close', 'high', 'low', 'volume', 'amount', 'volume_delta',
       'open_2_d', 'open_-2_r', 'cr', 'cr-ma1', 'cr-ma2', 'cr-ma3',
       'volume_-3,2,-1_max', 'volume_-3~1_min', 'kdjk', 'kdjd', 'kdjj',
       'open_2_sma', 'macd', 'macds', 'macdh', 'boll', 'boll_ub', 'boll_lb',
       'close_10.0_le_5_c', 'cr-ma2_xu_cr-ma1_20_c', 'close_10.0_ge_5_fc',
       'rsi_6', 'rsi_12', 'wr_10', 'wr_6', 'cci', 'cci_20', 'tr', 'atr', 'dma',
       'pdi', 'mdi', 'dx', 'adx', 'adxr', 'trix', 'close_3_trix', 'trix_9_sma',
       'tema', 'close_2_tema', 'vr', 'vr_6_sma']

>2.Change symbol_list,period,interval to get data of different stocks, perionds and interval
