import threading

from src.investmentIdeas.buckets.bucketOrders import checkAndFillAllPendingOrders
from src.investmentIdeas.buckets.bucketUnitPrice import updateAllBucketUnitPrice
from src.investmentIdeas.buckets.buckets import updateBucketsInCache

threading.Thread(
    target=updateBucketsInCache, args=()).start()
threading.Thread(
    target=checkAndFillAllPendingOrders, args=()).start()
threading.Thread(
    target=updateAllBucketUnitPrice, args=()).start()