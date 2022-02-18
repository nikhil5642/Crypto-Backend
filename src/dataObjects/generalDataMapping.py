from src.dataObjects.polarGraphItem import PolarGraphItem, PolarGraphDataItem


def StabilityGraph(value: int, past: int, future: int, health: int, usage: int):
    return PolarGraphItem("Stability Graph", [PolarGraphDataItem("VALUE", value),
                                              PolarGraphDataItem(
                                                  "FUTURE", future),
                                              PolarGraphDataItem("PAST", past),
                                              PolarGraphDataItem(
                                                  "HEALTH", health),
                                              PolarGraphDataItem("USEAGE", usage)]).getJson()
