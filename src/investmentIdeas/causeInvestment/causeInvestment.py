from calendar import c
from turtle import st
import copy
from unicodedata import category
from DataBase.MongoDB import getInvestmentCategoriesCollection
from src.DataFieldConstants import NAME, TITLE_IMG, ID, BUCKETS, DESCRIPTION, SHORT_DESCRIPTION
from src.investmentIdeas.buckets.buckets import getBucketsBasicInfo
from typing import List

categoryDB = getInvestmentCategoriesCollection()


def getInvestInCauseItems(causes: List[str]):
    data = []
    for category in categoryDB.find({ID: {'$in': causes}}):
        data.append({ID: category[ID], NAME: category[NAME], SHORT_DESCRIPTION: category[SHORT_DESCRIPTION],
                     TITLE_IMG: category[TITLE_IMG]})
    return data


def getCauseItemDetails(cause: str):
    details = categoryDB.find({ID: cause})[0]
    details.pop("_id")
    if BUCKETS in details:
        details[BUCKETS] = getBucketsBasicInfo(details[BUCKETS])
    return details
