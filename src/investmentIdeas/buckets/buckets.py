import json
from datetime import datetime
from typing import List

from DataBase.MongoDB import getBucketsCollection
from DataBase.RedisDB import getRedisInstance
from server.fastApi.modules.liveMarketData import getExchangeRate
from src.DataFieldConstants import AMOUNT_PER_UNIT, LAST_UPDATED, NAME, PORTFOLIO, TITLE_IMG, ID, CATEGORY, \
    RETURN_ONE_YR, MIN_AMOUNT, RISK_LEVEL, SHORT_DESCRIPTION, UNIT_PRICE

bucketDB = getBucketsCollection()
redis_client = getRedisInstance()


def getBucketsBasicInfo(bucketIds: List[str]):
    data = []
    for bucketId in bucketIds:
        bucket = redis_client.get(bucketId + "_MarketData")
        if bucket is not None:
            bucket = json.loads(bucket)
            data.append({ID: bucket[ID], NAME: bucket[NAME], CATEGORY: bucket[CATEGORY],
                         SHORT_DESCRIPTION: bucket[SHORT_DESCRIPTION],
                         RETURN_ONE_YR: bucket[RETURN_ONE_YR],
                         UNIT_PRICE: bucket[UNIT_PRICE],
                         MIN_AMOUNT: bucket[MIN_AMOUNT],
                         RISK_LEVEL: bucket[RISK_LEVEL],
                         TITLE_IMG: bucket[TITLE_IMG]})
    return data


def updateRedisDataBase():
    for bucket in bucketDB.find({}):
        bucket.pop("_id")
        bucket.pop("lastUpdated")
        redis_client.set(bucket[ID] + "_MarketData", json.dumps(bucket))


def getBucketDetail(bucketId: str):
    details = json.loads(redis_client.get(bucketId + "_MarketData"))
    return details


def buyBucket(bucketId: str):
    json.loads(redis_client.get(bucketId + "_MarketData"))[PORTFOLIO]


def updateAllUnitPrice():
    for bucket in bucketDB.find({}):
        updateBucketPrice(bucket)


def updateBucketPrice(bucketData):
    current_price = calculateUnitPrice(bucketData[PORTFOLIO])
    bucketDB.update_one(
        {ID: bucketData[ID]}, {"$set": {UNIT_PRICE: current_price, LAST_UPDATED: datetime.now()}})


def calculateUnitPrice(portfolio: str):
    price = 0
    for portfolioItem in portfolio:
        price += portfolioItem[AMOUNT_PER_UNIT] * \
            getExchangeRate(
            portfolioItem[ID], "INR")

    return price
