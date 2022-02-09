import uuid
from DataBase.MongoDB import getLoginInfoCollection, getUserInfoCollection
from SRC.DataFieldName import mobileNumber, userID, authorisation

loginDB = getLoginInfoCollection()
userDB = getUserInfoCollection()


def processLogin(mobileNumber):
    auth = generateAuthorisation()
    if(checkExistingLogin(auth, mobileNumber)):
        return auth
    else:
        setNewLogin(auth, mobileNumber)
        return auth


def setNewLogin(auth, mobNum):
    userId = userDB.count_documents({})+1
    loginDB.insert_one(
        {mobileNumber: mobNum, userID: userId, authorisation: auth})
    userDB.insert_one({mobileNumber: mobNum, userID: userId})


def verifyAuth(auth):
    result = loginDB.find_one({authorisation: auth})
    if(result):
        return True
    return False


def getUserIdByAuth(auth):
    result = loginDB.find_one({authorisation: auth})
    if(result):
        return result[userID]
    return None


def checkExistingLogin(auth, mobNum):
    if(mobNum):
        result = loginDB.update_one({mobileNumber: mobNum}, {
                                    "$set": {authorisation: auth}})
        if(result.matched_count > 0):
            return True
    return False


def generateAuthorisation():
    return uuid.uuid4().hex
