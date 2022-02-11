
from DataBase.MongoDB import getUserInfoCollection
from src.DataFieldConstants import BALANCE, USER_ID

userDB = getUserInfoCollection()


def getAmountByUserId(userId: str, currency: str):
    result = userDB.find_one({USER_ID: int(userId)})
    if(result):
        if(result[BALANCE][currency]):
            return result[BALANCE][currency]
    return 0


def getMutiCurrencyAmountByUserId(userId: str, currencies: list[str]):
    result = userDB.find_one({USER_ID: int(userId)})
    balance = {}
    if(result):
        for currency in currencies:
            if(result[BALANCE][currency]):
                balance[currency] = result[BALANCE][currency]
            else:
                balance[currency] = 0
    return balance


def getCompletePortFolio(userId: str):
    result = userDB.find_one({USER_ID: int(userId)})
    if(result):
        if(result[BALANCE]):
            return result[BALANCE]
    return {}


def updateAmountByUserId(userId: str, newAmount: int, currency: str):
    userDB.update_one(
        {USER_ID: int(userId), "$set": {BALANCE: {currency: newAmount}}})
