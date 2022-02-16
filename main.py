import json
import os

if __name__ == '__main__':
    data = json.load(open(os.path.abspath("./src/tickerDetails/tickerItems/CoinList.json"), 'r'))
    print(data["BTC"])
