import websocket
import json

cc = 'btcusdt'
socket = f'wss://stream.binance.com:9443/ws/{cc}@depth10@100ms'

def on_message(ws, message):
    obj = json.loads(message)
    #print(obj['s'], obj['p'])
    print(message)

def on_error(ws, error):
    print(error)

def on_close(ws):
    print("### closed ###")

def on_open(ws):
    print("### connected ###")

if __name__ == "__main__":
    ws = websocket.WebSocketApp(socket,
                              on_message = on_message,
                              on_error = on_error,
                              on_close = on_close)
    ws.on_open = on_open
    ws.run_forever()