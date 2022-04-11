import threading
from time import sleep
from src.fiatOnRamp.fiatExchange import updateFiatCurrencyInCache
from src.investmentIdeas.buckets.bucketChart import updateAllBucketChart, updateAllChartsOnCache, updateAllTickerCharts

from src.investmentIdeas.buckets.bucketOrders import checkAndFillAllPendingOrders
from src.investmentIdeas.buckets.bucketUnitPrice import updateAllBucketUnitPrice
from src.investmentIdeas.buckets.buckets import updateBucketsInCache

threading.Thread(
    target=updateFiatCurrencyInCache, args=()).start()
threading.Thread(
    target=updateBucketsInCache, args=()).start()
threading.Thread(
    target=checkAndFillAllPendingOrders, args=()).start()
threading.Thread(
    target=updateAllBucketUnitPrice, args=()).start()
threading.Thread(
    target=updateAllTickerCharts, args=()).start()
sleep(5*60)
threading.Thread(
    target=updateAllBucketChart, args=()).start()
threading.Thread(
    target=updateAllChartsOnCache, args=()).start()
