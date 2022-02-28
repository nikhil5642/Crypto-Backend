from unicodedata import name
from fastapi import APIRouter
from pydantic import BaseModel
from server.fastApi.modules.liveMarketData import LiveMarketData, getLiveMarketDataInstance
from server.fastApi.modules.tickerDetails import getTickerDetails

from src.DataFieldConstants import RESULT
from typing import List

router = APIRouter(prefix="/market")


class TickerListModel(BaseModel):
    tickers: List[str] = []


class TickerModel(BaseModel):
    tickerId: str = ""


@router.post("/getTickerLiveData")
async def getTickerLiveData(data: TickerListModel):
    return {RESULT: getLiveMarketDataInstance().getTickersData(data.tickers)}


@router.post("/tickerDetails")
async def tickerDetails(data: TickerModel):
    return {RESULT: getTickerDetails(data.tickerId)}

if __name__ == '__main__':
    print(list(["adsf", "dfa"]) is List[str])
