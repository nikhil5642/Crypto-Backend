from DataBase.MongoDB import getBucketsCollection
from src.investmentIdeas.buckets.bucketOrders import buyPartOfBucket
from src.wazirx.orders import placeBuyOrderFromUSDT
if __name__ == '__main__':
    # bucketDB = getBucketsCollection()
    # for bucket in bucketDB.find({}):
    #     print(bucket)
    buyPartOfBucket(1, "bucket_x", 1)
