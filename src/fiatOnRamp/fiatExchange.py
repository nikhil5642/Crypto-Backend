
import json
from time import sleep
from DataBase.MongoDB import getUSDTFiatCollection
from DataBase.RedisDB import getRedisInstance
from src.DataFieldConstants import FIAT, ID, NAME, PRICE, TEMPLATE


fiatDB = getUSDTFiatCollection()
redis_client = getRedisInstance()

currencyTemplates = {
    'inr': '₹ %s',
    'usdt': '%s USDT'
}


def updateFiatCurrencyInCache():
    while True:
        result = {}
        result['usdt'] = {PRICE: 1, NAME: "Tether",
                          TEMPLATE: getCurrencyTemplate('usdt')}
        for fiat in fiatDB.find({}):
            result[fiat[FIAT]] = {PRICE: fiat[PRICE],
                                  NAME: fiat[NAME],
                                  TEMPLATE: getCurrencyTemplate(fiat[FIAT])}
        redis_client.set("fiatExchangeData", json.dumps(result))
        sleep(5*60)


def getFiatCurruncyData():
    result = []
    data = json.loads(redis_client.get("fiatExchangeData"))
    for fiat in data:
        item = data[fiat]
        item[ID] = fiat
        result.append(item)
    return result


def getSingleFiatCurruncyData(currency):
    data = json.loads(redis_client.get("fiatExchangeData"))[currency]
    data[ID] = currency
    return data


def getCurrencyTemplate(currency):
    return currencyTemplates[str(currency).lower()]
