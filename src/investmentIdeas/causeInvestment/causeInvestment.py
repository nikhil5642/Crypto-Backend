import json
import os
from turtle import st
import copy
from src.DataFieldConstants import NAME, TITLE_IMG, ID, BUCKETS
from src.investmentIdeas.buckets.buckets import getBucketsBasicInfo
from typing import List

causeInvestmentList = json.load(
    open(os.path.abspath("./src/investmentIdeas/causeInvestment/CauseInvestmentList.json"), 'r'))


def getInvestInCauseItems(causes: List[str]):
    data = []
    for cause in causes:
        if cause in causeInvestmentList:
            data.append({ID: cause, NAME: causeInvestmentList[cause][NAME],
                        TITLE_IMG: causeInvestmentList[cause][TITLE_IMG]})
    return data


def getCauseItemDetails(causes: str):
    details = copy.deepcopy(causeInvestmentList[causes])
    if BUCKETS in details:
        details[BUCKETS] = getBucketsBasicInfo(details[BUCKETS])
    return details
