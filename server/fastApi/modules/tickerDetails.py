

from src.tickerDetails.tickers.BTC import getBTCData


def getTickerDetails(tickerId: str):
    if(tickerId == "BTC"):
        return getBTCData()
    return getBTCData()
