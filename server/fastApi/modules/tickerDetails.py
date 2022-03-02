

from src.tickerDetails.tickerItems.generalInfo import GeneralInfo
from src.tickerDetails.tickerItems.tagsProcessing import getProcessedTickerTags
from src.tickerDetails.tickers.BTC import getBTCData


def getTickerDetails(tickerId: str):
    data = []
    data.append(GeneralInfo(tickerId).getJson())
    getProcessedTickerTags(tickerId)

    return data
