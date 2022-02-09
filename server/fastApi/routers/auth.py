from fastapi import APIRouter
from pydantic import BaseModel

from server.fastApi.modules.login import getUserIdByAuth, processLogin, verifyAuth
from SRC.DataFieldName import authorisation, success, userID

router = APIRouter(prefix="/auth")


class LoginModel(BaseModel):
    mobileNumber: str


class VerifyAuthModel(BaseModel):
    auth: str


@router.post("/login")
async def login(data: LoginModel):
    return {authorisation: processLogin(data.mobileNumber)}


@router.post("/verify")
async def verify(data: VerifyAuthModel):
    return {success: verifyAuth(data.auth)}


@router.post("/userId")
async def verify(data: VerifyAuthModel):
    return {userID: getUserIdByAuth(data.auth)}
