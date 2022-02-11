from fastapi import APIRouter
from pydantic import BaseModel
from server.fastApi.modules.liveMarketData import LiveMarketData

from server.fastApi.modules.portfolio import getAmountByUserId, getMutiCurrencyAmountByUserId, getCompletePortFolio

from src.DataFieldConstants import RESULT

router = APIRouter(prefix="/portfolio")
liveMarketData = LiveMarketData()
liveMarketData.fetchAndUpdateLiveMarketData()


class TickerListModel(BaseModel):
    tickers: list[str] = []


class PortFolioModel(BaseModel):
    userId: str
    currency: str


class MutliCurrencyPortFolioModel(BaseModel):
    userId: str
    currencies: list[str]


@router.post("/getRemainingAmount")
async def getRemainingAmount(portfolio: PortFolioModel):
    return getAmountByUserId(portfolio.userId, portfolio.currency)


@router.post("/getMultipleCurrencyBalance")
async def getMultipleCurrencyBalance(portfolio: MutliCurrencyPortFolioModel):
    return getMutiCurrencyAmountByUserId(portfolio.userId, portfolio.currencies)


@router.post("/getCompletePortFolio")
async def getPortFolio(portfolio: PortFolioModel):
    return getCompletePortFolio(portfolio.userId)

if __name__ == '__main__':
    print(list(["adsf", "dfa"]) is list[str])
