from binance.spot import Spot as Client

listCoin = open('listCoin.txt')

for row in listCoin:
    print(row.rstrip())

    spot_client = Client(base_url="https://api3.binance.com")
    depth_dict = spot_client.depth(row.rstrip(), limit=150)

    listBids = []
    listAsks = []
    price = 500000
    
    for bid in depth_dict['bids']:
        bid.append(float(bid[0])*float(bid[1]))
        if bid[2]>price:
            listBids.append(bid)
    print(f"BIDS: {listBids}")

    for ask in depth_dict['asks']:
        ask.append(float(ask[0])*float(ask[1]))
        if ask[2]>price:
            listAsks.append(ask)
    print(f"ASKS: {listAsks}")


print("COMPLITE!")