import copy
from datetime import date, datetime
import json
import threading
from tkinter import CURRENT
from tokenize import Double
from typing import List
from DataBase.MongoDB import getLiveMarketCollection
from DataBase.RedisDB import getRedisInstance
import pickle
import numpy as np
import pandas as pd
import requests
from src.DataFieldConstants import CHANGE, DAY, ID, LAST_UPDATED, MONTH, NAME, PRICE, VOLATILITY, WEEK, YEAR

baseUrl = "https://min-api.cryptocompare.com"
redis_instance = getRedisInstance()


def fetchChartData(id):
    current = redis_instance.get(id+"_ChartData")
    if current is None:
        return {}
    else:
        return json.loads(current)


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
        current = redis_instance.get(tickerId+"_ChartData")
        if current is None:
            current = {}
        else:
            current = json.loads(current)
        current[DAY] = df.iloc[-96:].to_json(orient="records")
        redis_instance.set(tickerId+"_ChartData", json.dumps(current))


def updateWeeklyAndMonthlyData(tickerId, data):
    df = copy.deepcopy(data)
    df.drop(["volumeto", "volumefrom", "conversionType",
             "conversionSymbol"], axis=1, inplace=True)

    current = redis_instance.get(tickerId+"_ChartData")
    if current is None:
        current = {}
    else:
        current = json.loads(current)
    current[WEEK] = df.iloc[-168:].to_json(orient="records")
    current[MONTH] = df.iloc[-720:].to_json(orient="records")
    redis_instance.set(tickerId+"_ChartData", json.dumps(current))


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
        current = redis_instance.get(tickerId+"_ChartData")
        if current is None:
            current = {}
        else:
            current = json.loads(current)
        current[YEAR] = df.iloc[-365:].to_json(orient="records")
        redis_instance.set(tickerId+"_ChartData", json.dumps(current))
