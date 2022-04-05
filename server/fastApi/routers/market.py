from typing import List

from fastapi import APIRouter
from pydantic import BaseModel

from server.fastApi.modules.chartData import fetchChartData
from server.fastApi.modules.liveMarketData import getLiveMarketDataInstance
from server.fastApi.modules.tickerDetails import getTickerDetails
from src.DataFieldConstants import RESULT

router = APIRouter(prefix="/market")


class TickerListModel(BaseModel):
    tickers: List[str] = []


class TickerModel(BaseModel):
    tickerId: str = ""


class ChartModel(BaseModel):
    id: str = ""


@router.post("/getTickerLiveData")
async def getTickerLiveData(data: TickerListModel):
    return {RESULT: getLiveMarketDataInstance().getTickersData(data.tickers)}


@router.post("/tickerDetails")
async def tickerDetails(data: TickerModel):
    return {RESULT: getTickerDetails(data.tickerId)}


@router.post("/chartData")
async def chartData(data: ChartModel):
    return {RESULT: fetchChartData(data.id)}


if __name__ == '__main__':
    print(list(["adsf", "dfa"]) is List[str])
