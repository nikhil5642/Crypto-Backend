from datetime import datetime
from time import sleep

from DataBase.MongoDB import getBucketsCollection, getBucketsTransactionCollection, getUserInfoCollection, \
    getCryptoBalanceCollection
from src.DataFieldConstants import ID, LAST_UPDATED, PORTFOLIO, UNIT_PRICE, AMOUNT_PER_UNIT, \
    LAST_PRICE
from src.logger.logger import GlobalLogger

bucketDB = getBucketsCollection()
bucketTransactionDB = getBucketsTransactionCollection()
userDB = getUserInfoCollection()
balanceDB = getCryptoBalanceCollection()


def updateAllBucketUnitPrice():
    GlobalLogger().info("Update all buckets price service started")
    while True:
        for bucket in bucketDB.find({}):
            current_price = calculateUnitPrice(bucket[PORTFOLIO])
            bucketDB.update_one(
                {ID: bucket[ID]}, {"$set": {UNIT_PRICE: current_price, LAST_UPDATED: datetime.now()}})
        sleep(5 * 60)


def calculateUnitPrice(portfolio: str):
    price = 0
    for portfolioItem in portfolio:
        price += portfolioItem[AMOUNT_PER_UNIT] * \
                 getLatestTickerPrice(portfolioItem[ID])

    return price


def getLatestTickerPrice(tickerId):
    ticker = balanceDB.find_one({ID: tickerId})
    if ticker[LAST_PRICE] > 0:
        return ticker[LAST_PRICE]
    else:
        GlobalLogger().error("No last price found")
        return 1
