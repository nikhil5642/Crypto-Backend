from unicodedata import category
from fastapi import APIRouter
from pydantic import BaseModel
from src.investmentIdeas.buckets.buckets import getBucketDetail, getBucketsBasicInfo
from typing import List

from src.investmentIdeas.causeInvestment.causeInvestment import getCauseItemDetails, getInvestInCauseItems

router = APIRouter(prefix="/ideas")


class CauseIdeas(BaseModel):
    userId: str


class CauseIdeasDetails(BaseModel):
    userId: str
    categoryId: str


class BucketList(BaseModel):
    userId: str


class BucketItem(BaseModel):
    userId: str
    bucketId: str


@router.post("/causeIdeas")
async def causeIdeas(causeItem: CauseIdeas):
    return getInvestInCauseItems(["metaverse", "lending", "payments"])


@router.post("/causeIdeaDetails")
async def causeIdeaDetails(causeItem: CauseIdeasDetails):
    return getCauseItemDetails(causeItem.categoryId)


@router.post("/bucketsList")
async def causeIdeaDetails(bucket: BucketList):
    return getBucketsBasicInfo(["bucket_x", "bucket_y", "bucket_m"])


@router.post("/bucketDetails")
async def causeIdeaDetails(bucket: BucketItem):
    return getBucketDetail(bucket.bucketId)

if __name__ == '__main__':
    print(list(["adsf", "dfa"]) is List[str])
