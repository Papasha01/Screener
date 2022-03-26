from binance.client import Client

ls = open('listCoin', 'w')


api_key = "xxx"
api_secret = "xxx"

client = Client(api_key, api_secret)
exchange_info = client.get_exchange_info()
for s in exchange_info['symbols']:
    if "USDT"in str(s['symbol']):
        ls.write(s['symbol'] + "\n")
        print(s['symbol'])
ls.close()
print('Conplite!')