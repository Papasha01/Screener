from binance.spot import Spot as Client
from asyncio.windows_events import NULL
import unicorn_binance_websocket_api
import json
import logging
import time
from threading import Thread
from datetime import datetime, timedelta
from db_requests import select_get_quantity, delete_sqlite_record, insert_into_table, update_sqlite_table

ubwa = unicorn_binance_websocket_api.BinanceWebSocketApiManager(exchange="binance.com")
logging.basicConfig(filename="simple.log", level=logging.INFO)
delta = timedelta(seconds=5)
limit = 100000
listCoin = []
jsMessage = json

def checking_for_a_diff():
    def check(ba):
        if float(ba[0])*float(ba[1])>limit: 
            record = select_get_quantity(jsMessage['data']['s'], ba[0])
            if not record:
                insert_into_table(jsMessage['data']['s'], ba[0], ba[1], str(datetime.now()))
            elif float(record) * 0.9 < float(ba[1]): 
                update_sqlite_table(jsMessage['data']['s'], ba[0], ba[1], str(datetime.now()))
            else: delete_sqlite_record(jsMessage['data']['s'], ba[0])

    while True:
            oldest_data_from_stream_buffer = ubwa.pop_stream_data_from_stream_buffer()
            if oldest_data_from_stream_buffer:
                jsMessage = json.loads(oldest_data_from_stream_buffer)
                if 'stream' in jsMessage.keys():
                    print(jsMessage)
                    for bid in jsMessage['data']['b']:
                        check(bid)
                    for ask in jsMessage['data']['a']:
                        check(ask)

def get_first_data():
    coins = open('coins.txt')
    for row in coins:
        spot_client = Client(base_url="https://api1.binance.com")
        depth_dict = spot_client.depth(row.rstrip(), limit=150)
        del depth_dict["lastUpdateId"]
        listCoin.append(row.rstrip())
        print(f'Check: {row.rstrip()}')

        for ba in depth_dict.values():
            for i in ba:
                if (float(i[0])*float(i[1]))>limit:
                    if select_get_quantity(row.rstrip(), i[0]) == False:
                        insert_into_table(row.rstrip(), i[0], i[1], str(datetime.now()))
                    else: update_sqlite_table(row.rstrip(), i[0], i[1], str(datetime.now())),
    ubwa.create_stream(['depth'], listCoin)
    coins.close()


def send_notification():
    while True:
        time.sleep(5)
        print('hello!')
    
get_first_data()
th1 = Thread(target=checking_for_a_diff)
th2 = Thread(target=send_notification)
th1.start()
th2.start()


# Привязка дела к телеграму
# Кнопки в телеграме