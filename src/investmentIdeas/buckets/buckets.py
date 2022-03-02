from turtle import st
from DataBase.MongoDB import getBucketsCollection
from server.fastApi.modules.liveMarketData import getLiveMarketDataInstance
from server.fastApi.routers.market import getTickerLiveData

from src.DataFieldConstants import AMOUNT_PER_UNIT, LAST_UPDATED, NAME, PORTFOLIO, TITLE_IMG, ID, CATEGORY, RETURN_ONE_YR, MIN_AMOUNT, RISK_LEVEL, SHORT_DESCRIPTION, UNIT_PRICE
from typing import List
from datetime import datetime

bucketDB = getBucketsCollection()


def getBucketsBasicInfo(bucketIds: List[str]):
    global lastUpdated
    data = []
    for bucket in bucketDB.find({ID: {'$in': bucketIds}}):
        if(LAST_UPDATED not in bucket or (bucket[LAST_UPDATED]-datetime.now()).total_seconds() > 900):
            updateBucketPrice(bucket)
        data.append({ID: bucket[ID], NAME: bucket[NAME], CATEGORY: bucket[CATEGORY],
                    SHORT_DESCRIPTION: bucket[SHORT_DESCRIPTION],
                    RETURN_ONE_YR: bucket[RETURN_ONE_YR],
                    UNIT_PRICE: bucket[UNIT_PRICE],
                    MIN_AMOUNT: bucket[MIN_AMOUNT],
                    RISK_LEVEL: bucket[RISK_LEVEL],
                    TITLE_IMG: bucket[TITLE_IMG]})
    return data


def getBucketDetail(bucketId: str):
    details = bucketDB.find({ID: bucketId})[0]
    details.pop("_id")
    return details


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
            getLiveMarketDataInstance().getExchangeRate(
                portfolioItem[ID], "INR")

    return price
