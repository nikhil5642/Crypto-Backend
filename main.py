from server.fastApi.modules.portfolio import exchangeCurrency


if __name__ == '__main__':
    print(exchangeCurrency(1, "INR", "BTC", 1000))
