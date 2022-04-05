import unicorn_binance_websocket_api
import json

listCoin = []
coins = open('coins.txt')
for row in coins: listCoin.append(row.rstrip())
coins.close()

ubwa_trade = unicorn_binance_websocket_api.BinanceWebSocketApiManager(exchange="binance.com")
ubwa_trade.create_stream(['depth'], listCoin)
while True:
        oldest_data_from_stream_buffer = ubwa_trade.pop_stream_data_from_stream_buffer()
        if oldest_data_from_stream_buffer:
            jsMessage = json.loads(oldest_data_from_stream_buffer)
            if 'stream' in jsMessage.keys():
                print(jsMessage)