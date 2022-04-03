from binance.spot import Spot as Client
from datetime import datetime, time, timedelta
from time import sleep

delta = timedelta(seconds=5)
newListCoin1 = []
fullListCoin = []
price = 400000
cf = 0.9

def GetDataCoin():
    listNameCoin = open('listNameCoin.txt')
    for row in listNameCoin:
        spot_client = Client(base_url="https://api1.binance.com")
        depth_dict = spot_client.depth(row.rstrip(), limit=150)
        del depth_dict["lastUpdateId"]

        print(row.rstrip())
        coin = []        
        for value in depth_dict.values():
            for i in value:
                if (float(i[0])*float(i[1]))>price:
                    coin.append([row.rstrip(), i[0], i[1], datetime.now()])
                    #print(i)
        if len(coin) != 0:
            newListCoin1.append(coin)
    listNameCoin.close()

def CheckTheCoin():
    p = 0

    for coin1 in newListCoin1:
        for info1 in coin1:
            x=-1
            y=-1
            z=-1
            for newListCoin2 in fullListCoin:
                x+=1
                y=-1
                z=-1
                if  info1[3] - newListCoin2[0][0][3]> delta:
                    for coin2 in newListCoin2:
                        y+=1
                        z=-1
                        for info2 in coin2:
                            z+=1
                            if info1[0] == info2[0] and info1[1] == info2[1]:
                                if float(info1[2])>float(info2[2])*cf:
                                    print('OK!')
                                else: 
                                    print('удаление')
                                    fullListCoin[x][y].pop(z)
                                    break
                            else: 
                                print('н/ц')
                                break
                else:
                    print('время')
                

                        
                                
                        
GetDataCoin()
fullListCoin.append(newListCoin1)

while True:
    newListCoin1 = []
    GetDataCoin()
    CheckTheCoin()
    fullListCoin.append(newListCoin1)

#     # Переподключение к WebSocket каждые 23 часа
# def reconnect_websocket_every_23h():
#     time.sleep(5)
#     print('\nStart reconnecting')
#     ubwa.stop_stream(ubwa.get_request_id())
#     ubwa.create_stream(['depth'], listCoin)
#     print('\nSuccessful connection ')
#     print(threading.active_count())
#     reconnect_websocket_every_23h() 

# def reconnect_websocket():
#     time.sleep(82800)
#     print('\nStart reconnecting')
#     ubwa.stop_stream(ubwa.get_request_id())
#     ubwa.create_stream(['depth'], listCoin)
#     print('\nSuccessful connection ')