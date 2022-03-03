import copy
import json
import requests
import pandas as pd
from dateutil import tz
if __name__ == '__main__':
    response = requests.get(
        "https://min-api.cryptocompare.com/data/v2/histohour?fsym=BTC&tsym=INR&limit=2000")
    df = pd.DataFrame(response.json()["Data"]["Data"])
    df.drop(["volumeto", "volumefrom", "conversionType",
            "conversionSymbol"], axis=1, inplace=True)
    # df['time'] = pd.to_datetime(
    #     df['time'], unit='s')
    # df.index = df["time"]
    # df = df.resample("15min").agg(
    #     {'open': 'first', 'close': 'last', 'high': 'max', 'low': 'min'})
    # df.reset_index(inplace=True)
    print(df.head())
    data = df.iloc[-2:].to_json(orient="records")
    print(data)
