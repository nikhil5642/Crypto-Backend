import json
import pprint

from exchange import getCurrentExchange
exchange = getCurrentExchange()
# out = exchange.fetch_ticker('BTC/USDT')
out = exchange.fetch_balance()
print(out["USDT"])
# out = exchange.fetch_trades('BTC/USDT')
# out = exchange.load_markets()
# out = exchange.fetchOrderBook('BTC/USDT')
# pprint.pprint(out)
