from fastapi import FastAPI
from starlette.staticfiles import StaticFiles

from .routers import auth, market, portfolio, ideas

app = FastAPI()

app.include_router(auth.router)
app.include_router(market.router)
app.include_router(portfolio.router)
app.include_router(ideas.router)

app.mount("/assets", StaticFiles(directory="assets"), name="assets")


@app.get("/")
async def root():
    return {"message": "Hello Bigger Applications!"}
