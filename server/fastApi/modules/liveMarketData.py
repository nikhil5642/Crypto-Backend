from datetime import datetime
from tokenize import Double
from typing import List

import numpy as np
import pandas as pd
import requests

from src.tickerDetails.tickerItems.tagsProcessing import getProcessedTickerTags

baseUrl = "https://min-api.cryptocompare.com"


class Ticker:
    name = ""
    tickerId = ""
    currentPrice = 0.0
    change = 0.0
    volatility = 0
    tags = []
    lastFetched = datetime.now()

    def __init__(self, name: str, tickerId: str, currentPrice: Double, change: Double):
        self.name = name
        self.tickerId = tickerId
        self.currentPrice = currentPrice
        self.change = change
        self.tags = getProcessedTickerTags(tickerId)

    def updatePrice(self, newPrice: Double, change: Double):
        self.currentPrice = newPrice
        self.change = change
        if (datetime.now() - self.lastFetched).total_seconds() > 3600:
            self.updateAdditionalInfo()

    def getJsonData(self):
        return {"name": self.name,
                "id": self.tickerId,
                "price": self.currentPrice,
                "change": self.change,
                "riskIndex": self.volatility,
                "tags": self.tags, }

    def updateAdditionalInfo(self):
        endPoint = "data/v2/histohour"
        params = {"fsym": self.tickerId,
                  "tsym": "INR",
                  "limit": 200,
                  "toTs": -1
                  }
        response = requests.get(baseUrl + endPoint, params=params)
        if response.status_code == 200:
            df = pd.DataFrame(response.json()["Data"])
            df.sort_index(ascending=False, inplace=True)
            self.calculateAndUpdateVolatility(df)
            self.lastFetched = datetime.now()

    def calculateAndUpdateVolatility(self, df):
        returns = (np.log(df.close /
                          df.close.shift(-1)))
        returns.fillna(0, inplace=True)
        std = np.std(returns)
        mean = np.mean(returns)
        if returns[0] > mean + 3 * std or returns[0] < mean - 3 * std:
            self.volatility = 1  # "Highly Volatile"
        elif returns[0] > mean + std or returns[0] < mean - std:
            self.volatility = 0  # "Volatile"
        else:
            self.volatility = -1  # "Low Volatile"


class LiveMarketData:
    data = {}
    lastFetched = datetime.now()

    def createOrUpdateTicker(self, name: str, tickerId: str, currentPrice: Double, change: Double):
        if tickerId in self.data:
            self.data[tickerId].updatePrice(currentPrice, change)
        else:
            self.data[tickerId] = Ticker(name, tickerId, currentPrice, change)

    def fetchAndUpdateLiveMarketData(self):
        endPoint = "/data/top/mktcapfull"
        params = {"limit": 100,
                  "tsym": "INR",
                  "page": 0}

        response = requests.get(baseUrl + endPoint, params=params)
        if response.status_code == 200:
            for ticker in response.json()["Data"]:
                try:
                    self.createOrUpdateTicker(
                        ticker["CoinInfo"]["FullName"], ticker["CoinInfo"]["Name"], ticker["RAW"]["INR"]["PRICE"],
                        ticker["RAW"]["INR"]["CHANGEPCT24HOUR"])
                except:
                    print("Data not present for:",
                          ticker["CoinInfo"]["FullName"])
            self.lastFetched = datetime.now()
            print("Live Data Fetched")
        else:
            self.fetchAndUpdateLiveMarketData()

    def getTickersData(self, ticker: List[str]):
        if (datetime.now() - self.lastFetched).total_seconds() > 900:
            self.fetchAndUpdateLiveMarketData()
        return [self.data[val].getJsonData() for val in ticker if val in self.data]

    def getExchangeRate(self, fromCurrency: str, toCurrency: str):
        if (datetime.now() - self.lastFetched).total_seconds() > 900:
            self.fetchAndUpdateLiveMarketData()
        try:
            return self.data[fromCurrency].currentPrice
        except:
            return 1


marketData = LiveMarketData()
marketData.fetchAndUpdateLiveMarketData()


def getLiveMarketDataInstance():
    return marketData


if __name__ == '__main__':
    liveMarketData = LiveMarketData()
    liveMarketData.fetchAndUpdateLiveMarketData()
    print(liveMarketData.getTickersData(["BTC", "XRP", "ABC"]))
