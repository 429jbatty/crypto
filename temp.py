# IMPORTS
import ccxt
import pandas as pd
import random
import numpy as np
import time
import matplotlib.pyplot as plt

# RELATIVE IMPORTS
from logic import find_all_combos, get_available_markets, get_swap_df, get_swap_return, get_tri_arb

exchange = ccxt.coinbase()
markets = exchange.load_markets()

#####
exchange_id = 'coinbase'
currencies = ['ETH', 'USD', 'EUR']
get_tri_arb(exchange_id, currencies)[0]

d = []
for i in range(100):
    d.append(get_tri_arb(exchange_id, currencies)[0])




# An "interface" to matplotlib.axes.Axes.hist() method
n, bins, patches = plt.hist(x=d, bins='auto', color='#0504aa',
                            alpha=0.7, rwidth=0.85)
plt.grid(axis='y', alpha=0.75)
plt.xlabel('Value')
plt.ylabel('Frequency')
plt.title('My Very Own Histogram')
maxfreq = n.max()
# Set a clean upper y-axis limit.
plt.ylim(ymax=np.ceil(maxfreq / 10) * 10 if maxfreq % 10 else maxfreq + 10)
plt.show()

# def arb_btcusd():
#     # compare btc/usd across exchanges
#     exchanges = []
#     bid = []
#     ask = []

#     for exchange_id in ccxt.exchanges:
#         try:
#             exchanges.append(exchange_id)

#             exchange = getattr(ccxt, exchange_id)()
#             ticker_data = exchange.fetch_ticker('BTC/USD')
#             bid.append(ticker_data["bid"])
#             ask.append(ticker_data["ask"])
#         except:
#             None

#     df_btc_usd = pd.DataFrame(list(zip(exchanges, bid, ask)),
#                 columns =['EXCHANGE', 'BID', 'ASK'])

#     #Drop NAs and 0s
#     df_btc_usd.dropna(axis = 0, inplace = True)
#     df_btc_usd = df_btc_usd.loc[
#         (df_btc_usd["BID"] != 0) &
#         (df_btc_usd["ASK"] != 0) 
#         ]


#     #Get arbitrage
#     best_bid_price = max(df_btc_usd["BID"])
#     best_bid_ex = df_btc_usd.loc[
#         df_btc_usd["BID"] == max(df_btc_usd["BID"]),
#         "EXCHANGE"].item()

#     best_ask_price = min(df_btc_usd["ASK"])
#     best_ask_ex = df_btc_usd.loc[
#         df_btc_usd["ASK"] == min(df_btc_usd["ASK"]),
#         "EXCHANGE"].item()

#     if best_bid_price > best_ask_price:
#         print("Buy BTC for USD on " + best_ask_ex + " for " + "${:,.2f}".format(best_ask_price))
#         print("Sell BTC for USD on " + best_bid_ex + " for " + "${:,.2f}".format(best_bid_price))