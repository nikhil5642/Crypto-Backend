from turtle import st
from DataBase.MongoDB import getBucketsCollection
from server.fastApi.routers.market import getTickerLiveData

from src.DataFieldConstants import AMOUNT_PER_UNIT, NAME, PORTFOLIO, TITLE_IMG, ID, CATEGORY, RETURN_ONE_YR, RETURN_THREE_YR, MIN_AMOUNT, RISK_LEVEL, SHORT_DESCRIPTION, UNIT_PRICE
from typing import List

bucketDB = getBucketsCollection()


def getBucketsBasicInfo(bucketIds: List[str]):
    data = []
    for bucket in bucketDB.find({ID: {'$in': bucketIds}}):
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


def getCurrentUnitPrice(bucketId: str):
    return bucketDB.find({ID: bucketId})[0][UNIT_PRICE]


# def updateAllUnitPrice(bucketId: str):
#     print("")


def calculateUnitPrice(bucketId: str):
    price = 0
    for portfolioItem in bucketDB.find({ID: bucketId})[PORTFOLIO]:
        price += portfolioItem[AMOUNT_PER_UNIT] * \
            getTickerLiveData().getExchangeRate(portfolioItem[ID])

    return price
