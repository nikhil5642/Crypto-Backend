import threading
import uuid
from time import sleep

from DataBase.MongoDB import getBucketsCollection, getBucketsTransactionCollection, getUserInfoCollection, \
    getCryptoBalanceCollection
from DataBase.RedisDB import getRedisInstance
from server.fastApi.modules.portfolio import getMultiCurrencyAmountByUserId
from src.DataFieldConstants import AMOUNT_IN_USDT, BALANCE, BUCKET_ID, FREE, ID, INVESTED, \
    ORDER_TYPE, PORTFOLIO, TRANSACTIONID, TRANSACTIONS, UNIT_PRICE, UNITS, USDT, USER_ID, PENDING, AMOUNT_PER_UNIT, \
    LAST_PRICE
from src.logger.logger import GlobalLogger
from src.wazirx.wazirxOrders import placeBuyOrderFromUSDT, placeSellOrderToUSDT

redis_client = getRedisInstance()

bucketDB = getBucketsCollection()
bucketTransactionDB = getBucketsTransactionCollection()
userDB = getUserInfoCollection()
balanceDB = getCryptoBalanceCollection()


def buyPartOfBucket(userId: str, bucketId: str, amountInUSDT):
    currentBalance = getMultiCurrencyAmountByUserId(
        userId, [bucketId, USDT])
    if currentBalance[USDT] < amountInUSDT:
        return False, "Insufficient Balance"
    bucket = bucketDB.find_one({ID: bucketId})
    buyBuketPrice = bucket[UNIT_PRICE] * 1.001
    bucketUnitsAllotted = amountInUSDT / buyBuketPrice
    transactionId = uuid.uuid4().hex
    bucketDB.update_one(
        {ID: bucketId},
        {"$set": {FREE: bucket[FREE] - bucketUnitsAllotted, INVESTED: bucket[INVESTED] + bucketUnitsAllotted}})
    bucketTransactionDB.insert_one(
        {ORDER_TYPE: "buy", TRANSACTIONID: transactionId, USER_ID: userId, BUCKET_ID: bucketId,
         UNITS: bucketUnitsAllotted, AMOUNT_IN_USDT: amountInUSDT})

    userDB.update_one({USER_ID: int(userId)},
                      {"$push": {TRANSACTIONS: {TRANSACTIONID: transactionId,
                                                BUCKET_ID: bucketId,
                                                UNITS: bucketUnitsAllotted,
                                                AMOUNT_IN_USDT: amountInUSDT,
                                                ORDER_TYPE: "buy"}},
                       "$set": {BALANCE + "." + bucketId: currentBalance[bucketId] + bucketUnitsAllotted,
                                BALANCE + "." + USDT: currentBalance[USDT] - amountInUSDT}})
    if bucket[FREE] - bucketUnitsAllotted < 1:
        buyOneBucketFromExchange(bucketId)


def sellPartOfBucket(userId: str, bucketId: str, amountInBucket):
    currentBalance = getMultiCurrencyAmountByUserId(
        userId, [bucketId, USDT])
    if currentBalance[bucketId] < amountInBucket:
        return False, "Insufficient Balance"
    bucket = bucketDB.find_one({ID: bucketId})
    sellBuketPrice = bucket[UNIT_PRICE] * 0.999
    usdtRefunded = amountInBucket * sellBuketPrice
    transactionId = uuid.uuid4().hex
    bucketDB.update_one(
        {ID: bucketId},
        {"$set": {FREE: bucket[FREE] + amountInBucket, INVESTED: bucket[INVESTED] - amountInBucket}})
    bucketTransactionDB.insert_one(
        {ORDER_TYPE: "sell", TRANSACTIONID: transactionId, USER_ID: userId, BUCKET_ID: bucketId,
         UNITS: amountInBucket, AMOUNT_IN_USDT: usdtRefunded})

    userDB.update_one({USER_ID: int(userId)},
                      {"$push": {TRANSACTIONS: {TRANSACTIONID: transactionId,
                                                BUCKET_ID: bucketId,
                                                UNITS: amountInBucket,
                                                AMOUNT_IN_USDT: usdtRefunded,
                                                ORDER_TYPE: "sell"}},
                       "$set": {BALANCE + "." + bucketId: currentBalance[bucketId] - amountInBucket,
                                BALANCE + "." + USDT: currentBalance[USDT] + usdtRefunded}})
    if bucket[FREE] + amountInBucket > 2:
        sellOneBucketFromExchange(bucketId)


def buyOneBucketFromExchange(bucketId: str):
    portfolio = bucketDB.find_one({ID: bucketId})[PORTFOLIO]
    for ticker in portfolio:
        result = balanceDB.update_one({ID: ticker[ID]}, {
            "$inc": {PENDING: ticker[AMOUNT_PER_UNIT]}})
        if not result.matched_count > 0:
            balanceDB.insert_one({ID: ticker[ID],
                                  BALANCE: 0,
                                  PENDING: ticker[AMOUNT_PER_UNIT],
                                  LAST_PRICE: 0, })


def sellOneBucketFromExchange(bucketId: str):
    portfolio = bucketDB.find_one({ID: bucketId})[PORTFOLIO]
    for ticker in portfolio:
        balanceDB.update_one({ID: ticker[ID]}, {
            "$inc": {PENDING: -ticker[AMOUNT_PER_UNIT]}})


def checkAndFillAllPendingOrders():
    GlobalLogger().error("checkAndFillAllPendingOrders")
    while True:
        for ticker in balanceDB.find({}):
            if ticker[PENDING] != 0:
                threading.Thread(
                    target=processOrder, args=(ticker,)).start()
                sleep(5)
        sleep(60)


def processOrder(ticker):
    if ticker[PENDING] > 0:
        placeBuyOrderFromUSDT(ticker[ID], ticker[PENDING])
    elif abs(ticker[PENDING]) <= ticker[BALANCE]:
        placeSellOrderToUSDT(ticker[ID], -ticker[PENDING])
    else:
        GlobalLogger().error(f"Insufficient {ticker[ID]} balance")
