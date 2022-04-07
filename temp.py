import unicorn_binance_websocket_api
import json

ubwa_trade = unicorn_binance_websocket_api.BinanceWebSocketApiManager(exchange="binance.com")
ubwa_trade.create_stream(['depth', 'aggTrade'], 'BTCUSDT')
while True:
        oldest_data_from_stream_buffer = ubwa_trade.pop_stream_data_from_stream_buffer()
        if oldest_data_from_stream_buffer:
            jsMessage = json.loads(oldest_data_from_stream_buffer)
            if 'stream' in jsMessage.keys():
                print(jsMessage)