import numpy as np
import matplotlib.pyplot as plt
class Nav:
    def __init__(self,initial_value):
        self.symbol=''
        self.day=0
        self.initial_value=initial_value
        self.cash=initial_value
        self.nav=initial_value
        self.stockquant=0
        self.stockprice=0
        self.stockvalue=0
        # record the trading history
        self.tradinghist=[]
        self.pricehist=[]
        self.navhist=[]

    def invest(self,symbol,signal,price):
        self.day+=1
        self.symbol=symbol
        # sell
        if signal==0:
            # have stock
            if self.stockquant>0:
                self.stockprice=price
                self.cash +=self.stockquant*self.stockprice
                self.stockquant=0
                self.stockvalue=0
                self.nav=self.stockvalue+self.cash

            self.tradinghist.append(signal)
            self.pricehist.append(price)
            self.navhist.append(self.nav)

        # Buy
        elif signal==2:
            # have 0 stock
            if self.stockquant==0:
                self.nav = self.cash
                self.stockprice = price
                self.stockquant = int(self.cash/self.stockprice)
                self.stockvalue = self.stockquant*self.stockprice
                self.cash -= self.stockvalue
                self.nav=self.stockvalue+self.cash

            self.tradinghist.append(signal)
            self.pricehist.append(price)
            self.navhist.append(self.nav)

        #hold
        elif signal==1:
            self.stockprice = price
            self.stockvalue = self.stockquant * self.stockprice
            self.nav=self.cash+self.stockvalue

            self.tradinghist.append(signal)
            self.pricehist.append(price)
            self.navhist.append(self.nav)


# use stock['close'] as the stock price; y_predict is the prediction for X_test, it is the signal for trading
def Generate_nav(fund,symbol,price,y_predict):
    teststart=price.shape[0]-y_predict.shape[0]
    stockprice = price[teststart:price.shape[0]]
    # print(y_predict.shape[0])
    # print(stockprice.shape[0])
    if stockprice.shape[0]==y_predict.shape[0]:
        portofolio = Nav(fund)
        for i in range(stockprice.shape[0]):
            # print(y_predict.flatten()[i])
            # print(stockprice.flatten()[i])
            portofolio.invest(symbol,y_predict.flatten()[i],stockprice.flatten()[i])
        # It is the list of NAV during the tesing period
        NetAssetValue=portofolio.navhist
        Tradinghist=portofolio.tradinghist
        pricehist=portofolio.pricehist
        # print(len(NetAssetValue))
        # print(len(Tradinghist))
        # print(len(pricehist))

        # print(stockprice[0])
        # print(len(stockprice))
        # Market Performance:
        shares=fund/stockprice[0]
        marketvalue=shares*stockprice.flatten()
        # print(marketvalue)
        # *******
        plt.plot(marketvalue)
        plt.plot(NetAssetValue)
        plt.title(symbol)
        plt.ylabel('Net Asset Value')
        plt.xlabel('Day')
        plt.legend(['Market Value','Investment Value'], loc='upper left')
        plt.show()
        return portofolio.navhist
    else:
        print("Prediction length error! Check generate_nav()")
