import json
from ccxt.base.errors import InsufficientFunds, InvalidOrder
from src.wazirx.exchange import getCurrentExchange


def placeBuyOrderFromUSDT(tickerId, amount):
    symbol = tickerId+"/USDT"
    orderBook = getCurrentExchange().fetchOrderBook(symbol)
    topBuyPrice = orderBook["bids"][0][0]
    topSellPrice = orderBook["asks"][0][0]
    orderPrice = topBuyPrice+(topSellPrice-topBuyPrice)*.2
    if orderPrice*amount < 2:
        return False
    try:
        getCurrentExchange().create_limit_buy_order(symbol, amount, orderPrice)
        return True
    except InsufficientFunds:
        print("insufficientFund")
    except InvalidOrder:
        print("invalid order")
    return False


if __name__ == '__main__':
    placeBuyOrderFromUSDT("BTC", 0.00005)
