import ccxt

api_key = 'hAp3UhNZNVi0SvAcVuLjbe6CKTI3MxjVeNimN865ITP7kAtPoEJ8yaQvW83Ac2HN'
api_secret = 'ibLJSsdulz24aXIwyOUtqWSQeYEjxnvgQfmSm0ru'

exchange = ccxt.wazirx(
    {
        'api_key': api_key,
        'secret': api_secret
    })


def getWazirXClient():
    return exchange
