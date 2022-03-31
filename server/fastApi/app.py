import threading

from fastapi import FastAPI
from starlette.staticfiles import StaticFiles

from src.investmentIdeas.buckets.bucketOrders import checkAndFillAllPendingOrders
from src.investmentIdeas.buckets.buckets import updateBucketsInCache
from .routers import auth, market, portfolio, ideas

app = FastAPI()

app.include_router(auth.router)
app.include_router(market.router)
app.include_router(portfolio.router)
app.include_router(ideas.router)

app.mount("/assets", StaticFiles(directory="assets"), name="assets")

threading.Thread(
    target=updateBucketsInCache, args=()).start()
threading.Thread(
    target=checkAndFillAllPendingOrders, args=()).start()


@app.get("/")
async def root():
    return {"message": "Hello Bigger Applications!"}
