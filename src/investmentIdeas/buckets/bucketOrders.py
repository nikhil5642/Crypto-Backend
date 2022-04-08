import threading
import uuid
from time import sleep

from DataBase.MongoDB import getBucketsCollection, getBucketsTransactionCollection, getUserInfoCollection, \
    getCryptoBalanceCollection
from DataBase.RedisDB import getRedisInstance
from server.fastApi.modules.portfolio import getBalanceByUserId
from src.DataFieldConstants import AMOUNT_IN_USDT, BALANCE, BUCKET_ID, FREE, ID, INVESTED, \
    ORDER_TYPE, PORTFOLIO, TRANSACTIONID, TRANSACTIONS, UNIT_PRICE, UNITS, USER_ID, PENDING, AMOUNT_PER_UNIT, \
    LAST_PRICE, USDT_BALANCE, INVESTMENTS
from src.logger.logger import GlobalLogger
from src.wazirx.wazirxOrders import placeBuyOrderFromUSDT, placeSellOrderToUSDT

redis_client = getRedisInstance()

bucketDB = getBucketsCollection()
bucketTransactionDB = getBucketsTransactionCollection()
userDB = getUserInfoCollection()
balanceDB = getCryptoBalanceCollection()


def buyPartOfBucket(userId: str, bucketId: str, amountInUSDT):
    currentBalance = getBalanceByUserId(userId)
    transactionId = uuid.uuid4().hex

    if currentBalance < amountInUSDT:
        return False, transactionId, "Insufficient Balance"
    bucket = bucketDB.find_one({ID: bucketId})
    buyBuketPrice = bucket[UNIT_PRICE] * 1.001
    bucketUnitsAllotted = amountInUSDT / buyBuketPrice
    bucketDB.update_one(
        {ID: bucketId},
        {"$inc": {FREE: -bucketUnitsAllotted, INVESTED: bucketUnitsAllotted}})
    bucketTransactionDB.insert_one(
        {ORDER_TYPE: "buy", TRANSACTIONID: transactionId, USER_ID: userId, BUCKET_ID: bucketId,
         UNITS: bucketUnitsAllotted, AMOUNT_IN_USDT: amountInUSDT})

    userDB.update_one({USER_ID: int(userId)},
                      {"$push": {TRANSACTIONS: {TRANSACTIONID: transactionId,
                                                BUCKET_ID: bucketId,
                                                UNITS: bucketUnitsAllotted,
                                                AMOUNT_IN_USDT: amountInUSDT,
                                                ORDER_TYPE: "buy"}},
                       "$inc": {INVESTMENTS + "." + bucketId + "." + UNITS: bucketUnitsAllotted,
                                INVESTMENTS + "." + bucketId + "." + INVESTED: amountInUSDT,
                                USDT_BALANCE: -amountInUSDT}})
    if bucket[FREE] - bucketUnitsAllotted < 0.5:
        buyOneBucketFromExchange(bucketId)
    return True, transactionId, "Transaction Successfull"


def sellPartOfBucket(userId: str, bucketId: str, amountInBucket):
    transactionId = uuid.uuid4().hex
    currentBalance = getBalanceByUserId(userId)
    if currentBalance < amountInBucket:
        return False, transactionId, "Insufficient Balance"
    bucket = bucketDB.find_one({ID: bucketId})
    sellBuketPrice = bucket[UNIT_PRICE] * 0.999
    usdtRefunded = amountInBucket * sellBuketPrice
    bucketDB.update_one(
        {ID: bucketId},
        {"$inc": {FREE: amountInBucket, INVESTED: - amountInBucket}})
    bucketTransactionDB.insert_one(
        {ORDER_TYPE: "sell", TRANSACTIONID: transactionId, USER_ID: userId, BUCKET_ID: bucketId,
         UNITS: amountInBucket, AMOUNT_IN_USDT: usdtRefunded})

    userDB.update_one({USER_ID: int(userId)},
                      {"$push": {TRANSACTIONS: {TRANSACTIONID: transactionId,
                                                BUCKET_ID: bucketId,
                                                UNITS: amountInBucket,
                                                AMOUNT_IN_USDT: usdtRefunded,
                                                ORDER_TYPE: "sell"}},
                       "$inc": {INVESTMENTS + "." + bucketId + "." + UNITS: -amountInBucket,
                                USDT_BALANCE: usdtRefunded},
                       "$set": {INVESTMENTS + "." + bucketId + "." + INVESTED: 0}})

    if bucket[FREE] + amountInBucket > 2:
        sellOneBucketFromExchange(bucketId)

    return True, transactionId, "Transaction Successful"


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
    bucketDB.update_one({ID: bucketId}, {
        "$inc": {FREE: 1}})


def sellOneBucketFromExchange(bucketId: str):
    portfolio = bucketDB.find_one({ID: bucketId})[PORTFOLIO]
    for ticker in portfolio:
        balanceDB.update_one({ID: ticker[ID]}, {
            "$inc": {PENDING: -ticker[AMOUNT_PER_UNIT]}})
    bucketDB.update_one({ID: bucketId}, {
        "$inc": {FREE: -1}})


def checkAndFillAllPendingOrders():
    GlobalLogger().info("Check and Fill pending orders service started")
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
