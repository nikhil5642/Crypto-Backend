from src.dataObjects.chartData import ChartData
from src.dataObjects.generalInfo import GeneralInfo
from src.dataObjects.tickerRatings import TickerRatings
from src.dataObjects.tickerTags import TickerTags


def getTickerDetails(tickerId: str):
    data = []
    data.append(GeneralInfo(tickerId).getJson())
    chartData = ChartData(tickerId)
    if chartData.DATA is not None:
        data.append(chartData.getJson())
    data.append(TickerTags(tickerId).getJson())
    ratings = TickerRatings(tickerId)
    if ratings is not None:
        data.append(ratings)
    return data
