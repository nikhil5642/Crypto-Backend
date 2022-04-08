from typing import List

from fastapi import APIRouter
from pydantic import BaseModel

from src.DataFieldConstants import SUCCESS, MESSAGE, TRANSACTIONID
from src.investmentIdeas.buckets.bucketOrders import buyPartOfBucket, sellPartOfBucket
from src.investmentIdeas.buckets.buckets import getBucketDetail, getBucketsBasicInfo
from src.investmentIdeas.causeInvestment.causeInvestment import getCauseItemDetails, getInvestInCauseItems

router = APIRouter(prefix="/ideas")

bucketFunds = ['bucket_x']


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


class FundTransactionItem(BaseModel):
    userId: str
    fundID: str
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


@router.post("/buyFund")
async def buyFund(fund: FundTransactionItem):
    if fund.fundID in bucketFunds:
        return buyBucket(fund)
    return {SUCCESS: False, MESSAGE: "Invalid Fund"}


@router.post("/sellFund")
async def sellFund(fund: FundTransactionItem):
    if fund in bucketFunds:
        return sellBucket(fund)
    return {SUCCESS: False, MESSAGE: "Invalid Fund"}


def buyBucket(bucket: FundTransactionItem):
    success, transactionId, message = buyPartOfBucket(
        bucket.userId, bucket.fundID, bucket.amount)
    return {SUCCESS: success, TRANSACTIONID: transactionId, MESSAGE: message}


def sellBucket(bucket: FundTransactionItem):
    success, transactionId, message = sellPartOfBucket(
        bucket.userId, bucket.fundID, bucket.amount)
    return {SUCCESS: success,  TRANSACTIONID: transactionId, MESSAGE: message}


if __name__ == '__main__':
    print(list(["adsf", "dfa"]) is List[str])
