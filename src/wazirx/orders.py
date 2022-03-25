

from exchange import getCurrentExchange


def placeBuyOrderFromUSDT(tickerId, amount):
    symbol = tickerId+"/USDT"
    orderBook = getCurrentExchange().fetchOrderBook(symbol)
    topBuyPrice = orderBook["bids"][0][0]
    topSellPrice = orderBook["asks"][0][0]
    orderPrice = topBuyPrice+(topSellPrice-topBuyPrice)*.2
    getCurrentExchange().create_limit_buy_order(symbol, amount, orderPrice)


if __name__ == '__main__':
    placeBuyOrderFromUSDT("BTC", 0.00005)
