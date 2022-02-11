from unicodedata import name
from fastapi import APIRouter
from pydantic import BaseModel
from server.fastApi.modules.liveMarketData import LiveMarketData
from server.fastApi.modules.tickerDetails import getTickerDetails

from src.DataFieldConstants import RESULT

router = APIRouter(prefix="/market")
liveMarketData = LiveMarketData()
liveMarketData.fetchAndUpdateLiveMarketData()


class TickerListModel(BaseModel):
    tickers: list[str] = []


@router.post("/getTickerLiveData")
async def getTickerLiveData(data: TickerListModel):
    return {RESULT: liveMarketData.getTickersData(data.tickers)}


@router.post("/getTickerDetails")
async def getTickerLiveData(tickerId: str):
    return {RESULT: getTickerDetails(tickerId)}

if __name__ == '__main__':
    print(list(["adsf", "dfa"]) is list[str])
