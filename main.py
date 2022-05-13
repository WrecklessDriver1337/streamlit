import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
with st.echo(code_location='below'):
    """
    ## Cryptocurrencies analysis
    ### Find out the most profitable investment with us
    """
    @st.cache(allow_output_mutation=True)
    def get_data():
        bitcoin_data = pd.read_csv("coin_Bitcoin.csv")
        ethereum_data = pd.read_csv("coin_Ethereum.csv")
        tether_data = pd.read_csv("coin_Tether.csv")
        binance_coin_data = pd.read_csv("coin_BinanceCoin.csv")
        usd_coin_data = pd.read_csv("coin_USDCoin.csv")
        solana_data = pd.read_csv("coin_Solana.csv")
        dogecoin_data = pd.read_csv("coin_Dogecoin.csv")
        data_frames = {'Bitcoin': bitcoin_data, 'Ethereum': ethereum_data, 'Tether': tether_data,
                       'Binance Coin': binance_coin_data, 'USD Coin': usd_coin_data,
                       'Solana': solana_data, 'Dogecoin': dogecoin_data}
        return data_frames

    options = st.multiselect(
        'Which currencies would you like to observe? (These are default settings)',
        ['Bitcoin', 'Ethereum', 'Tether', 'Binance Coin', 'USD Coin', 'Solana', 'Dogecoin'],
        ['Ethereum', 'Binance Coin', 'Solana'])

    """
    ### At first let's compare the prices of the chosen currencies
    If the scale has become too big you can safely delete the top most currency 
    and get it back later for the upcoming analysis
    """
    df = get_data()
    for i in df.keys():
        df[i]['Date'] = pd.to_datetime(df[i]['Date'], format='%Y-%m-%d')
    sub_df = {key: value for key, value in df.items() if key in options}
    colors = ['blue', 'red', 'orange', 'green', 'black', 'yellow', 'brown']
    fig, ax = plt.subplots()
    for i in range(len(sub_df)):
        sns.lineplot(data=sub_df[options[i]], x="Date", y="Close", palette=[colors[i]],
                     hue='Symbol', ax=ax, lw=1.5)
    st.pyplot(fig)

    """
    ### Market caps of these cryptocurrencies (on 03-05-2022)
    """
    M_cap = {'Bitcoin': 582, 'Ethereum': 255, 'Tether': 79, 'Binance Coin': 50,
             'USD Coin': 50, 'Solana': 18, 'Dogecoin': 12}
    M_cap_mod = {}
    keys = list(M_cap.keys())
    for n in range(len(M_cap)):
        if keys[n] in options:
            M_cap_mod.update({f'{keys[n]}': M_cap[keys[n]]})
    M_cap_mod.update({'Other cryptocurrencies': 1300 - sum(M_cap_mod.values())})
    M_cap_df = pd.DataFrame(M_cap_mod,
                            index=[0]).T.reset_index().rename(columns={"index": "Currency", 0: "Cap (in billion $)"})
    fig = px.pie(M_cap_df, values='Cap (in billion $)', names='Currency',
                 title='Market capitalization of picked currencies')
    st.plotly_chart(fig)
    st.write(M_cap_df)
    """
    ## Let's now compute some valuable information for investors
    
    ### Yearly volatility of the currencies (starting from 01-01-2017 if possible):
    """
    date = "01-01-2017"
    Bitcoin_returns = df['Bitcoin']['Close'].loc[(df['Bitcoin']['Date'] > date)].pct_change()
    Ethereum_returns = df['Ethereum']['Close'].loc[(df['Ethereum']['Date'] > date)].pct_change()
    Tether_returns = df['Tether']['Close'].loc[(df['Tether']['Date'] > date)].pct_change()
    Binance_Coin_returns = df['Binance Coin']['Close'].loc[(df['Binance Coin']['Date'] > date)].pct_change()
    USD_Coin_returns = df['USD Coin']['Close'].loc[(df['USD Coin']['Date'] > date)].pct_change()
    Solana_returns = df['Solana']['Close'].loc[(df['Solana']['Date'] > date)].pct_change()
    Dogecoin_returns = df['Dogecoin']['Close'].loc[(df['Dogecoin']['Date'] > date)].pct_change()

    Bitcoin_vol = np.std(Bitcoin_returns)*(253**0.5)**2
    Ethereum_vol = np.std(Ethereum_returns)**2*253
    Tether_vol = np.std(Tether_returns)**2*253
    Binance_Coin_vol = np.std(Binance_Coin_returns)**2*253
    USD_Coin_vol = np.std(USD_Coin_returns)**2*253
    Solana_vol = np.std(Solana_returns)**2*253
    Dogecoin_vol = np.std(Dogecoin_returns)**2*253
    Volatilities = {'Bitcoin': Bitcoin_vol, 'Ethereum': Ethereum_vol,
                    'Tether': Tether_vol, 'Binance Coin': Binance_Coin_vol, 'USD Coin': USD_Coin_vol,
                    'Solana': Solana_vol, 'Dogecoin': Dogecoin_vol}

    Volatilities_picked = {}
    for n in range(len(Volatilities)):
        if keys[n] in options:
            Volatilities_picked.update({f'{keys[n]}': Volatilities[keys[n]]})
    ### FROM: https://stackoverflow.com/questions/613183/how-do-i-sort-a-dictionary-by-value
    Volatilities_picked = {k: v for k, v in sorted(Volatilities_picked.items(),
                                                   reverse=True, key=lambda item: item[1])}
    ### END FROM
    st.write(Volatilities_picked)
    x = Volatilities_picked.keys()
    y = Volatilities_picked.values()
    fig = plt.figure()
    ax = fig.add_axes([0, 0, 1, 1])
    ax.bar(x, y, color='orange')
    st.pyplot(fig)
    """
    This is volatility of returns of the cryptocurrencies. If you picked Tether or USD Coin you can see that their 
    volatility is almost 0.
    It happens because their price is locked at the level of 1 USD.
    ### Mean yearly returns from the cryptocurrencies
    """
    Bitcoin_mean = (1+np.mean(Bitcoin_returns)) ** 12 - 1
    Ethereum_mean = (1+np.mean(Ethereum_returns)) ** 12 - 1
    Tether_mean = (1+np.mean(Tether_returns)) ** 12 - 1
    Binance_Coin_mean = (1+np.mean(Binance_Coin_returns)) ** 12 - 1
    USD_Coin_mean = (1+np.mean(USD_Coin_returns)) ** 12 - 1
    Solana_mean = (1+np.mean(Solana_returns)) ** 12 - 1
    Dogecoin_mean = (1+np.mean(Dogecoin_returns)) ** 12 - 1
    Means = {'Bitcoin': Bitcoin_mean, 'Ethereum': Ethereum_mean,
             'Tether': Tether_mean, 'Binance Coin': Binance_Coin_mean, 'USD Coin': USD_Coin_mean,
             'Solana': Solana_mean, 'Dogecoin': Dogecoin_mean}
    Means_picked = {}
    for n in range(len(Means)):
        if keys[n] in options:
            Means_picked.update({f'{keys[n]}': Means[keys[n]]})
    ### FROM: https://stackoverflow.com/questions/613183/how-do-i-sort-a-dictionary-by-value
    Means_picked = {k: v for k, v in sorted(Means_picked.items(),
                    reverse=True, key=lambda item: item[1])}
    ### END FROM

    x = Means_picked.keys()
    y = Means_picked.values()
    fig = plt.figure()
    ax = fig.add_axes([0, 0, 1, 1])
    ax.bar(x, y, color='orange')
    st.pyplot(fig)

    """
    As Tether's and USD Coin's prices are locked we can see that their returns are 0 as well*
    #### Now we can compute a very important factor in investment called coefficient of variation. It can be derived by dividing standard deviation of the returns by its mean
    ##### The lower the number the better the investment is.
    """
    """
    Coefficient of variation (COV) of these currencies is:
    """
    COV_picked = {key: Volatilities_picked[key] ** 0.5 // Means_picked.get(key, 0)
                  for key in Means_picked.keys()}
    ### FROM: https://stackoverflow.com/questions/613183/how-do-i-sort-a-dictionary-by-value
    COV_picked = {k: v for k, v in sorted(COV_picked.items(),
                  reverse=False, key=lambda item: item[1])}
    ### END FROM
    x = COV_picked.keys()
    y = COV_picked.values()
    fig = plt.figure()
    ax = fig.add_axes([0, 0, 1, 1])
    ax.bar(x, y, color='orange')
    st.pyplot(fig)
    """
    Expectedly USD Coin and Tether have the worst coefficients as they give 0 returns. If you need a closer look at 
    other cryptocurrencies it is recommended to delete USD Coin and Tether from the analysis.
    #### The first investment from the left is considered the most lucrative from the ones you have picked. You can fearlessly invest in it, good luck.
    """
    st.write(COV_picked)