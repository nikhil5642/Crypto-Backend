import json

from DataBase.RedisDB import getRedisInstance
from src.DataFieldConstants import ITEM_TYPE, DATA

redis_instance = getRedisInstance()


def fetchChartData(tickerId):
    current = redis_instance.get(tickerId + "_ChartData")
    if current is None:
        return None
    else:
        return json.loads(current)


class ChartData:
    ITEM_TYPE = "ChartData"

    def __init__(self, tickerId: str):
        self.DATA = fetchChartData(tickerId)

    def getJson(self):
        return {
            ITEM_TYPE: self.ITEM_TYPE,
            DATA: self.DATA
        }
