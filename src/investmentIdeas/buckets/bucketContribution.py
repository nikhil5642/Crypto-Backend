from re import I
from time import sleep
from DataBase.MongoDB import getBucketsCollection
from src.DataFieldConstants import AMOUNT_PER_UNIT, ID, PORTFOLIO, UNIT_PRICE

from src.investmentIdeas.buckets.bucketUnitPrice import calculateUnitPrice, getLatestTickerPrice

bucketDB = getBucketsCollection()


def updateAllBucketPortfolioContribution():
    for bucket in bucketDB.find({}):
        unit_price = bucket[UNIT_PRICE]
        for item in bucket[PORTFOLIO]:
            bucketDB.update_one(
                {ID: bucket[ID]}, {"$set": {PORTFOLIO + "." + item[ID]: getTickerContribution(item, unit_price)}})


def getTickerContribution(item, unit_price):
    return round((getLatestTickerPrice(item[ID]) * item[AMOUNT_PER_UNIT]*100)/unit_price, 2)
