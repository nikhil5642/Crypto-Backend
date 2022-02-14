from turtle import update
from DataBase.MongoDB import getUserInfoCollection
from server.fastApi.modules.liveMarketData import LiveMarketData, getLiveMarketDataInstance
from src.DataFieldConstants import BALANCE, USER_ID, TRANSACTIONS
import uuid

userDB = getUserInfoCollection()


def getAmountByUserId(userId: str, currency: str):
    result = userDB.find_one({USER_ID: int(userId)})
    if result:
        if result[BALANCE][currency]:
            return result[BALANCE][currency]
    return 0


def getMutiCurrencyAmountByUserId(userId: str, currencies: list[str]):
    result = userDB.find_one({USER_ID: int(userId)})
    balance = {}
    if result:
        for currency in currencies:
            if currency in result[BALANCE]:
                balance[currency] = result[BALANCE][currency]
            else:
                balance[currency] = 0
    return balance


def getCompletePortFolio(userId: str):
    result = userDB.find_one({USER_ID: int(userId)})
    if result:
        if result[BALANCE]:
            return result[BALANCE]
    return {}


def updateAmountByUserId(userId: str, newAmount: int, currency: str):
    userDB.update_one(
        {USER_ID: int(userId), "$set": {BALANCE: {currency: newAmount}}})


def exchangeCurrency(userId: str, fromCurrency: str, toCurrency: str, amountInFromCurrency: int,actionType:str):
    # try:
        if(actionType=='buy'):
            exchangeRate = getLiveMarketDataInstance().getExchangeRate(fromCurrency, toCurrency)
            amountInToCurrency = amountInFromCurrency / exchangeRate
        else:
            exchangeRate = getLiveMarketDataInstance().getExchangeRate(toCurrency, fromCurrency)
            amountInToCurrency = amountInFromCurrency * exchangeRate

        currentBalance = getMutiCurrencyAmountByUserId(
            userId, [fromCurrency, toCurrency])
        transactionId = uuid.uuid4().hex
        userDB.update_one({USER_ID: int(userId)},
                          {"$push": {TRANSACTIONS: {"transactionId": transactionId,
                                                    "from": amountInFromCurrency,
                                                    "fromCurrency": fromCurrency,
                                                    "to": amountInToCurrency,
                                                    "toCurrency": toCurrency}},
                           "$set": {BALANCE: {fromCurrency: currentBalance[fromCurrency] - amountInFromCurrency,
                                              toCurrency: currentBalance[toCurrency] + amountInToCurrency}}})
        return True, transactionId
    # except:
    #     return False, ""
