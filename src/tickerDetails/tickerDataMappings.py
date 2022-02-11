from src.tickerDetails.tickerItems.polarGraphItem import PolarGraphDataItem, PolarGraphItem
from src.tickerDetails.tickerItems.generalInfo import GeneralInfo


def StablityGraph(value: int, past: int, future: int, health: int, usage: int):
    return PolarGraphItem("Stability Graph", [PolarGraphDataItem("VALUE", value),
                                              PolarGraphDataItem(
                                                  "FUTURE", future),
                                              PolarGraphDataItem("PAST", past),
                                              PolarGraphDataItem(
                                                  "HEALTH", health),
                                              PolarGraphDataItem("USEAGE", usage)]).getJson()


def Info(name: str, description: str):
    return GeneralInfo(name, description).getJson()
