from server.fastApi.modules.login import generateAuthorisation, getUserIdByAuth


if __name__ == '__main__':

    for i in range(1, 100):
        auth = generateAuthorisation()
        # login(auth,"12345"+str(i))
        print(getUserIdByAuth(auth))
