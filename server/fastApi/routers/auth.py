import requests
from fastapi import APIRouter
from pydantic import BaseModel

from server.fastApi.modules.login import getUserIdByAuth, processLogin, verifyAuth
from src.DataFieldConstants import AUTHORISATION, SUCCESS, USER_ID, SESSION_ID

router = APIRouter(prefix="/auth")


class SendOTPModel(BaseModel):
    mobileNumber: str


class VerifyOTPModel(BaseModel):
    mobileNumber: str
    sessionId: str
    otp: str


class VerifyAuthModel(BaseModel):
    auth: str


TWO_FACTOR_AUTH_API_KEY = "37bc1f71-8fd4-11ec-a4c2-0200cd936042"


@router.post("/sendOTP")
async def login(data: SendOTPModel):
    response = requests.get(
        f"https://2factor.in/API/V1/{TWO_FACTOR_AUTH_API_KEY}/SMS/{data.mobileNumber}/AUTOGEN/OTP").json()
    if response["Status"] == "Success":
        return {SUCCESS: True, SESSION_ID: response["Details"]}

    return {SUCCESS: False}


@router.post("/verifyOTP")
async def login(data: VerifyOTPModel):
    response = requests.get(
        f"https://2factor.in/API/V1/{TWO_FACTOR_AUTH_API_KEY}/SMS/VERIFY/{data.sessionId}/{data.otp}").json()
    if response["Status"] == "Success":
        return {SUCCESS: True, AUTHORISATION: processLogin(data.mobileNumber)}
    return {SUCCESS: False}


@router.post("/verify")
async def verify(data: VerifyAuthModel):
    return {SUCCESS: verifyAuth(data.auth)}


@router.post("/userId")
async def verify(data: VerifyAuthModel):
    return {USER_ID: getUserIdByAuth(data.auth)}
