from binance.client import Client
import config

client = Client(config.API_KEY, config.API_SECRET_KEY)
print("logged in")

def get_asset():
    assets = []
    info = client.get_account()
    for i in info['balances']:
        if float(i['free'])>0:
            del i['free']
            del i['locked']
            assets.append(i)
    return assets

print(get_asset())
        
