import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from binance.spot import Spot as Client

spot_client = Client(base_url="https://api3.binance.com")
depth_dict = spot_client.depth("ETHUSDT", limit=10)

for bid in depth_dict['bids']:
    print(type(bid))

# df_list = []
# for side in ["bids", "asks"]:
#     df = pd.DataFrame(depth_dict[side], columns=["price", "quantity"], dtype=float)
#     df["side"] = side
#     df_list.append(df)

# df = pd.concat(df_list).reset_index(drop=True)


# # График
# fig, ax = plt.subplots()
# sns.scatterplot(x="price", y="quantity", hue="side", 
#                 data=df, palette=["green", "red"])

# plt.show()