
from DataBase.MongoDB import getUserInfoCollection
from src.DataFieldConstants import CREDITS, USER_ID

userDB = getUserInfoCollection()


def getCreditsByUserId(userId: str):
    result = userDB.find_one({USER_ID: int(userId)})
    print("result", result, userId)
    if(result):
        return result[CREDITS]
    return 0


def updateCreditsByUserId(userId: str, newCredit: int):
    result = userDB.update_one(
        {USER_ID: int(userId), "$set": {CREDITS: newCredit}})
    print("result", result, userId)
    if(result):
        return result[CREDITS]
    return 0
