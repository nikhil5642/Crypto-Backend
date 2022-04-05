import copy
import json

import pandas as pd
import requests

from DataBase.RedisDB import getRedisInstance
from src.DataFieldConstants import DAY, ID, MONTH, WEEK, YEAR

baseUrl = "https://min-api.cryptocompare.com"
redis_instance = getRedisInstance()


def fetchChartData(id):
    current = redis_instance.get(id + "_ChartData")
    if current is None:
        return {}
    else:
        current = json.loads(current)
        current.pop(ID, None)
        return current


def updateOneDayData(tickerId):
    endPoint = "/data/v2/histominute"
    params = {"fsym": tickerId,
              "tsym": "INR",
              "limit": 2000,
              "toTs": -1}
    response = requests.get(baseUrl + endPoint, params=params)
    if response.status_code == 200:
        df = pd.DataFrame(response.json()["Data"]["Data"])
        df.drop(["volumeto", "volumefrom", "conversionType",
                 "conversionSymbol"], axis=1, inplace=True)
        df['time'] = pd.to_datetime(
            df['time'], unit='s')
        df.index = df["time"]
        df = df.resample("15min").agg(
            {'open': 'first', 'close': 'last', 'high': 'max', 'low': 'min'})
        df.reset_index(inplace=True)
        current = redis_instance.get(tickerId + "_ChartData")
        if current is None:
            current = {}
        else:
            current = json.loads(current)

        current[DAY] = json.loads(df.iloc[-96:].to_json(orient="records"))
        for index, item in enumerate(current[DAY]):
            item['time'] = round(item['time'] / 1000)
            current[DAY][index] = item
        redis_instance.set(tickerId + "_ChartData", json.dumps(current))


def updateWeeklyAndMonthlyData(tickerId, data):
    df = copy.deepcopy(data)
    df.drop(["volumeto", "volumefrom", "conversionType",
             "conversionSymbol"], axis=1, inplace=True)

    current = redis_instance.get(tickerId + "_ChartData")
    if current is None:
        current = {}
    else:
        current = json.loads(current)
    current[WEEK] = json.loads(df.iloc[-168:].to_json(orient="records"))
    current[MONTH] = json.loads(df.iloc[-720:].to_json(orient="records"))
    redis_instance.set(tickerId + "_ChartData", json.dumps(current))


def updateOneYearData(tickerId):
    endPoint = "/data/v2/histoday"
    params = {"fsym": tickerId,
              "tsym": "INR",
              "limit": 400,
              "toTs": -1}
    response = requests.get(baseUrl + endPoint, params=params)
    if response.status_code == 200:
        df = pd.DataFrame(response.json()["Data"]["Data"])
        df.drop(["volumeto", "volumefrom", "conversionType",
                 "conversionSymbol"], axis=1, inplace=True)
        current = redis_instance.get(tickerId + "_ChartData")
        if current is None:
            current = {}
        else:
            current = json.loads(current)
        current[YEAR] = json.loads(df.iloc[-365:].to_json(orient="records"))
        redis_instance.set(tickerId + "_ChartData", json.dumps(current))
