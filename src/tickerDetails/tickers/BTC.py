from src.dataObjects.generalDataMapping import StabilityGraph
from src.tickerDetails.tickerItems.generalInfo import GeneralInfo


def getBTCData():
    data = []
    data.append(GeneralInfo("BTC").getJson())
    data.append(StabilityGraph(2, 3, 5, 8, 9))
    return data
