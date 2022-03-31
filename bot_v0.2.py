from binance.spot import Spot as Client
from asyncio.windows_events import NULL
import unicorn_binance_websocket_api
import json
import logging
import time
import threading
from threading import Thread
from datetime import datetime, timedelta
from db_requests import select_get_quantity, delete_sqlite_record, insert_into_table, update_sqlite_table, select_get_an_approved_entry

from pygame import mixer
mixer.init() 
sound=mixer.Sound("C:/Program Files (x86)/FSR Launcher/SubApps/CScalp/Data/Sounds/nyaa_volumeUP.mp3")

ubwa = unicorn_binance_websocket_api.BinanceWebSocketApiManager(exchange="binance.com")
logging.basicConfig(filename="simple.log", level=logging.INFO)
delta = timedelta(seconds=30)
limit = 100000
cf = 0.9
listCoin = []

# Получение и проверка с sql получаемых записей
def checking_for_a_diff():
    def check(ba):
        if float(ba[0])*float(ba[1])>limit:                                                         # Если цена * кол-во > limit
            record = select_get_quantity(jsMessage['data']['s'], ba[0])
            if not record:                                                                          # Если записи нет            
                insert_into_table(jsMessage['data']['s'], ba[0], ba[1], str(datetime.now()))        # Создание записи
            elif float(record) * cf < float(ba[1]):                                                # Если количество осталось
                update_sqlite_table(jsMessage['data']['s'], ba[0], ba[1], str(datetime.now()))      # Выполнить обновление
            else: 
                delete_sqlite_record(jsMessage['data']['s'], ba[0])                                 # Выполнить удаление

    while True:
            oldest_data_from_stream_buffer = ubwa.pop_stream_data_from_stream_buffer()
            if oldest_data_from_stream_buffer:
                jsMessage = json.loads(oldest_data_from_stream_buffer)
                if 'stream' in jsMessage.keys():
                    # print(jsMessage)
                    for bid in jsMessage['data']['b']:
                        check(bid)
                    for ask in jsMessage['data']['a']:
                        check(ask)

# Первое получение данных
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
                    if not select_get_quantity(row.rstrip(), i[0]):                             # Если нет записи
                        insert_into_table(row.rstrip(), i[0], i[1], str(datetime.now()))        # Создание записи
                    else: update_sqlite_table(row.rstrip(), i[0], i[1], str(datetime.now())),   # Обновление записи
    ubwa.create_stream(['depth'], listCoin)
    coins.close()

# Отправка уведомлений, удаление старых записей
def check_old_data():
    while True:
        # (3, 'SHIBUSDT', 2.556e-05, 6775264818.0, '2022-03-31 20:15:53.095394')
        records = select_get_an_approved_entry(datetime.now() - delta)
        if records:
            for record in records:
                print(f'APPROVED: {record}')
                sound.play()
                delete_sqlite_record(record[1], record[2])
        time.sleep(5)

get_first_data()

th1 = Thread(target=checking_for_a_diff).start()
th2 = Thread(target=check_old_data).start()

# Привязка дела к телеграму
# Кнопки в телеграме