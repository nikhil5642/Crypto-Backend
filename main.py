from src.DataFieldConstants import AMOUNT_PER_UNIT, ID
from src.investmentIdeas.buckets.bucketChart import updateAllBucketChart, updateAllChartsOnCache, updateAllTickerCharts
from src.investmentIdeas.buckets.bucketOrders import buyOneBucketFromExchange
from src.investmentIdeas.buckets.bucketUnitPrice import updateAllBucketUnitPrice
from src.investmentIdeas.buckets.buckets import updateBucketsInCache
from src.wazirx.wazirxOrders import placeBuyOrderFromUSDT

if __name__ == '__main__':
    # updateAllTickerCharts()
    # buyOneBucketFromExchange("bucket_x")
    # sellOneBucketFromExchange("bucket_x")
    # item = {ID: "BTC", AMOUNT_PER_UNIT: 0.0000}
    # print(getTickerContribution(item, 2))
    # updateAllBucketChart()
    updateAllChartsOnCache()
