import requests

if __name__ == '__main__':
    TWO_FACTOR_AUTH_API_KEY = "37bc1f71-8fd4-11ec-a4c2-0200cd936042"
    mobileNumber = "8755919615"
    response = requests.get(f"https://2factor.in/API/V1/{TWO_FACTOR_AUTH_API_KEY}/SMS/{mobileNumber}/AUTOGEN/OTP")
    print(response.text)
