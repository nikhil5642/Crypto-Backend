

from src.tickerDetails.tickers.BTC import getBTCData


def getTickerDetails(tickerId: str):
    print(tickerId)
    if(tickerId == "BTC"):
        return getBTCData()
    return getBTCData()
