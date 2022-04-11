
from locale import currency
from fastapi import APIRouter
from pydantic import BaseModel

from src.DataFieldConstants import RESULT
from src.fiatOnRamp.fiatExchange import getFiatCurruncyData, getSingleFiatCurruncyData


router = APIRouter(prefix="/fiatExchange")


class SingleFiatRate(BaseModel):
    id: str


@router.get("/fiatList")
async def fiatList():
    return {RESULT: getFiatCurruncyData()}


@router.post("/fiatCurrentRate")
async def fiatCurrentRate(fiat: SingleFiatRate):
    return {RESULT: getSingleFiatCurruncyData(fiat.id)}
