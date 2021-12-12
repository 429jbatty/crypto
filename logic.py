import ccxt
import pandas as pd
import numpy

def get_available_markets(
    markets,
    base_currency="",
    quote_currency=""
    ):

    available_markets = []

    if quote_currency != "" and base_currency != "":
        for market in markets:
            if markets[market]["quote"] == quote_currency.upper():
                if markets[market]["base"] == base_currency.upper():
                    available_markets.append(market)

    elif quote_currency != "" and base_currency == "":
        for market in markets:
            if markets[market]["quote"] == quote_currency.upper():
                available_markets.append(market)

    elif quote_currency == "" and base_currency != "":
        for market in markets:
            if markets[market]["base"] == base_currency.upper():
                available_markets.append(market)                      

    elif quote_currency == "" and base_currency == "":
        for market in markets:
            available_markets.append(market)

    return available_markets


def find_all_combos(
    markets,
    coin_a,
    coin_b,
    coin_c
    ):

    #A/B
    try:
        a_b = get_available_markets(markets, base_currency=coin_a,quote_currency=coin_b)[0]
    except:
        try: 
            a_b = get_available_markets(markets, base_currency=coin_b,quote_currency=coin_a)[0]
        except:
            print("This market cannot convert between " + coin_a + " and " + coin_b)
            a_b = None
    #A/C
    try:
        a_c = get_available_markets(markets, base_currency=coin_a,quote_currency=coin_c)[0]
    except:
        try: 
            a_c = get_available_markets(markets, base_currency=coin_c,quote_currency=coin_a)[0]
        except:
            print("This market cannot convert between " + coin_a + " and " + coin_c)
            a_c = None
    #B/C
    try:
        b_c = get_available_markets(markets, base_currency=coin_b,quote_currency=coin_c)[0]
    except:
        try: 
            b_c = get_available_markets(markets, base_currency=coin_c,quote_currency=coin_b)[0]
        except:
            print("This market cannot convert between " + coin_b + " and " + coin_c)
            b_c = None

    combos = [
        a_b,
        a_c,
        b_c
    ]

    return combos


def get_swap_df(
    exchange,
    markets,
    currency_swaps,
    ):
    #Get all exchange rates
    quote_list = []
    base_list = []
    bid_list = []
    ask_list = []

    for market in currency_swaps:
        ticker_data = exchange.fetch_ticker(market)
        market_dict = markets[market]

        quote_list.append(market_dict["quote"])
        base_list.append(market_dict["base"])
        bid_list.append(ticker_data["bid"])
        ask_list.append(ticker_data["ask"])

    swap_df = pd.DataFrame(
        list(zip(
            quote_list, 
            base_list, 
            bid_list, 
            ask_list)),
        columns =['QUOTE', 'BASE', 'BID', 'ASK'])

    # Flip neccessary quote/base rows
    for i in range(len(swap_df)):
        quote_dup = swap_df.loc[i,"QUOTE"] in (swap_df.loc[swap_df.index != i,"QUOTE"].to_list())
        base_dup = swap_df.loc[i,"BASE"] in (swap_df.loc[swap_df.index != i,"BASE"].to_list())
        if quote_dup * base_dup:       
            swap_df.loc[i, ["QUOTE","BASE"]] = swap_df.loc[i, ["BASE","QUOTE"]].values
            swap_df.loc[i, ["BID","ASK"]] = 1 / (swap_df.loc[i, ["ASK","BID"]].values)

    return swap_df


def get_swap_return(swap_df):

    # Flip neccessary quote/base rows
    for i in range(len(swap_df)):
        quote_dup = swap_df.loc[i,"QUOTE"] in (swap_df.loc[swap_df.index != i,"QUOTE"].to_list())
        base_dup = swap_df.loc[i,"BASE"] in (swap_df.loc[swap_df.index != i,"BASE"].to_list())
        if quote_dup * base_dup:       
            swap_df.loc[i, ["QUOTE","BASE"]] = swap_df.loc[i, ["BASE","QUOTE"]].values
            swap_df.loc[i, ["BID","ASK"]] = 1 / (swap_df.loc[i, ["ASK","BID"]].values)

    ending_value = numpy.prod(swap_df["BID"])
    swap_return = ending_value-1
    
    return swap_return


def get_tri_arb(
    exchange_id: str,
    currencies: list
    ):

    # Connect to Exchange
    exchange = getattr(ccxt, exchange_id)()

    # Load market
    markets = exchange.load_markets()

    cur_swaps = find_all_combos(
        markets,
        currencies[0],
        currencies[1],
        currencies[2]
        )

    swap_df = get_swap_df(
        exchange,
        markets,
        cur_swaps)

    swap_return = get_swap_return(swap_df)
    # print("{0:.4%}".format(swap_return))
    
    return swap_return, swap_df


def write_offerings_csv():
    # view exchange offerings
    exchange_list = []
    base_list = []
    quote_list = []

    for exchange_it in ccxt.exchanges:
        try:
            exchange = getattr(ccxt, exchange_it)()
            markets = exchange.load_markets()
            for market_it in markets:
                exchange_list.append(exchange_it)
                base_list.append(markets[market_it]["base"])
                quote_list.append(markets[market_it]["quote"])
        except:
            print("Cannot connect to " + exchange_it)
            continue

    df_offerings = pd.DataFrame(list(zip(exchange_list, base_list, quote_list)),
                columns =['EXCHANGE', 'BASE', 'QUOTE'])

    df_offerings.to_csv("df_offerings.csv", index=False)

df_offerings.loc[
    (df_offerings["QUOTE"] == "USD") &
    (df_offerings["BASE"] == "EUR")
]
