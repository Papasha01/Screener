from db_requests import select_get_an_verified_record, delete_all_data, select_all_records, select_all_user_id, select_record, delete_sqlite_record, insert_first, update_enter_range, update_out_from_range, update_record, select_get_an_accepted_records, insert_user_id, select_user_id
from datetime import datetime, timedelta
from binance.spot import Spot as Client
from asyncio.windows_events import NULL
import unicorn_binance_websocket_api
from progress.spinner import Spinner 
from progress.bar import Bar
from threading import Thread
from loguru import logger
from pygame import mixer
import configparser
import threading
import json
import time
import telebot

logger.add("simple.log")
logger.debug("Start script")

# Импорт cfg
config = configparser.ConfigParser()                                                        # создаём объекта парсера
config.read("cfg.ini")                                        # читаем конфиг
delta = timedelta(minutes = float(config["Settings"]["delta"].strip ('"')))
time_resend = timedelta(minutes = float(config["Settings"]["time_resend"].strip ('"')))
limit = float(config["Settings"]["limit"].strip ('"'))
cf_update = float(config["Settings"]["cf_update"].strip ('"'))
cf_distance = float(config["Settings"]["cf_distance"].strip ('"'))

# Звук оповещения
mixer.init() 
sound_notification=mixer.Sound("C:/Program Files (x86)/FSR Launcher/SubApps/CScalp/Data/Sounds/nyaa_volumeUP.mp3")
sound_error_polling=mixer.Sound("C:/Program Files (x86)/FSR Launcher/SubApps/CScalp/Data/Sounds/error_sicko_mode.mp3")
sound_error=mixer.Sound("C:/Program Files (x86)/FSR Launcher/SubApps/CScalp/Data/Sounds/error_CDOxCYm.mp3")
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
                    record = select_record(row, i[0])
                    if not record:                                                     # Если записи нет            
                        insert_first(row, i[0], i[1], str(datetime.now()))        # Создание записи
                    elif float(record[3]) * cf_update < float(i[1]):                   # Если количество осталось
                        update_record(row, i[0], i[1], record[4])                      # Обновить количество и оставить дату
                    else: 
                        update_record(row, i[0], i[1], str(datetime.now()))            # Выполнить обновление

    bar.finish()
    print('Import Complite')

# Получение данных из websocket и сравнение их с бд
def checking_for_a_diff():
    def check(ba):
        record = select_record(jsMessage['data']['s'], ba[0])
        if float(ba[0])*float(ba[1])>limit:                                                         # Если цена * кол-во > limit
            if not record:                                                                          # Если записи нет            
                insert_first(jsMessage['data']['s'], ba[0], ba[1], str(datetime.now()))             # Создание записи
            elif float(record[3]) * cf_update < float(ba[1]):                                       # Если количество осталось
                update_record(jsMessage['data']['s'], ba[0], ba[1], record[4])                      # Обновить количество и оставить дату
            else: 
                update_record(jsMessage['data']['s'], ba[0], ba[1], str(datetime.now()))            # Выполнить обновление
        elif record:  
            delete_sqlite_record(jsMessage['data']['s'], ba[0])                                     #  Удаляет заявки меньшн < limit                                   
            
    while True:
        oldest_data_from_stream_buffer = ubwa.pop_stream_data_from_stream_buffer()
        if oldest_data_from_stream_buffer:
            jsMessage = json.loads(oldest_data_from_stream_buffer)
            if 'stream' in jsMessage.keys():
                for bid in jsMessage['data']['b']:
                    check(bid)
                for ask in jsMessage['data']['a']:
                    check(ask)

# Проверка данных в БД
def check_old_data():
    while True:
        # time.sleep(5)
        # record = (3, 'SHIBUSDT', 2.556e-05, 6775264818.0, '2022-03-31 20:15:53.095394')
        records = select_get_an_accepted_records(datetime.now() - delta)
        if records:
            for record in records:
                try:
                    spot_client = Client(base_url="https://api1.binance.com")
                    sign = float(spot_client.ticker_price(record[1])['price']) / float(record[2])
                    percentage_to_density = abs((sign) - 1)
                    if  percentage_to_density <= cf_distance:
                        if sign > 1:
                            percentage_to_density = -percentage_to_density
                            update_enter_range(record[1], record[2])
                            print(f'\n\nCoin: {record[1]}\nPrice: {record[2]}\nQuantity: {record[3]}\nAmount: {round(float(record[2]) * float(record[3]), 2)}$\nPercentage to density: {round(percentage_to_density*100, 2)}%\nDate of discovery: {record[4]}')
                            send_telegram(record, percentage_to_density)
                            logger.debug(f'{str(record)} {str(percentage_to_density)})')
                            sound_notification.play()
                    else: 
                        update_out_from_range(record[1], record[2])
                except Exception as e:
                    logger.error(e)
                    sound_error.play()
                    time.sleep(10)
                    check_old_data()

# Работа с ботом
token = '5276441681:AAHi9DX8ZYWVlm49AEBU1be0gVEXWmeKoZ8'
bot=telebot.TeleBot(token)

# Запуск цикла Telebot
def polling():
    time.sleep(5)
    try: 
        bot.polling(none_stop=True) 
    except Exception as e: 
        logger.error(e)
        sound_error_polling.play()
        time.sleep(5)
        polling()

# Взаимодействие с ботом
@bot.message_handler(commands=['start'])
def start_handler(message):
    bot.send_message(message.chat.id, "I'm working!")

    if not select_user_id(str(message.chat.id)):
        insert_user_id(str(message.chat.id))
        
@bot.message_handler(commands=['check'])
def start_handler(message):
    records = select_get_an_verified_record()
    all_verified_message = ''
    if records:
        for record in records:
            spot_client = Client(base_url="https://api1.binance.com")
            sign = float(spot_client.ticker_price(record[1])['price']) / float(record[2])
            percentage_to_density = abs((sign) - 1)
            if sign > 1:
                percentage_to_density = -percentage_to_density
            all_verified_message += f'Coin: {record[1]}\nPrice: {record[2]}\nQuantity: {record[3]}\nAmount: {round(float(record[2]) * float(record[3]), 2)}$\nPercentage to density: {round(percentage_to_density*100, 2)}%\nDate of discovery: {record[4]}\n\n'
        bot.send_message(message.chat.id, all_verified_message)
    else: 
        bot.send_message(message.chat.id, 'No records')

# Отправка уведомления в телеграм
def send_telegram(record, percentage_to_density):
    if select_all_user_id():
        for user_id in select_all_user_id():
            try:
                bot.send_message(user_id[0], f'\n\nCoin: {record[1]}\nPrice: {record[2]}\nQuantity: {record[3]}\nAmount: {round(float(record[2]) * float(record[3]), 2)}$\nPercentage to density: {round(percentage_to_density*100, 2)}%\n\nDate of discovery: {record[4]}\n')
            except telebot.apihelper.ApiException as e:
                if e.description == "Forbidden: bot was blocked by the user":
                    print(f"Attention please! The user {user_id[0]} has blocked the bot")

# Значек работы программы
def spin():
    while True:
        time.sleep(0.2)
        spinner.next()

# Вызовы основных функций
print ("Do you want to delete all the data? y/n")
solution = input()
if solution == 'y' or solution == 'Y':
    if select_all_records():
        delete_all_data()

print ("Do you want to initialize coins? y/n")
solution = input()
if solution == 'y' or solution == 'Y':
    get_first_data()

# Запуск нескольких потоков
th1 = Thread(target=checking_for_a_diff).start()
th2 = Thread(target=check_old_data).start()
th3 = Thread(target=polling).start()
spin()