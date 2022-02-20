import json
import os
from turtle import st

from src.DataFieldConstants import NAME, TITLE_IMG, ID

buckets = json.load(
    open(os.path.abspath("./src/investmentIdeas/buckets/BucketList.json"), 'r'))


def getBucketsBasicInfo(bucketIds: list[str]):
    data = []
    for bucketId in bucketIds:
        if bucketId in buckets:
            data.append({ID: bucketId, NAME: buckets[bucketId][NAME],
                        TITLE_IMG: buckets[bucketId][TITLE_IMG]})
    return data


def getBucketDetail(bucketId: str):
    return buckets[bucketId]
