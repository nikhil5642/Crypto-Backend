from h11 import Data
from src.DataFieldConstants import DATA, DESCRIPTION, ITEM_TYPE, NAME, VALUES


class GeneralInfo:
    ITEM_TYPE = "GeneralInfo"

    def __init__(self, name: str, description: str):
        self.DATA = {NAME: name, DESCRIPTION: description}

    def getJson(self):
        return{
            ITEM_TYPE: self.ITEM_TYPE,
            DATA: self.DATA
        }


if __name__ == '__main__':
    print(GeneralInfo("title", "dsfakljalsjfk;a").getJson())
