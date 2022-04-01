from db_requests import select_all_user_id, select_get_quantity, delete_sqlite_record, insert_into_table, update_sqlite_table, select_get_an_approved_entry, insert_user_id, select_user_id
from datetime import datetime, timedelta
from binance.spot import Spot as Client
from asyncio.windows_events import NULL
import unicorn_binance_websocket_api
from progress.spinner import Spinner 
from progress.bar import Bar
from threading import Thread
from pygame import mixer
import json
import time
import telebot
import configparser

# Импорт cfg
config = configparser.ConfigParser()    # создаём объекта парсера
config.read("cfg.ini")                  # читаем конфиг
config["Settings"]["time"]
delta = timedelta(minutes = float(config["Settings"]["time"].strip ('"')))
limit = float(config["Settings"]["limit"].strip ('"'))
cf_update = float(config["Settings"]["cf_update"].strip ('"'))
cf_distance = float(config["Settings"]["cf_distance"].strip ('"'))

# Звук оповещения
mixer.init() 
sound=mixer.Sound("C:/Program Files (x86)/FSR Launcher/SubApps/CScalp/Data/Sounds/nyaa_volumeUP.mp3")
ubwa = unicorn_binance_websocket_api.BinanceWebSocketApiManager(exchange="binance.com")


# Парсинг файла с монетами в массив
listCoin = []
coins = open('coins.txt')
for row in coins: listCoin.append(row.rstrip())
coins.close()

# Progress bar
bar = Bar('Importing Coins', max = len(listCoin))
spinner = Spinner('Checking ')

ubwa.create_stream(['depth'], listCoin)
print('Successful connection')

# Переподключение к WebSocket каждые 23 часа
def reconnect_websocket():
    time.sleep(82800)
    print('\nStart reconnecting')
    ubwa.stop_stream(ubwa.get_request_id())
    ubwa.create_stream(['depth'], listCoin)
    print('\nSuccessful connection ')
    reconnect_websocket() 

# Первое получение данных
def get_first_data():
    for row in listCoin:
        spot_client = Client(base_url="https://api1.binance.com")
        depth_dict = spot_client.depth(row, limit=150)
        del depth_dict["lastUpdateId"]
        # print(f'Check: {row}')
        bar.next()
    
        for ba in depth_dict.values():
            for i in ba:
                if (float(i[0])*float(i[1]))>limit:
                    if not select_get_quantity(row, i[0]):                             # Если нет записи
                        insert_into_table(row, i[0], i[1], str(datetime.now()))        # Создание записи
                    else: update_sqlite_table(row, i[0], i[1], str(datetime.now())),   # Обновление записи
    bar.finish()
    print('Import Complite')

# Получение и проверка с sql получаемых записей
def checking_for_a_diff():
    def check(ba):
        record = select_get_quantity(jsMessage['data']['s'], ba[0])
        if float(ba[0])*float(ba[1])>limit:                                                         # Если цена * кол-во > limit
            if not record:                                                                          # Если записи нет            
                insert_into_table(jsMessage['data']['s'], ba[0], ba[1], str(datetime.now()))        # Создание записи
            elif float(record[3]) * cf_update < float(ba[1]):                                       # Если количество осталось
                update_sqlite_table(jsMessage['data']['s'], ba[0], ba[1], record[4])                # Обновить цену и оставить дату
            else: 
                update_sqlite_table(jsMessage['data']['s'], ba[0], ba[1], str(datetime.now()))      # Выполнить обновление
        elif record:  
            delete_sqlite_record(jsMessage['data']['s'], ba[0])                                     #  Удаляет заявки 0.000000                                   
            
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

# Отправка уведомлений, удаление старых записей
def check_old_data():
    while True:
        time.sleep(2)
        # (3, 'SHIBUSDT', 2.556e-05, 6775264818.0, '2022-03-31 20:15:53.095394')
        # {'symbol': 'DOGEUSDT', 'price': '0.13950000'}
        records = select_get_an_approved_entry(datetime.now() - delta)
        if records:
            for record in records:
                spot_client = Client(base_url="https://api1.binance.com")
                percentage_to_density = abs((float(spot_client.ticker_price(record[1])['price']) / float(record[2]) - 1))
                if  percentage_to_density <= cf_distance:
                    print(f'\n\nCoin: {record[1]}\nPrice: {record[2]}\nQuantity: {record[3]}\nAmount: {float(record[2]) * float(record[3])}$\nPercentage to density: {percentage_to_density*100}%\nDate of discovery: {record[4]}')
                    send_telegram(record, percentage_to_density)
                    sound.play()
                    delete_sqlite_record(record[1], record[2])
                    

# Работа с ботом
token = '5276441681:AAHi9DX8ZYWVlm49AEBU1be0gVEXWmeKoZ8'
bot=telebot.TeleBot(token)

# def infinity_polling(self, *args, **kwargs):
#     while not self.__stop_polling.is_set():
#         try:
#             self.polling(*args, **kwargs)
#         except Exception as e:
#             time.sleep(5)
#             pass
#     print("Break infinity polling")

# Запуск цикла Telebot
def polling():
    bot.polling(none_stop=True, interval=0)

# Запись id user в бд
@bot.message_handler(commands=['start'])
def start_handler(message):
    bot.send_message(message.chat.id, "I'm working!")

    if not select_user_id(str(message.chat.id)):
        insert_user_id(str(message.chat.id))

# Отправка уведомления в телеграм
def send_telegram(record, percentage_to_density):
    for user_id in select_all_user_id():
        try:
            bot.send_message(user_id[0], f'\n\nCoin: {record[1]}\nPrice: {record[2]}\nQuantity: {record[3]}\nAmount: {float(record[2]) * float(record[3])}$\nPercentage to density: {percentage_to_density*100}%\n\nDate of discovery: {record[4]}\n')
        except telebot.apihelper.ApiException as e:
            if e.description == "Forbidden: bot was blocked by the user":
                   print(f"Attention please! The user {user_id[0]} has blocked the bot")

# Значек работы программы
def spin():
    while True:
        time.sleep(0.2)
        spinner.next()

# Вызовы основных функций
print ("Do you want to initialize coins?? y/n")
solution = input()
if solution == 'y' or solution == 'Y':
    get_first_data()

th1 = Thread(target=checking_for_a_diff).start()
th2 = Thread(target=check_old_data).start()
th3 = Thread(target=polling).start()
th4 = Thread(target=reconnect_websocket).start()
spin()