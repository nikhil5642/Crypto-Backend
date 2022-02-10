from fastapi import APIRouter
from pydantic import BaseModel
from server.fastApi.modules.liveMarketData import LiveMarketData
from server.fastApi.modules.portfolio import getCreditsByUserId

from src.DataFieldConstants import CREDITS, RESULT

router = APIRouter(prefix="/portfolio")
liveMarketData = LiveMarketData()
liveMarketData.fetchAndUpdateLiveMarketData()


class TickerListModel(BaseModel):
    tickers: list[str] = []


class PortFolioModel(BaseModel):
    userId: str


@router.post("/getRemainingCredits")
async def getTickerLiveData(portfolio: PortFolioModel):
    return {CREDITS: getCreditsByUserId(portfolio.userId)}


if __name__ == '__main__':
    print(list(["adsf", "dfa"]) is list[str])
