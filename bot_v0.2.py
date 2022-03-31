from asyncio.windows_events import NULL
import unicorn_binance_websocket_api
import json
import logging
from datetime import datetime, timedelta
from DB import select_info, delete_sqlite_record, insert_into_table, update_sqlite_table

# add filemode="w" to overwrite
logging.basicConfig(filename="sample.log", level=logging.INFO)





ubwa = unicorn_binance_websocket_api.BinanceWebSocketApiManager(exchange="binance.com")
ubwa.create_stream(['depth'], ['btcusdt', 'ethusdt', 'dogeusdt', 'bnbusdt', 'ADAUSDT', 'AAVEUSDT'])

while True:
    oldest_data_from_stream_buffer = ubwa.pop_stream_data_from_stream_buffer()
    if oldest_data_from_stream_buffer:
        jsMessage = json.loads(oldest_data_from_stream_buffer)
        if 'stream' in jsMessage.keys():
            for bid in jsMessage['data']['b']:
                if select_info(jsMessage['data']['s'], bid[0]) != NULL:
                    insert_into_table(jsMessage['data']['s'], bid[0], bid[1], str(datetime.now()))
                else:update_sqlite_table(jsMessage['data']['s'], bid[0], bid[1], str(datetime.now()))
            for ask in jsMessage['data']['a']:
                if select_info(jsMessage['data']['s'], ask[0]) != NULL:
                    insert_into_table(jsMessage['data']['s'], ask[0], ask[1], str(datetime.now()))
                else:update_sqlite_table(jsMessage['data']['s'], ask[0], bid[1], str(datetime.now()))
                        
            print()
            print(jsMessage['data']['b'])
        