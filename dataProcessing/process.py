import json
import os


def generateCoinTagListFromListing():
    data = json.load(open(os.path.abspath("./CoinListingResponse.json"), 'r'))
    result = {}
    for item in data["data"]:
        result[item["symbol"]] = item["tags"]
    with open('CoinTagList.json', 'w') as fp:
        json.dump(result, fp)


generateCoinTagListFromListing()
