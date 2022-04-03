import json
from time import sleep
from typing import List

from DataBase.MongoDB import getBucketsCollection, getCryptoBalanceCollection
from DataBase.RedisDB import getRedisInstance
from src.DataFieldConstants import NAME, TITLE_IMG, ID, CATEGORY, \
    RETURN_ONE_YR, MIN_AMOUNT, RISK_LEVEL, SHORT_DESCRIPTION, UNIT_PRICE
from src.logger.logger import GlobalLogger

bucketDB = getBucketsCollection()
redis_client = getRedisInstance()
balanceDB = getCryptoBalanceCollection()


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


def updateBucketsInCache():
    GlobalLogger().info("Update Buckets in Cache service started")
    while True:
        for bucket in bucketDB.find({}):
            bucket.pop("_id")
            bucket["lastUpdated"] = bucket["lastUpdated"].timestamp()
            redis_client.set(bucket[ID] + "_MarketData", json.dumps(bucket))
        sleep(5 * 60)


def getBucketDetail(bucketId: str):
    details = json.loads(redis_client.get(bucketId + "_MarketData"))
    return details
