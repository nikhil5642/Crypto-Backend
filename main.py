import copy
import json

from DataBase.MongoDB import getBucketsCollection
if __name__ == '__main__':
    bucketDB = getBucketsCollection()
    for bucket in bucketDB.find({}):
        print(bucket)
