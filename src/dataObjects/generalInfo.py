import json
import os

from src.DataFieldConstants import DATA, DESCRIPTION, ITEM_TYPE, NAME

data = json.load(open(os.path.abspath(
    "./src/assets/CoinList.json"), 'r'))


class GeneralInfo:
    ITEM_TYPE = "GeneralInfo"

    def __init__(self, tickerId: str):
        if (tickerId in data):
            self.DATA = {NAME: data[tickerId]["CoinName"],
                         DESCRIPTION: data[tickerId]["Description"]}
        else:
            self.DATA = None

    def getJson(self):
        return {
            ITEM_TYPE: self.ITEM_TYPE,
            DATA: self.DATA
        }


if __name__ == '__main__':
    print(GeneralInfo("BTC").getJson())
