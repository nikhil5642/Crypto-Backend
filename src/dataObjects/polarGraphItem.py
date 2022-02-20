from src.DataFieldConstants import ITEM_TYPE, TITLE, VALUES, DATA

from typing import List


class PolarGraphDataItem:
    def __init__(self, name: str, value: int):
        self.name = name
        self.value = value

    def getJson(self):
        return {"x": self.name, "y": self.value}


class PolarGraphItem:
    ITEM_TYPE = "PolarGraph"

    def __init__(self, title: str, itemList: List[PolarGraphDataItem]):
        self.DATA = {
            TITLE: title,
            VALUES: [item.getJson() for item in itemList]
        }

    def getJson(self):
        return {
            ITEM_TYPE: self.ITEM_TYPE,
            DATA: self.DATA
        }


if __name__ == '__main__':
    print(PolarGraphItem("title", [PolarGraphDataItem("adb", 0)]).getJson())
