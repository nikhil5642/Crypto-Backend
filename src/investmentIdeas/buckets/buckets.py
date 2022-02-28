import json
import os
from turtle import st

from src.DataFieldConstants import NAME, TITLE_IMG, ID, CATEGORY, RETURN_ONE_YR, RETURN_THREE_YR, MIN_AMOUNT, RISK_LEVEL, SHORT_DESCRIPTION
from typing import List

buckets = json.load(
    open(os.path.abspath("./src/investmentIdeas/buckets/BucketList.json"), 'r'))


def getBucketsBasicInfo(bucketIds: List[str]):
    data = []
    for bucketId in bucketIds:
        if bucketId in buckets:
            data.append({ID: bucketId, NAME: buckets[bucketId][NAME], CATEGORY: buckets[bucketId][CATEGORY],
                        SHORT_DESCRIPTION: buckets[bucketId][SHORT_DESCRIPTION],
                        RETURN_ONE_YR: buckets[bucketId][RETURN_ONE_YR],
                        RETURN_THREE_YR: buckets[bucketId][RETURN_THREE_YR],
                        MIN_AMOUNT: buckets[bucketId][MIN_AMOUNT],
                        RISK_LEVEL: buckets[bucketId][RISK_LEVEL],
                        TITLE_IMG: buckets[bucketId][TITLE_IMG]})
    return data


def getBucketDetail(bucketId: str):
    return buckets[bucketId]
