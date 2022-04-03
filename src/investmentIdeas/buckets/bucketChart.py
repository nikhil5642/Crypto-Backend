
import json
from time import sleep
import requests
from DataBase.MongoDB import getBucketsCollection, getChartDataCollection, getCryptoBalanceCollection
from src.DataFieldConstants import AMOUNT_PER_UNIT, ID, ONE_MONTH, ONE_WEEK, ONE_YEAR, PORTFOLIO, SIX_MONTH, THREE_MONTH, UNIT_PRICE
import pandas as pd

from src.investmentIdeas.buckets.bucketContribution import getTickerContribution

bucketDB = getBucketsCollection()
balanceDB = getCryptoBalanceCollection()
chartDataDB = getChartDataCollection()


def updateAllBucketChart():
    while True:
        for bucket in bucketDB.find({}):
            updateBucketChartData(bucket)
        sleep(12*60*60)


def updateBucketChartData(bucket):
    one_week = None
    one_month = None
    three_month = None
    six_month = None
    one_year = None

    for item in bucket[PORTFOLIO]:
        current_item_chartData = getChartData(item[ID])
        current_one_week = pd.DataFrame(current_item_chartData[ONE_WEEK])
        current_one_month = pd.DataFrame(current_item_chartData[ONE_MONTH])
        current_three_month = pd.DataFrame(current_item_chartData[THREE_MONTH])
        current_six_month = pd.DataFrame(current_item_chartData[SIX_MONTH])
        current_one_year = pd.DataFrame(current_item_chartData[ONE_YEAR])
        if one_week is None:
            one_week = current_one_week
            one_month = current_one_month
            three_month = current_three_month
            six_month = current_six_month
            one_year = current_one_year
            for col in ['high', 'low', 'open', 'close']:
                one_week[col] *= item[AMOUNT_PER_UNIT]
                one_month[col] *= item[AMOUNT_PER_UNIT]
                three_month[col] *= item[AMOUNT_PER_UNIT]
                six_month[col] *= item[AMOUNT_PER_UNIT]
                one_year[col] *= item[AMOUNT_PER_UNIT]
        else:
            for col in ['high', 'low', 'open', 'close']:
                one_week[col] += item[AMOUNT_PER_UNIT]*current_one_week[col]
                one_month[col] += item[AMOUNT_PER_UNIT]*current_one_month[col]
                three_month[col] += item[AMOUNT_PER_UNIT] * \
                    current_three_month[col]
                six_month[col] += item[AMOUNT_PER_UNIT]*current_six_month[col]
                one_year[col] += item[AMOUNT_PER_UNIT]*current_one_year[col]
    chartDataDB.update_one(
        {ID: bucket[ID]}, {'$set': {ONE_YEAR: json.loads(one_year.to_json(orient="records")),
                                    SIX_MONTH: json.loads(six_month.to_json(orient="records")),
                                    THREE_MONTH: json.loads(three_month.to_json(orient="records")),
                                    ONE_MONTH: json.loads(one_month.to_json(orient="records")),
                                    ONE_WEEK: json.loads(one_week.to_json(orient="records"))}}, upsert=True)


def getChartData(id):
    result = chartDataDB.find_one({ID: id})
    if result:
        return result
    else:
        return None


def updateAllTickerCharts():
    while True:
        for ticker in balanceDB.find({}):
            updateChartOfTicker(ticker[ID])
        sleep(6*60*60)


def updateChartOfTicker(tickerId):
    one_day_candles_data = getOneDayCandlesData(tickerId)
    one_hour_candles_data = getOneHourCandlesData(tickerId)
    one_yr = one_day_candles_data[-365:]
    six_month = one_day_candles_data[-182:]
    three_month = one_day_candles_data[-90:]
    one_month = one_hour_candles_data[-720:]
    one_week = one_hour_candles_data[-168:]
    chartDataDB.update_one(
        {ID: tickerId}, {'$set': {ONE_YEAR: one_yr,
                                  SIX_MONTH: six_month,
                                  THREE_MONTH: three_month,
                                  ONE_MONTH: one_month,
                                  ONE_WEEK: one_week}}, upsert=True)


def getOneDayCandlesData(tickerId):
    url = "https://min-api.cryptocompare.com/data/v2/histoday"
    params = {"fsym": tickerId,
              "tsym": "USD",
              "limit": 400,
              "toTs": -1}
    response = requests.get(url, params=params)
    if response.status_code == 200:
        df = pd.DataFrame(response.json()["Data"]["Data"])
        df.drop(["volumeto", "volumefrom", "conversionType",
                 "conversionSymbol"], axis=1, inplace=True)
        return json.loads(df.to_json(orient="records"))
    else:
        print("Unable to fetch 1Day candles data, retrying")
        return getOneDayCandlesData(tickerId)


def getOneHourCandlesData(tickerId):
    url = "https://min-api.cryptocompare.com/data/v2/histohour"
    params = {"fsym": tickerId,
              "tsym": "USD",
              "limit": 800,
              "toTs": -1}
    response = requests.get(url, params=params)
    if response.status_code == 200:
        df = pd.DataFrame(response.json()["Data"]["Data"])
        df.drop(["volumeto", "volumefrom", "conversionType",
                 "conversionSymbol"], axis=1, inplace=True)
        return json.loads(df.to_json(orient="records"))
    else:
        print("Unable to fetch 1Hour candles data, retrying")
        return getOneDayCandlesData(tickerId)
