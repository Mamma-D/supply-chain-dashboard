""" this scripts calls APIs and gets 5 yaer history for the two tickers given to it
and it displays its charts"""

import yfinance as yf
import plotly.graph_objects as go
from plotly.subplots import make_subplots


def get_ticker(n_of_runs=2):
    """this function gets a ticker from user and checks whether its valid or not"""

    tickers = []

    for i in range(n_of_runs):

        while True:

            user_input = input('\n-----Enter the ticker name-----\n')

            try:
                input_cap = user_input.upper()
                ticker_obj = yf.Ticker(input_cap)

                #checking to see if the ticker is valid
                if len(ticker_obj.info) < 2:
                    raise NameError(f"Name {input_cap} does not exist.")

                tickers.append(ticker_obj)
                break

            except (AttributeError, NameError):
                print("\n-----Your input isn't valid, try again-----")

    return tuple(tickers)


def get_df(user_ticker_1, user_ticker_2):
    """this function receives each tickers data frame from yahoo finance"""

    df_1 = user_ticker_1.history('5y')
    df_2 = user_ticker_2.history('5y')

    if (not df_1.empty) and (not df_2.empty):

        first_ticker_name = user_ticker_1.info.get('shortName')
        second_ticker_name = user_ticker_2.info.get('shortName')
        return {first_ticker_name:df_1,
                second_ticker_name:df_2}


def make_avg (data_frames_with_name, n=30):
    """this function adds a new column of 'n MA' to the price data frame.(n default is 30)"""

    for df in data_frames_with_name.values():

        rolled_prices = df['Close'].rolling(n)

        df['30 MA'] = rolled_prices.mean()

    return data_frames_with_name

def make_fig(df_wn):
    """this function makes charts for each df gievn to it"""

    dict_keys_list = list(df_wn.keys())
    ticker_name_1 = dict_keys_list[0]
    ticker_name_2 = dict_keys_list[1]

    fig = make_subplots(
        cols=1,
        rows=2,
        shared_xaxes= True,
        vertical_spacing=0.1,
        subplot_titles=(ticker_name_1,ticker_name_2)
    )

    color_sets=[
        ('green', 'lightgreen'),
        ('blue', 'lightblue')
    ]

    for (name, df), (primary_color, secondary_color) in zip(df_wn.items(), color_sets):

    # * Adding the price scatter (lines)
        fig.add_trace(
            go.scatter(
                x=df.index,
                y=df.Close,
                name=f'{name} Price',
                line=dict(color=primary_color),
                row=1, col=1
            )
        )

    # * Adding the moving average scatter

        fig.add_trace(go.scatter(
            x=df.index,
            y=df['30 MA'],
            name=f'{name} 30 MA',
            line=dict(
                color=secondary_color, width='1'),
                row=1, col=1))

    return fig


def show_fig(figs):
    """this functions shows each chart given to it"""

    for fig in figs:
        fig.show()


if __name__ == '__main__':

    ticker_rec_1, ticker_rec_2 = get_ticker()

    dataframes_received = get_df(ticker_rec_1, ticker_rec_2)

    data_frames_with_average = make_avg(dataframes_received)

    figs_created = make_fig(data_frames_with_average)

    show_fig(figs_created)
