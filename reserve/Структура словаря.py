from datetime import datetime
from time import sleep

def nth_discipline(pos):
    "Возвращает пару (название, описание) из словаря coinDict для курса на n-ной позиции."
    items = list(coinDict.items())
    count = len(list(coinDict.items()))
    return count, items[pos]

coinDict = dict({
    str(datetime.now()):{
        'btc':{
            'price': 32000,
            'count': 100
        }
    }
})

sleep(0.002)

coinDict.update(dict({
    str(datetime.now()):{
        'eth':{
            'price': 22000,
            'count': 200
        }
    }
}))

print(nth_discipline(1))
#print(coinDict)