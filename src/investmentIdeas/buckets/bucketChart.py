
from DataBase.MongoDB import getBucketsCollection, getCryptoBalanceCollection
from src.DataFieldConstants import UNIT_PRICE


bucketDB = getBucketsCollection()
balanceDB = getCryptoBalanceCollection()


def updateAllBucketChart():
    for bucket in bucketDB.find({}):
        unit_price = bucket[UNIT_PRICE]
        for item in bucket[PORTFOLIO]:
            bucketDB.update_one(
                {ID: bucket[ID]}, {"$set": {PORTFOLIO + "." + item[ID]: getTickerContribution(item, unit_price)}})


def updateAllTickerCharts():
    for ticker in balanceDB.find({}):
        updateChartOfTicker(ticker)


def updateChartOfTicker():
    pass
