from src.tickerDetails.tickerDataMappings import Info, StablityGraph


def getBTCData():
    data = []
    data.append(Info(
        "BITCOIN", "Started by sathoshi nakamoto as a modern way of peer to peer payment"))
    data.append(StablityGraph(2, 3, 5, 8, 9))
    return data
