from server.fastApi.modules.login import generateAuthorisation, getUserIdByAuth
from server.fastApi.modules.portfolio import getCreditsByUserId


if __name__ == '__main__':
    getCreditsByUserId("1")
