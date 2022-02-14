
import re
from selectors import SelectorKey
from tokenize import Double

from anyio import sleep_forever
from coinmarketcapapi import CoinMarketCapAPI, CoinMarketCapAPIError
from datetime import datetime

COINMARKETCAP_API_KEY = '8ac04e5d-477c-44c4-a58e-3e4f82e3253f'


class Ticker:
    name = ""
    tickerId = ""
    currentPrice = 0.0

    def __init__(self, name: str, tickerId: str, currentPrice: Double):
        self.name = name
        self.tickerId = tickerId
        self.currentPrice = currentPrice

    def updatePrice(self, newPrice: Double):
        self.currentPrice = newPrice

    def getJsonData(self):
        return {"name": self.name,
                "id": self.tickerId,
                "price": self.currentPrice}


class LiveMarketData():
    data = {}
    cmc = CoinMarketCapAPI(COINMARKETCAP_API_KEY)
    lastFetched = datetime.now()

    def createOrUpdateTicker(self, name: str, tickerId: str, currentPrice: Double):
        if(tickerId in self.data):
            self.data[tickerId].updatePrice(currentPrice)
        else:
            self.data[tickerId] = Ticker(name, tickerId, currentPrice)

    def fetchAndUpdateLiveMarketData(self):
        fetched = self.cmc.cryptocurrency_listings_latest(
            convert='INR', start=1, limit=10)
        for ticker in fetched.data:
            self.createOrUpdateTicker(
                ticker["name"], ticker["symbol"], ticker["quote"]["INR"]["price"])
        self.lastFetched = datetime.now()
        print("Live Data Fetched")

    def getTickersData(self, ticker: list[str]):
        if((datetime.now() - self.lastFetched).total_seconds() > 900):
            self.fetchAndUpdateLiveMarketData()
        return [self.data[val].getJsonData() for val in ticker if val in self.data]

    def getExchangeRate(self, fromCurrency: str, toCurrency: str):
        if((datetime.now() - self.lastFetched).total_seconds() > 900):
            self.fetchAndUpdateLiveMarketData()
        return self.data[toCurrency].currentPrice


marketData = LiveMarketData()
marketData.fetchAndUpdateLiveMarketData()


def getLiveMarketDataInstance():
    return marketData


if __name__ == '__main__':
    liveMarketData = LiveMarketData()
    liveMarketData.fetchAndUpdateLiveMarketData()
    print(liveMarketData.getTickersData(["BTC", "XRP", "ABC"]))
