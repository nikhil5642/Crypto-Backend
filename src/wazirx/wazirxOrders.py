from time import sleep

from ccxt.base.errors import InsufficientFunds, InvalidOrder, RateLimitExceeded

from DataBase.MongoDB import getCryptoBalanceCollection
from src.DataFieldConstants import ID, PENDING, BALANCE, LAST_PRICE
from src.logger.logger import GlobalLogger
from src.wazirx.exchange import getWazirXClient

balanceDB = getCryptoBalanceCollection()


def placeBuyOrderFromUSDT(tickerId, amount):
    symbol = tickerId + "/USDT"
    orderBook = getWazirXClient().fetchOrderBook(symbol)
    topBuyPrice = orderBook["bids"][0][0]
    topSellPrice = orderBook["asks"][0][0]
    buyRate = topBuyPrice + (topSellPrice - topBuyPrice) * .5
    if buyRate * amount < 2:
        GlobalLogger().error("Can't process, less than 2 USDT")
        return
    try:
        order = getWazirXClient().create_limit_buy_order(symbol, amount, buyRate)
        sleep(60)
        orderExecuted = verifyOrderExecution(order)
        if not orderExecuted:
            cancel_order(order)
        else:
            balanceDB.update_one({ID: tickerId}, {
                "$set": {LAST_PRICE: buyRate},
                "$inc": {PENDING: -amount, BALANCE: amount}})

    except InsufficientFunds:
        GlobalLogger().error("insufficientFund")
    except InvalidOrder:
        GlobalLogger().error("invalid order")
    except Exception:
        GlobalLogger().error("Exception Occured ")


def placeSellOrderToUSDT(tickerId, amount):
    symbol = tickerId + "/USDT"
    orderBook = getWazirXClient().fetchOrderBook(symbol)
    topBuyPrice = orderBook["bids"][0][0]
    topSellPrice = orderBook["asks"][0][0]
    sellRate = topBuyPrice + (topSellPrice - topBuyPrice) * .5

    if sellRate * amount < 2:
        GlobalLogger().error("insufficientFund")
    try:
        order = getWazirXClient().create_limit_sell_order(symbol, amount, sellRate)
        sleep(60)
        orderExecuted = verifyOrderExecution(order)
        if not orderExecuted:
            cancel_order(order)
        else:
            balanceDB.update_one({ID: tickerId}, {
                "$set": {LAST_PRICE: sellRate},
                "$inc": {PENDING: amount, BALANCE: -amount}})

    except InsufficientFunds:
        GlobalLogger().error("insufficientFund")
    except InvalidOrder:
        GlobalLogger().error("invalid order")
    except Exception:
        GlobalLogger().error("Exception Occurred")


def verifyOrderExecution(curOrder):
    try:
        openOrders = getWazirXClient().fetch_open_orders()
        for order in openOrders:
            if curOrder == order:
                return False
        return True
    except Exception:
        return verifyOrderExecution(curOrder)


def cancel_order(curOrder):
    try:
        getWazirXClient().cancel_order(
            id=curOrder["id"], symbol=curOrder["symbol"])
    except RateLimitExceeded:
        cancel_order(curOrder)


if __name__ == '__main__':
    placeBuyOrderFromUSDT("BTC", 0.00005)
