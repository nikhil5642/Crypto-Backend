import json
import os

from src.DataFieldConstants import TAGS, ITEM_TYPE, DATA

fundamentals = json.load(open(os.path.abspath(
    "./src/assets/CoinFundamentals.json"), 'r'))


def getProcessedTickerTags(tickerId: str):
    if tickerId in fundamentals:
        return fundamentals[tickerId].get(TAGS, [])
    return []


class TickerTags:
    ITEM_TYPE = "Tags"

    def __init__(self, tickerId: str):
        if tickerId in fundamentals:
            self.DATA = {TAGS: getProcessedTickerTags(tickerId)}
        else:
            self.DATA = None

    def getJson(self):
        return {
            ITEM_TYPE: self.ITEM_TYPE,
            DATA: self.DATA
        }
