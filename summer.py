"""this scripts calls APIs and gets 5 yaer history for the two tickers given to it
and it displays its charts"""

import yfinance as yf
import plotly.graph_objects as go
from plotly.subplots import make_subplots


def get_ticker(n_of_runs=2):
    """this function gets a ticker from user and checks whether its valid or not"""

    tickers = []

    for _ in range(n_of_runs):

        while True:

            user_input = input("\n-----Enter the ticker name-----\n")

            try:
                input_cap = user_input.strip().upper()
                ticker_obj = yf.Ticker(input_cap)

                # checking to see if the ticker is valid
                if len(ticker_obj.info) < 2:
                    raise NameError(f"Name {input_cap} does not exist.")

                tickers.append(ticker_obj)
                break

            except (AttributeError, NameError):
                print("\n-----Your input isn't valid, try again-----")

    return tuple(tickers)


def get_df(user_ticker_1, user_ticker_2):
    """this function receives each tickers data frame from yahoo finance"""

    df_1 = user_ticker_1.history("5y")
    df_2 = user_ticker_2.history("5y")

    if (df_1.empty) and (df_2.empty):

        raise ValueError("Data frames could not be retrieved. (empty data frames)")

    first_ticker_name = user_ticker_1.info.get("shortName")
    second_ticker_name = user_ticker_2.info.get("shortName")
    return {first_ticker_name: df_1, second_ticker_name: df_2}


def make_avg(data_frames_with_name, n=30):
    """this function adds a new column of 'n MA' to the price data frame.(n default is 30)"""

    for df in data_frames_with_name.values():

        rolled_prices = df["Close"].rolling(n)

        df[f"{n} MA"] = rolled_prices.mean()

    return data_frames_with_name


def make_fig(df_wn):
    """this function makes charts for each df gievn to it"""

    dict_keys_list = list(df_wn.keys())
    ticker_name_1 = dict_keys_list[0]
    ticker_name_2 = dict_keys_list[1]

    fig = make_subplots(
        cols=1,
        rows=2,
        shared_xaxes=True,
        vertical_spacing=0.1,
        subplot_titles=(ticker_name_1, ticker_name_2),
    )

    color_position = [
        (
            "rgba(2, 191, 0, 0.8)",
            "#82D682",
            1,
            "rgba(2, 191, 0, 0.0)",
            "rgba(2, 191, 0, 0.4)",
        ),
        (
            "rgba(17, 36, 226, 0.8)",
            "#4b6ad9",
            2,
            "rgba(17, 36, 226, 0.0)",
            "rgba(17, 36, 226, 0.4)",
        ),
    ]

    for (name, df), (primary_color, secondary_color, position, fill_1, fill_2) in zip(
        df_wn.items(), color_position
    ):

        # * Adding the price scatter (lines)
        fig.add_trace(
            go.Scatter(
                x=df.index,
                y=df.Close,
                name=f"{name} Stock Price",
                line=dict(color=primary_color, width=1),
                fill="tozeroy",
                fillgradient=dict(
                    type="vertical", colorscale=[[0.0, fill_1], [1.0, fill_2]]
                ),
            ),
            row=position,
            col=1,
        )

        # * Adding the moving average scatter

        fig.add_trace(
            go.Scatter(
                x=df.index,
                y=df["30 MA"],
                name="30 MA",
                line=dict(color=secondary_color, width=1, dash="dot"),
            ),
            row=position,
            col=1,
        )

    fig.update_layout(template="plotly_dark")

    fig.update_layout(
        title=f"{ticker_name_1} vs {ticker_name_2} Stock Price",
        height=700,
        font=dict(family="Inter, Helvetica, Arial, sans-serif", color="#d1d5db"),
        legend=dict(orientation="h", 
                    yanchor="bottom",
                    y=1.05,
                    xanchor="right",
                    x=1,
                    bgcolor="rgba(0,0,0,0)"
                    ),
        margin=dict(l=40, r=40, t=40, b=40)
    )

    fig.update_annotations(font=dict(size=13, color="#9ca3af"))

    fig.update_xaxes(showgrid=False)

    #! ----- AI code block -----
    # fig.update_layout(hovermode="x unified")
    # fig.update_xaxes(showspikes=True, spikemode="across", spikecolor="rgba(255,255,255,0.25)", spikethickness=1)
    # fig.update_xaxes(
    # rangeselector=dict(
    #     buttons=[
    #         dict(count=6, label="6m", step="month", stepmode="backward"),
    #         dict(count=1, label="1y", step="year", stepmode="backward"),
    #         dict(count=3, label="3y", step="year", stepmode="backward"),
    #         dict(step="all", label="All"),
    #         ]
    #     ),
    #     row=1, col=1
    # )
    #! ----- AI code block -----

    return fig


def show_fig(fig):
    """this functions shows each chart given to it"""

    fig.show()


if __name__ == "__main__":

    # ticker_rec_1, ticker_rec_2 = get_ticker()
    ticker_rec_1, ticker_rec_2 = yf.Ticker("NVDA"), yf.Ticker("TSLA")

    dataframes_received = get_df(ticker_rec_1, ticker_rec_2)

    data_frames_with_average = make_avg(dataframes_received)

    figs_created = make_fig(data_frames_with_average)

    show_fig(figs_created)
