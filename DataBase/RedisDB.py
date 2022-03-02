import redis


class RedisManager:
    __instance = None

    @staticmethod
    def getInstance():
        if RedisManager.__instance == None:
            RedisManager()
        return RedisManager.__instance

    def __init__(self):
        if RedisManager.__instance != None:
            raise Exception("This class is a singleton!")
        else:
            RedisManager.__instance = redis.Redis(
                host='localhost', port=6379, db=0)


def getRedisInstance():
    return RedisManager.getInstance()
