from server.fastApi.modules.login import generateAuthorisation, getUserIdByAuth
from server.fastApi.modules.portfolio import getCreditsByUserId
from server.fastApi.modules.tickerDetails import getTickerDetails


if __name__ == '__main__':
    print(getTickerDetails("BTC"))
