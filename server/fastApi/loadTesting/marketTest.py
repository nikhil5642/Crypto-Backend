from locust import between, HttpUser, task


class WebsiteUser(HttpUser):
    wait_time = between(1, 5)

    @task
    def mainPage(self):
        self.client.get(url='/')

    @task
    def liveData(self):
        self.client.post(url='/market/getTickerLiveData', json={"tickers": ['BTC', 'ETH', 'XRP', 'AVAX', 'USDT']})
