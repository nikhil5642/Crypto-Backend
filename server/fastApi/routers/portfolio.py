from fastapi import APIRouter
from pydantic import BaseModel

from server.fastApi.modules.portfolio import exchangeCurrency, getAmountByUserId, getMutiCurrencyAmountByUserId, getCompletePortFolio

from src.DataFieldConstants import RESULT, SUCCESS, TRANSACTIONID, TRANSACTIONS

router = APIRouter(prefix="/portfolio")


class TickerListModel(BaseModel):
    tickers: list[str] = []


class PortFolioModel(BaseModel):
    userId: str
    currency: str


class ExcangeCurrencyModel(BaseModel):
    userId: str
    fromCurrency: str
    toCurrency: str
    amount: float
    actionType: str


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


@router.post("/exchangeCurrency")
async def exchange(exchange: ExcangeCurrencyModel):
    success, transactionId = exchangeCurrency(exchange.userId, exchange.fromCurrency,
                                             exchange.toCurrency, exchange.amount,exchange.actionType)
    return {SUCCESS: success, TRANSACTIONID: transactionId}

if __name__ == '__main__':
    print(list(["adsf", "dfa"]) is list[str])
