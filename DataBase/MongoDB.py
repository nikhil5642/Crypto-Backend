import os

from pymongo import MongoClient

MONGO_DB_NAME = "visa_mongo_db"


class MongoDBCollections:
    USER_INFO_COLLECTION = "user_info"
    LOGIN_INFO_COLLECTION = "login_info"
    BUCKET_COLLECTION = "buckets"
    INVESTMETN_CATEGORIES_COLLECTION = "invest_categories"
    LIVE_MARKET_COLLECTION = "live_market"


class MongoManager:
    __instance = None

    @staticmethod
    def getInstance():
        if MongoManager.__instance == None:
            MongoManager()
        return MongoManager.__instance

    def __init__(self):
        if MongoManager.__instance != None:
            raise Exception("This class is a singleton!")
        else:
            uri = "mongodb+srv://realmcluster.ndjcn.mongodb.net/myFirstDatabase?authSource=%24external&authMechanism=MONGODB-X509&retryWrites=true&w=majority"
            client = MongoClient(uri,
                                 tls=True,
                                 tlsCertificateKeyFile=os.path.abspath("./DataBase/mongo.pem"))
            MongoManager.__instance = client[MONGO_DB_NAME]


def getCollection():
    return MongoManager.getInstance()


def getUserInfoCollection():
    return MongoManager.getInstance()[MongoDBCollections.USER_INFO_COLLECTION]


def getLoginInfoCollection():
    return MongoManager.getInstance()[MongoDBCollections.LOGIN_INFO_COLLECTION]


def getBucketsCollection():
    return MongoManager.getInstance()[MongoDBCollections.BUCKET_COLLECTION]


def getInvestmentCategoriesCollection():
    return MongoManager.getInstance()[MongoDBCollections.INVESTMETN_CATEGORIES_COLLECTION]


def getLiveMarketCollection():
    return MongoManager.getInstance()[MongoDBCollections.LIVE_MARKET_COLLECTION]


if __name__ == '__main__':
    db = MongoManager.getInstance()
    userInfoCollection = db[MongoDBCollections.USER_INFO_COLLECTION]
    print(userInfoCollection.find_one({"userId": 1}))
