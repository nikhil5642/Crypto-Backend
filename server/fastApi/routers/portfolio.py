from typing import List

from fastapi import APIRouter
from pydantic import BaseModel

from server.fastApi.modules.portfolio import exchangeCurrency, getCompletePortFolio, getRecentTransactions, \
    getBalanceByUserId
from src.DataFieldConstants import SUCCESS, TOTAL_INVESTED_VALUE, TRANSACTIONID, DATA, TOTAL_PORTFOLIO_VALUE

router = APIRouter(prefix="/portfolio")


class TickerListModel(BaseModel):
    tickers: List[str] = []


class PortFolioModel(BaseModel):
    userId: str
    currency: str


class BalanceModel(BaseModel):
    userId: str


class ExcangeCurrencyModel(BaseModel):
    userId: str
    fromCurrency: str
    toCurrency: str
    amount: float
    actionType: str


class MutliCurrencyPortFolioModel(BaseModel):
    userId: str
    currencies: List[str]


class RecentTransactions(BaseModel):
    userId: str


@router.post("/getRemainingAmount")
async def getRemainingAmount(portfolio: BalanceModel):
    return getBalanceByUserId(portfolio.userId)


#
# @router.post("/getMultipleCurrencyBalance")
# async def getMultipleCurrencyBalance(portfolio: MutliCurrencyPortFolioModel):
#     return getMultiCurrencyAmountByUserId(portfolio.userId, portfolio.currencies)
#

@router.post("/getCompletePortFolio")
async def getPortFolio(portfolio: PortFolioModel):
    portfolioItems, totalInvestment = getCompletePortFolio(portfolio.userId)
    return {TOTAL_INVESTED_VALUE: totalInvestment, DATA: portfolioItems}


@router.post("/exchangeCurrency")
async def exchange(exchange: ExcangeCurrencyModel):
    success, transactionId = exchangeCurrency(exchange.userId, exchange.fromCurrency,
                                              exchange.toCurrency, exchange.amount, exchange.actionType)
    return {SUCCESS: success, TRANSACTIONID: transactionId}


@router.post("/getRecentTransactions")
async def getPortFolio(transactions: RecentTransactions):
    return {DATA: getRecentTransactions(transactions.userId)}


if __name__ == '__main__':
    print(list(["adsf", "dfa"]) is List[str])
