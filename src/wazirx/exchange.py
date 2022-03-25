import ccxt
exchange = ccxt.wazirx(
    {
        'api_key': 'hAp3UhNZNVi0SvAcVuLjbe6CKTI3MxjVeNimN865ITP7kAtPoEJ8yaQvW83Ac2HN',
        'secret': 'ibLJSsdulz24aXIwyOUtqWSQeYEjxnvgQfmSm0ru'
    })


def getCurrentExchange():
    return exchange
