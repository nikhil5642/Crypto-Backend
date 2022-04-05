from typing import List

from fastapi import APIRouter
from pydantic import BaseModel

from src.DataFieldConstants import SUCCESS, MESSAGE
from src.investmentIdeas.buckets.bucketOrders import buyPartOfBucket, sellPartOfBucket
from src.investmentIdeas.buckets.buckets import getBucketDetail, getBucketsBasicInfo
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


class BucketTransactionItem(BaseModel):
    userId: str
    bucketId: str
    amount: int


@router.post("/causeIdeas")
async def causeIdeas(causeItem: CauseIdeas):
    return getInvestInCauseItems(["metaverse", "lending", "payments"])


@router.post("/causeIdeaDetails")
async def causeIdeaDetails(causeItem: CauseIdeasDetails):
    return getCauseItemDetails(causeItem.categoryId)


@router.post("/bucketsList")
async def causeIdeaDetails(bucket: BucketList):
    return getBucketsBasicInfo(["bucket_x"])


@router.post("/bucketDetails")
async def causeIdeaDetails(bucket: BucketItem):
    return getBucketDetail(bucket.bucketId)


@router.post("/buyBucket")
async def buyBucket(bucket: BucketTransactionItem):
    success, message = buyPartOfBucket(
        bucket.userId, bucket.bucketId, bucket.amount)
    return {SUCCESS: success, MESSAGE: message}


@router.post("/sellBucket")
async def sellBucket(bucket: BucketTransactionItem):
    success, message = sellPartOfBucket(
        bucket.userId, bucket.bucketId, bucket.amount)
    return {SUCCESS: success, MESSAGE: message}


if __name__ == '__main__':
    print(list(["adsf", "dfa"]) is List[str])
