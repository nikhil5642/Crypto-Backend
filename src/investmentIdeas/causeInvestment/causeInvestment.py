import json
import os
from turtle import st

from src.DataFieldConstants import NAME, TITLE_IMG, ID

causeInvestmentList = json.load(
    open(os.path.abspath("./src/investmentIdeas/causeInvestment/CauseInvestmentList.json"), 'r'))


def getInvestInCauseItems(causes: list[str]):
    data = []
    for cause in causes:
        if cause in causeInvestmentList:
            data.append({ID: cause, NAME: causeInvestmentList[cause][NAME],
                        TITLE_IMG: causeInvestmentList[cause][TITLE_IMG]})
    return data


def getCauseItemDetails(causes: str):
    return causeInvestmentList[causes]
