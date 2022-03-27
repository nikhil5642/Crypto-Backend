import json
import uuid
from DataBase.MongoDB import getBucketsCollection, getBucketsTransactionCollection, getUserInfoCollection

from DataBase.RedisDB import getRedisInstance
from server.fastApi.modules.portfolio import getMultiCurrencyAmountByUserId
from src.DataFieldConstants import AMOUNT_IN_USDT, AMOUNT_PER_UNIT, BALANCE, BUCKET_ID, BUCKETS, FREE, ID, INVESTED, ORDER_TYPE, PORTFOLIO, TRANSACTIONID, TRANSACTIONS, UNIT_PRICE, UNITS, USDT, USER_ID
from src.wazirx.orders import placeBuyOrderFromUSDT
redis_client = getRedisInstance()

bucketDB = getBucketsCollection()
bucketTransactionDB = getBucketsTransactionCollection()
userDB = getUserInfoCollection()


def buyPartOfBucket(userId: str, bucketId: str, amountInUSDT):
    bucket = bucketDB.find_one({ID: bucketId})
    buyBuketPrice = bucket[UNIT_PRICE]*1.001
    bucketUnitsAlloted = amountInUSDT/buyBuketPrice
    transactionId = uuid.uuid4().hex
    bucketDB.update_one(
        {ID: bucketId}, {"$set": {FREE: bucket[FREE]-bucketUnitsAlloted, INVESTED: bucket[INVESTED]+bucketUnitsAlloted}})
    bucketTransactionDB.insert_one(
        {ORDER_TYPE: "buy", TRANSACTIONID: transactionId, USER_ID: userId, BUCKET_ID: bucketId, UNITS: bucketUnitsAlloted, AMOUNT_IN_USDT: amountInUSDT})

    currentBalance = getMultiCurrencyAmountByUserId(
        userId, [bucketId, USDT])
    userDB.update_one({USER_ID: int(userId)},
                      {"$push": {TRANSACTIONS: {TRANSACTIONID: transactionId,
                                                BUCKET_ID: bucketId,
                                                UNITS: bucketUnitsAlloted,
                                                AMOUNT_IN_USDT: amountInUSDT,
                                                ORDER_TYPE: "buy"}},
                       "$set": {BALANCE + "." + bucketId: currentBalance[bucketId] + bucketUnitsAlloted,
                                BALANCE + "." + USDT: currentBalance[USDT] - amountInUSDT}})


def rebalanceBucketBalance(bucketId: str):
    pass
