from db_requests import update_currnet_price, select_coin_current_price, insert_price, select_get_an_verified_record, delete_all_data, select_all_records, select_all_user_id, select_record, delete_sqlite_record, insert_depth, update_enter_range, update_out_from_range, update_record, select_get_an_accepted_records, insert_user_id, select_user_id
from datetime import date, datetime, timedelta
from binance.spot import Spot as Client
# from asyncio.windows_events import NULL
import unicorn_binance_websocket_api
from progress.spinner import Spinner 
from progress.bar import Bar
from threading import Thread
from loguru import logger
from pygame import mixer
import configparser
import json
import time
import telebot

logger.add("simple.log")
logger.debug("Start script")

# Импорт cfg
config = configparser.ConfigParser()                          # создаём объекта парсера
config.read("cfg.ini")                                        # читаем конфиг
delta = timedelta(minutes = float(config["Settings"]["delta"].strip ('"')))
time_resend = timedelta(minutes = float(config["Settings"]["time_resend"].strip ('"')))
limit = float(config["Settings"]["limit"].strip ('"'))
cf_update = float(config["Settings"]["cf_update"].strip ('"'))
cf_distance = float(config["Settings"]["cf_distance"].strip ('"'))

# Звук оповещения
mixer.init() 
sound_notification=mixer.Sound("sounds/notification_nyaa.mp3")
sound_error_polling=mixer.Sound("sounds/error_polling.mp3")
sound_error=mixer.Sound("sounds/error_binance.mp3")


# Парсинг файла с монетами в массив
listCoin = []
coins = open('coins.txt')
for row in coins: listCoin.append(row.rstrip())
coins.close()

# Progress bar
bar = Bar('Importing Coins', max = len(listCoin))
spinner = Spinner('Checking ')


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
                    if not record:                                                      # Если записи нет            
                        insert_depth(row, i[0], i[1], str(datetime.now()))              # Создание записи
                    elif float(record[3]) * cf_update < float(i[1]):                    # Если количество осталось
                        update_record(row, i[0], i[1], record[4])                       # Обновить количество и оставить дату
                    else: 
                        update_record(row, i[0], i[1], str(datetime.now()))             # Выполнить обновление

    bar.finish()
    print('Import Complite')

# Подключеник к бинансу
ubwa_depth = unicorn_binance_websocket_api.BinanceWebSocketApiManager(exchange="binance.com")
ubwa_depth.create_stream(['depth'], listCoin)
print('Successful connection ubwa_depth')

ubwa_trade = unicorn_binance_websocket_api.BinanceWebSocketApiManager(exchange="binance.com")
ubwa_trade.create_stream(['aggTrade'], listCoin)
print('Successful connection ubwa_trade')

# Получение данных из websocket и сравнение их с бд
def get_depth_from_websocket():
    def check(ba):
        record = select_record(jsMessage['data']['s'], ba[0])
        if float(ba[0])*float(ba[1])>limit:                                                         # Если цена * кол-во > limit
            if not record:                                                                          # Если записи нет            
                insert_depth(jsMessage['data']['s'], ba[0], ba[1], str(datetime.now()))             # Создание записи
            elif float(record[3]) * cf_update < float(ba[1]):                                       # Если количество осталось
                update_record(jsMessage['data']['s'], ba[0], ba[1], record[4])                      # Обновить количество и оставить дату
            else: 
                update_record(jsMessage['data']['s'], ba[0], ba[1], str(datetime.now()))            # Выполнить обновление
        elif record:  
            delete_sqlite_record(jsMessage['data']['s'], ba[0])                                     #  Удаляет заявки меньшн < limit                                   
            
    while True:
        oldest_data_from_stream_buffer = ubwa_depth.pop_stream_data_from_stream_buffer()
        if oldest_data_from_stream_buffer:
            jsMessage = json.loads(oldest_data_from_stream_buffer)
            if 'stream' in jsMessage.keys():
                for bid in jsMessage['data']['b']:
                    check(bid)
                for ask in jsMessage['data']['a']:
                    check(ask)
# {'stream': 'xrpusdt@aggTrade', 'data': {'e': 'aggTrade', 'E': 1649082249217, 's': 'XRPUSDT', 'a': 331831505, 'p': '0.82910000'
def get_current_price_from_websocket():
    while True:
            oldest_data_from_stream_buffer = ubwa_trade.pop_stream_data_from_stream_buffer()
            if oldest_data_from_stream_buffer:
                jsMessage = json.loads(oldest_data_from_stream_buffer)
                if 'stream' in jsMessage.keys():
                    if select_coin_current_price(jsMessage['data']['s']):
                        update_currnet_price(jsMessage['data']['s'], jsMessage['data']['p'])
                    else: 
                        insert_price(jsMessage['data']['s'], jsMessage['data']['p'])
                    
                

# Проверка данных в БД, отправка уведомлений
def check_old_data():
    while True:
        # record = (3, 'SHIBUSDT', 2.556e-05, 6775264818.0, '2022-03-31 20:15:53.095394')
        records = select_get_an_accepted_records(str(datetime.now() - delta))
        if records:
            for record in records:
                try:
                    sign_ptd = float(select_coin_current_price(record[1])) / float(record[2])
                    percentage_to_density = abs((sign_ptd) - 1)
                    dt_out = datetime.strptime(record[5], '%Y-%m-%d %H:%M:%S.%f')
                    if  percentage_to_density <= cf_distance:
                        if datetime.now() - time_resend > dt_out and record[6] != 1:
                            if sign_ptd > 1: percentage_to_density = -percentage_to_density
                            update_enter_range(record[1], record[2], str(datetime.now()))
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
    logger.debug(f"User №{message.chat.id} send I'm working)")
    if not select_user_id(str(message.chat.id)):
        insert_user_id(str(message.chat.id))
        logger.debug(f'User №{message.chat.id} added to the database)')
        
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
        logger.debug(f"User №{message.chat.id} send all_verified_message")
        bot.send_message(message.chat.id, all_verified_message)
    else: 
        logger.debug(f"User №{message.chat.id} send No records)")
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
print ("\nDo you want to delete all the data? y/n")
solution = input()
if solution == 'y' or solution == 'Y':
    print ("ARE YOU SURE? Write: y/n")   
    solution = input()
    if solution == 'y' or solution == 'Y':
        if select_all_records():
            delete_all_data()

print ("Do you want to initialize coins? y/n")
solution = input()
if solution == 'y' or solution == 'Y':
    get_first_data()

# Запуск нескольких потоков
th1 = Thread(target=get_depth_from_websocket).start()
th2 = Thread(target=get_current_price_from_websocket).start()
th3 = Thread(target=check_old_data).start()
th4 = Thread(target=polling).start()
spin()