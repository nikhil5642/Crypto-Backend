import copy
from datetime import date, datetime
import json
from tkinter import CURRENT
from tokenize import Double
from typing import List
from DataBase.MongoDB import getLiveMarketCollection
from DataBase.RedisDB import getRedisInstance
import pickle
import numpy as np
import pandas as pd
import requests
from src.DataFieldConstants import CHANGE, ID, LAST_UPDATED, NAME, PRICE, VOLATILITY


baseUrl = "https://min-api.cryptocompare.com"

liveMarketDB = getLiveMarketCollection()

redis_instance = getRedisInstance()


def updateAdditionalInfo(tickerId):
    endPoint = "/data/v2/histohour"
    params = {"fsym": tickerId,
              "tsym": "INR",
              "limit": 200,
              "toTs": -1}
    response = requests.get(baseUrl + endPoint, params=params)
    if response.status_code == 200:
        df = pd.DataFrame(response.json()["Data"]["Data"])
        df.sort_index(ascending=False, inplace=True)
        volatility = calculateVolatility(df)
        current = json.loads(redis_instance.get(tickerId+"_MarketData"))
        current[VOLATILITY] = volatility
        current[LAST_UPDATED] = datetime.timestamp(datetime.now())
        redis_instance.set(tickerId+"_MarketData", json.dumps(current))


def calculateVolatility(data):
    df = copy.deepcopy(data)
    returns = (np.log(df.close /
                      df.close.shift(-1)))
    returns.fillna(0, inplace=True)
    std = np.std(returns)
    mean = np.mean(returns)
    if returns[0] > mean + 3 * std or returns[0] < mean - 3 * std:
        volatility = 1  # "Highly Volatile"
    elif returns[0] > mean + std or returns[0] < mean - std:
        volatility = 0  # "Volatile"
    else:
        volatility = -1  # "Low Volatile"
    return volatility


class LiveMarketData:

    def createOrUpdateTicker(self, name: str, tickerId: str, currentPrice: Double, change: Double):
        val = redis_instance.get(tickerId+"_MarketData")
        if val is not None:
            val = json.loads(val)
            val[PRICE] = currentPrice
            val[CHANGE] = change
            redis_instance.set(tickerId+"_MarketData", json.dumps(val))
            if LAST_UPDATED in val and (datetime.now() - datetime.fromtimestamp(float(val[LAST_UPDATED]))).total_seconds() > 3600:
                updateAdditionalInfo(tickerId)
        else:
            redis_instance.set(tickerId+"_MarketData", json.dumps(
                {NAME: name, ID: tickerId, PRICE: currentPrice, CHANGE: change}))
            updateAdditionalInfo(tickerId)

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
            redis_instance.set("liveMarketDataLastFetched",
                               datetime.timestamp(datetime.now()))
            print("Live Data Fetched")
        else:
            self.fetchAndUpdateLiveMarketData()

    def getTickersData(self, tickers: List[str]):
        lastUpdated = redis_instance.get("liveMarketDataLastFetched")
        if lastUpdated is None or (datetime.now() - datetime.fromtimestamp(float(lastUpdated))).total_seconds() > 900:
            self.fetchAndUpdateLiveMarketData()
        data = []
        for tickerId in tickers:
            ticker = redis_instance.get(tickerId+"_MarketData")
            if ticker is not None:
                data.append(json.loads(ticker))
        return data

    def getExchangeRate(self, fromCurrency: str, toCurrency: str):
        ticker = redis_instance.get(fromCurrency+"_MarketData")
        if ticker is None:
            return 0
        return json.loads(ticker)[PRICE]


marketData = LiveMarketData()
marketData.fetchAndUpdateLiveMarketData()


def getLiveMarketDataInstance():
    return marketData


if __name__ == '__main__':
    liveMarketData = LiveMarketData()
    liveMarketData.fetchAndUpdateLiveMarketData()
    print(liveMarketData.getTickersData(["BTC", "XRP", "ABC"]))
