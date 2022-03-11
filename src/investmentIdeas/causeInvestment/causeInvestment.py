import json
from datetime import datetime
from typing import List

from DataBase.MongoDB import getInvestmentCategoriesCollection
from DataBase.RedisDB import getRedisInstance
from src.DataFieldConstants import NAME, TITLE_IMG, ID, BUCKETS, SHORT_DESCRIPTION
from src.investmentIdeas.buckets.buckets import getBucketsBasicInfo

categoryDB = getInvestmentCategoriesCollection()

redis_client = getRedisInstance()


def getInvestInCauseItems(categories: List[str]):
    data = []
    updateRedisDataBase()

    for category in categories:
        category_data = redis_client.get(category + "_Category")
        if category_data is not None:
            category_data = json.loads(category_data)
            data.append(
                {ID: category_data[ID], NAME: category_data[NAME], SHORT_DESCRIPTION: category_data[SHORT_DESCRIPTION],
                 TITLE_IMG: category_data[TITLE_IMG]})
    return data


def updateRedisDataBase():
    lastUpdated = redis_client.get("categoryInfoLastFetched")
    if lastUpdated is None or (datetime.now() - datetime.fromtimestamp(float(lastUpdated))).total_seconds() > 3600:
        for category in categoryDB.find({}):
            category.pop("_id")
            redis_client.set(category[ID] + "_Category", json.dumps(category))
            redis_client.set(
                "categoryInfoLastFetched", datetime.timestamp(datetime.now()))


def getCauseItemDetails(category: str):
    details = json.loads(redis_client.get(category + "_Category"))
    if BUCKETS in details:
        details[BUCKETS] = getBucketsBasicInfo(details[BUCKETS])
    return details
