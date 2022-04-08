import uuid

from DataBase.MongoDB import getLoginInfoCollection, getUserInfoCollection
from src.DataFieldConstants import MOBILE_NUMBER, USER_ID, AUTHORISATION, USDT_BALANCE

loginDB = getLoginInfoCollection()
userDB = getUserInfoCollection()


def processLogin(mobileNumber):
    auth = generateAuthorisation()
    if checkExistingLogin(auth, mobileNumber):
        return auth, False  # Is not new user
    else:
        setNewLogin(auth, mobileNumber)
        return auth, True  # Is new user


def setNewLogin(auth, mobNum):
    userId = userDB.count_documents({}) + 1
    loginDB.insert_one(
        {MOBILE_NUMBER: mobNum, USER_ID: userId, AUTHORISATION: auth})
    userDB.insert_one(
        {MOBILE_NUMBER: mobNum, USER_ID: userId, USDT_BALANCE: 0})


def verifyAuth(auth):
    result = loginDB.find_one({AUTHORISATION: auth})
    if result:
        return True
    return False


def getUserIdByAuth(auth):
    result = loginDB.find_one({AUTHORISATION: auth})
    if result:
        return result[USER_ID]
    return None


def checkExistingLogin(auth, mobNum):
    if mobNum:
        result = loginDB.update_one({MOBILE_NUMBER: mobNum}, {
            "$set": {AUTHORISATION: auth}})
        if result.matched_count > 0:
            return True
    return False


def generateAuthorisation():
    return uuid.uuid4().hex
