from fastapi import APIRouter
from pydantic import BaseModel

from server.fastApi.modules.login import getUserIdByAuth, processLogin, verifyAuth
from src.DataFieldConstants import AUTHORISATION, SUCCESS, USER_ID

router = APIRouter(prefix="/auth")


class LoginModel(BaseModel):
    mobileNumber: str


class VerifyAuthModel(BaseModel):
    auth: str


@router.post("/login")
async def login(data: LoginModel):
    return {AUTHORISATION: processLogin(data.mobileNumber)}


@router.post("/verify")
async def verify(data: VerifyAuthModel):
    return {SUCCESS: verifyAuth(data.auth)}


@router.post("/userId")
async def verify(data: VerifyAuthModel):
    return {USER_ID: getUserIdByAuth(data.auth)}
