import json

import requests

from src.DataFieldConstants import ID, RATING, SIMETRI, TAGS, TOKEN_INSIGHT


def updateFundamentals():
    url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest?start=1&limit=5000&convert=INR"

    payload = {}
    headers = {
        'X-CMC_PRO_API_KEY': '8ac04e5d-477c-44c4-a58e-3e4f82e3253f'
    }

    response = requests.request("GET", url, headers=headers, data=payload)
    if response.status_code != 200:
        return
    response = response.json()
    data = {}
    for i, item in enumerate(response["data"]):
        data[item["symbol"]] = {TAGS: item[TAGS],
                                RATING: getFundamentalAnlysis(item[ID])}
        if i % 100 == 0:
            with open('./src/assets/CoinFundamentals.json', 'w') as f:
                json.dump(data, f)
                print(f"saved upto {i} items")
    with open('./src/assets/CoinFundamentals.json', 'w') as f:
        json.dump(data, f)
    print("Saved whole data")


def getFundamentalAnlysis(cmc_id):
    simetriAnalysis = getSimetriAnalysis(cmc_id)
    if simetriAnalysis != None:
        return simetriAnalysis

    tokenInsightAnalysis = getTokenInsightAnalysis(cmc_id)
    if tokenInsightAnalysis != None:
        return tokenInsightAnalysis
    return None


def getSimetriAnalysis(cmc_id):
    """Return simitri analysis of Ticker.

    Keyword arguments:
    cmc_id -- coin market cap coin id
    """
    try:
        url = "https://api.simetri.cryptobriefing.com/v1/reports_by_cmc_id/" + \
              str(cmc_id)

        payload = {}
        headers = {
            'TOKEN': 'gBvDmnj1KTb8urXw',
            'Origin': 'https://coinmarketcap.com'
        }
        item = requests.request(
            "GET", url, headers=headers, data=payload).json()["reports"][0]["array"][0]
        return {"provider": SIMETRI,
                "overall": item["number_grade"],
                "opportunity": item["market_opportunity_grade"],
                "ecosystem": item["ecosystem_structure_grade"],
                "performance": item["token_performance_grade"],
                "team": item["core_team_grade"],
                "technology": item["underlying_technology_grade"],
                "progress": item["roadmap_progress_grade"], }
    except:
        return None


def getTokenInsightAnalysis(cmc_id):
    """Return Token Insight analysis of a Ticker.

    Keyword arguments:
    cmc_id -- coin market cap coin id
    """
    try:
        url = "https://tokeninsight.com/wapiv2/widget/selectCmcWidgetLevelInfo"

        payload = {}
        params = {"cmcId": str(cmc_id)}
        headers = {
            'Host': 'tokeninsight.com'
        }

        item = requests.request(
            "POST", url, headers=headers, data=payload, params=params).json()["levelInfo"]
        overallScore = sum([getGradeValue(grade)
                            for grade in item["levelResult"]]) / len(item["levelResult"])
        return {"provider": TOKEN_INSIGHT,
                "overall": overallScore,
                "ecosystem": item["ecologyScore"],
                "team": item["teamScore"],
                "technology": item["subjectScore"], }
    except:
        return None


def getGradeValue(grade):
    if (grade == "A"):
        return 95
    elif (grade == "B"):
        return 80
    elif (grade == "C"):
        return 65
    elif (grade == "D"):
        return 50


if __name__ == "__main__":
    updateFundamentals()
