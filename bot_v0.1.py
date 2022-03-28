from binance.spot import Spot as Client
from datetime import date, datetime
listCoin = open('listCoin.txt')

dict1 = {}
dict2 = {}
limitRange = 150

for row in listCoin:
    spot_client = Client(base_url="https://api3.binance.com")
    depth_dict = spot_client.depth(row.rstrip(), limit=limitRange)
    del depth_dict["lastUpdateId"]

    print(row.rstrip())
    listValue = []
    price = 100000
    
    for value in depth_dict.values():
        for i in value:
            if (float(i[0])*float(i[1]))>price:
                listValue.append(i)
                ###Здесь словарь должен заполняться данными### 


    print(f"value: {listValue}")

print(f"\n{dict1}")
print("COMPLITE!")