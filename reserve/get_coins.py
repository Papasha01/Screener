import requests

content = requests.get("https://api.binance.com/api/v3/exchangeInfo").json()
content = content.get("symbols")
symbols = []
for thing in content:
    if thing.get("status") == "TRADING" and thing.get("isSpotTradingAllowed") == True:
        symbols.append(thing.get("symbol"))

ls = []
for s in symbols:
    if "USDT"in str(s):
        ls.append(s)
print(ls)
print(len(ls))