import json
import os

from src.DataFieldConstants import SIMETRI, TOKEN_INSIGHT
from src.dataObjects.polarGraphItem import PolarGraphItem, PolarGraphDataItem

fundamentals = json.load(open(os.path.abspath(
    "./src/assets/CoinFundamentals.json"), 'r'))


def TickerRatings(tickerId: str):
    raw_ratings = loadTickerRatingsFromFile(tickerId)
    if raw_ratings is None:
        return None
    elif raw_ratings['provider'] == SIMETRI:
        return getSimitriRating(raw_ratings)
    elif raw_ratings['provider'] == TOKEN_INSIGHT:
        return getTokenInsightRating(raw_ratings)
    else:
        return None


def loadTickerRatingsFromFile(tickerId: str):
    if tickerId in fundamentals:
        return fundamentals[tickerId].get("rating", None)
    return None


def getSimitriRating(ratings):
    return PolarGraphItem("Stability Graph",
                          [PolarGraphDataItem("OPPORTUNITY", ratings['opportunity']),
                           PolarGraphDataItem(
                               "ECOSYSTEM", ratings['ecosystem']),
                           # PolarGraphDataItem(
                           #     "PERFORMANCE", ratings['performance']),
                           PolarGraphDataItem("TEAM", ratings['team']),
                           PolarGraphDataItem(
                               "TECHNOLOGY", ratings['technology']),
                           PolarGraphDataItem("PROGRESS", ratings['progress'])
                           ]).getJson()


def getTokenInsightRating(ratings):
    return PolarGraphItem("Stability Graph",
                          [PolarGraphDataItem("ECOSYSTEM", ratings['ecosystem']),
                           PolarGraphDataItem("TEAM", ratings['team']),
                           PolarGraphDataItem(
                               "TECHNOLOGY", ratings['technology'])
                           ]).getJson()
