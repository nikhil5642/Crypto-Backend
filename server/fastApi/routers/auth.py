import requests
from fastapi import APIRouter
from pydantic import BaseModel

from server.fastApi.modules.login import getUserIdByAuth, processLogin, verifyAuth
from src.DataFieldConstants import AUTHORISATION, SUCCESS, USER_ID, SESSION_ID,NEW_USER

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
    if data.mobileNumber == "9999999999" or data.mobileNumber =="8888888888" : #for testing purpous
         return {SUCCESS: True, SESSION_ID: "testing"}
    
    response = requests.get(
        f"https://2factor.in/API/V1/{TWO_FACTOR_AUTH_API_KEY}/SMS/{data.mobileNumber}/AUTOGEN/OTP").json()
    if response["Status"] == "Success":
        return {SUCCESS: True, SESSION_ID: response["Details"]}

    return {SUCCESS: False}


@router.post("/verifyOTP")
async def login(data: VerifyOTPModel):
    if data.mobileNumber == "9999999999" : #for testing purpous
        auth,newUser=processLogin(data.mobileNumber)
        return {SUCCESS: True, AUTHORISATION: auth,NEW_USER:False}
    elif data.mobileNumber == "8888888888" : #for testing purpous
        auth,newUser=processLogin(data.mobileNumber)
        return {SUCCESS: True, AUTHORISATION: auth,NEW_USER:True}
    
    response = requests.get(
        f"https://2factor.in/API/V1/{TWO_FACTOR_AUTH_API_KEY}/SMS/VERIFY/{data.sessionId}/{data.otp}").json()
    if response["Status"] == "Success":
        auth,newUser=processLogin(data.mobileNumber)
        return {SUCCESS: True, AUTHORISATION: auth,NEW_USER:newUser}
    return {SUCCESS: False}


@router.post("/verify")
async def verify(data: VerifyAuthModel):
    return {SUCCESS: verifyAuth(data.auth)}


@router.post("/userId")
async def verify(data: VerifyAuthModel):
    return {USER_ID: getUserIdByAuth(data.auth)}
