from fastapi import APIRouter
from pydantic import BaseModel

from src.investmentIdeas.causeInvestment.causeInvestment import getCauseItemDetails, getInvestInCauseItems

router = APIRouter(prefix="/ideas")


class CauseIdeas(BaseModel):
    userId: str


class CauseIdeasDetails(BaseModel):
    userId: str
    categoryId: str


@router.post("/causeIdeas")
async def causeIdeas(causeItem: CauseIdeas):
    return getInvestInCauseItems(["metaverse", "lending", "payments"])


@router.post("/causeIdeaDetails")
async def causeIdeaDetails(causeItem: CauseIdeasDetails):
    return getCauseItemDetails(causeItem.categoryId)


if __name__ == '__main__':
    print(list(["adsf", "dfa"]) is list[str])
