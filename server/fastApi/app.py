from fastapi import FastAPI

from .routers import auth, market, portfolio

app = FastAPI()

app.include_router(auth.router)
app.include_router(market.router)
app.include_router(portfolio.router)


@app.get("/")
async def root():
    return {"message": "Hello Bigger Applications!"}
