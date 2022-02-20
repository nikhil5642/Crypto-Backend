import json
import os

coinTagList = json.load(open(os.path.abspath(
    "./src/tickerDetails/tickerItems/CoinTagList.json"), 'r'))


def getProcessedTickerTags(tickerId: str):
    return coinTagList[tickerId]
