import json
import os

from src.DataFieldConstants import DATA, DESCRIPTION, ITEM_TYPE, NAME

data = json.load(open(os.path.abspath("./src/tickerDetails/tickerItems/CoinList.json"), 'r'))


class GeneralInfo:
    ITEM_TYPE = "GeneralInfo"

    def __init__(self, tickerId: str):
        self.DATA = {NAME: data[tickerId]["CoinName"], DESCRIPTION: data[tickerId]["Description"]}

    def getJson(self):
        return {
            ITEM_TYPE: self.ITEM_TYPE,
            DATA: self.DATA
        }


if __name__ == '__main__':
    print(GeneralInfo("BTC").getJson())
