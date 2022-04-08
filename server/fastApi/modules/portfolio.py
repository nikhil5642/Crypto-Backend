import uuid

from DataBase.MongoDB import getUserInfoCollection
from server.fastApi.modules.liveMarketData import getExchangeRate, getNameAndExchangeRate
from src.DataFieldConstants import BALANCE, ID, NAME, PRICE, QUANTITY, USER_ID, TRANSACTIONS, USDT_BALANCE, \
    INVESTMENTS, UNITS

userDB = getUserInfoCollection()


def getBalanceByUserId(userId: str):
    result = userDB.find_one({USER_ID: int(userId)})
    if result:
        return result[USDT_BALANCE]
    return 0


#
# def getMultiCurrencyAmountByUserId(userId: str, currencies: List[str]):
#     result = userDB.find_one({USER_ID: int(userId)})
#     balance = {}
#     if result:
#         for currency in currencies:
#             if currency in result[BALANCE]:
#                 balance[currency] = result[BALANCE][currency]
#             else:
#                 balance[currency] = 0
#     return balance


def getCompletePortFolio(userId: str):
    userInfo = userDB.find_one({USER_ID: int(userId)})
    result = []
    totalInvestedValue = 0
    if userInfo:
        if INVESTMENTS in userInfo:
            for ticker in userInfo[INVESTMENTS]:
                name, exchangeRate = getNameAndExchangeRate(ticker)
                result.append(
                    {NAME: name, ID: ticker, PRICE: exchangeRate, QUANTITY: userInfo[INVESTMENTS][ticker][UNITS]})
                totalInvestedValue += userInfo[INVESTMENTS][ticker][UNITS]
            return result, totalInvestedValue
    return [], totalInvestedValue


def getRecentTransactions(userId: str):
    result = userDB.find_one({USER_ID: int(userId)})
    if result:
        if TRANSACTIONS in result:
            return result[TRANSACTIONS]
    return []


def updateAmountByUserId(userId: str, newAmount: int, currency: str):
    userDB.update_one(
        {USER_ID: int(userId), "$set": {BALANCE: {currency: newAmount}}})


def exchangeCurrency(userId: str, fromCurrency: str, toCurrency: str, amountInFromCurrency: int, actionType: str):
    try:
        if actionType == 'buy':
            exchangeRate = getExchangeRate(toCurrency, fromCurrency)
            amountInToCurrency = amountInFromCurrency / exchangeRate
        else:
            exchangeRate = getExchangeRate(fromCurrency, toCurrency)
            amountInToCurrency = amountInFromCurrency * exchangeRate

        currentBalance = getMultiCurrencyAmountByUserId(
            userId, [fromCurrency, toCurrency])
        transactionId = uuid.uuid4().hex
        userDB.update_one({USER_ID: int(userId)},
                          {"$push": {TRANSACTIONS: {"transactionId": transactionId,
                                                    "from": amountInFromCurrency,
                                                    "fromCurrency": fromCurrency,
                                                    "to": amountInToCurrency,
                                                    "toCurrency": toCurrency,
                                                    "actionType": actionType}},
                           "$set": {BALANCE + "." + fromCurrency: currentBalance[fromCurrency] - amountInFromCurrency,
                                    BALANCE + "." + toCurrency: currentBalance[toCurrency] + amountInToCurrency}})
        return True, transactionId
    except:
        return False, ""
