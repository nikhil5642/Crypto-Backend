from src.DataFieldConstants import AMOUNT_PER_UNIT, ID
from src.investmentIdeas.buckets.bucketContribution import getTickerContribution
from src.investmentIdeas.buckets.bucketOrders import buyOneBucketFromExchange

if __name__ == '__main__':
    # updateAllBucketUnitPrice()
    buyOneBucketFromExchange("bucket_x")
    # sellOneBucketFromExchange("bucket_x")
    # item = {ID: "BTC", AMOUNT_PER_UNIT: 0.0000}
    # print(getTickerContribution(item, 2))
