"""this scripts calls APIs and gets 5 year history for the two tickers given to it
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
                five_year_history = ticker_obj.history("5y")

                # checking to see if the ticker is valid
                if five_year_history.empty:
                    raise NameError(f"Name {input_cap} does not exist.")

                tickers.append(five_year_history)
                break

            except (AttributeError, NameError):
                print("\n-----Your input isn't valid, try again-----")

    return tuple(tickers)


def get_df(user_ticker_1, user_ticker_2):
    """this function receives each tickers data frame from yahoo finance"""

    df_1 = user_ticker_1.history("5y", actions=False)
    df_2 = user_ticker_2.history("5y", actions=False)

    if (df_1.empty) and (df_2.empty):

        raise ValueError("Data frames could not be retrieved. (empty data frames)")

    first_ticker_name = user_ticker_1.info.get("shortName")
    second_ticker_name = user_ticker_2.info.get("shortName")
    return {first_ticker_name: df_1, second_ticker_name: df_2}


def make_fig(df_wn, new_price=False):
    """this function makes charts for each df gievn to it"""

    # * Extracting ticker's names
    dict_keys_list = list(df_wn.keys())
    ticker_name_1 = dict_keys_list[0]
    ticker_name_2 = dict_keys_list[1]

    # * Making two subplots
    fig = make_subplots(
        cols=1,
        rows=3 if new_price else 2,
        shared_xaxes=True,
        vertical_spacing=0.1,
        subplot_titles=(ticker_name_1, ticker_name_2, "Correlation"),
    )

    # * Defining each chart properties including colors and positions in the plot
    color_position = [
        (
            "rgba(37, 152, 28, 0.8)",
            1,
            "rgba(17, 148, 0, 0.0)",
            "rgba(17, 148, 0, 0.4)",
        ),
        (
            "rgba(29, 25, 255, 0.8)",
            2,
            "rgba(17, 36, 226, 0.0)",
            "rgba(17, 36, 226, 0.4)",
        ),
    ]

    # * Adding each scatter to the plot we made earlier with their properties

    for (name, df), (primary_color, position, fill_1, fill_2) in zip(
        df_wn.items(), color_position
    ):

        # * Adding the price scatter (lines)
        fig.add_trace(
            go.Scatter(
                x=df.index,
                y=df.Close,
                name=f"{name}",
                line=dict(color=primary_color, width=1.2),
                fill="tozeroy",
                fillgradient=dict(
                    type="vertical", colorscale=[[0.0, fill_1], [1.0, fill_2]]
                ),
            ),
            row=position,
            col=1,
        )

    # * Adding the new affected price
    if new_price:

        fig.add_trace(
            go.Scatter(
                x=df_wn[ticker_name_1].index,
                y=df_wn[ticker_name_1]["new_price"],
                name="Company new price",
                line=dict(color="red", width=1, dash="solid"),
                fill="tozeroy",
                fillgradient=dict(
                    type="vertical",
                    colorscale=[[0.0, "rgba(255,0,0,0)"], [1.0, "rgba(255,0,0,0.5)"]],
                ),
            ),
            row=1,
            col=1,
        )

        # * Adding the correlation line

        fig.add_trace(
            go.Scatter(
                x=df_wn[ticker_name_1].index,
                y=df_wn[ticker_name_1]["correlation"],
                name="Dynamic Linear Correlation",
                line=dict(color="red", width=1, dash="solid"),
                fill="tozeroy",
                fillgradient=dict(
                    type="vertical",
                    colorscale=[[0.0, "rgba(255,0,0,0)"], [1.0, "rgba(255,0,0,0.5)"]],
                ),
            ),
            row=3,
            col=1,
        )

    # * Applying plotly default dark theme
    fig.update_layout(template="plotly_dark")

    # * Updating the plot applying following changes: Adding title, scretching the charts, relocating the legend
    fig.update_layout(
        title=dict(
            text=f"{ticker_name_1} vs {ticker_name_2}",
            y=0.99,
            x=0.5,
            xanchor="center",
            yanchor="top",
        ),
        font=dict(family="Inter, Helvetica, Arial, sans-serif", color="#d1d5db"),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.05,
            xanchor="center",
            x=0.5,
            font=dict(size=10),
            bgcolor="rgba(0,0,0,0)",
        ),
        margin=dict(b=10),
        hovermode="x unified",
        height=590,
    )

    # * Updating annotations. Making them smaller and darker
    fig.update_annotations(font=dict(size=13, color="#9ca3af"))

    # * Removing vertical guide lines in chart
    fig.update_xaxes(showgrid=False)

    #! ----- AI code block -----

    # *  This block changes your hovering. when you move your mouse in the chart it shows more detailed informations
    fig.update_xaxes(
        showspikes=True,
        spikemode="across",
        spikesnap="cursor",  # follows the mouse smoothly, not jumping between data points
        spikedash="dot",  # dotted instead of solid — reads as a guide, not a cut
        spikecolor="rgba(255,255,255,0.3)",
        spikethickness=1,
    )

    # * This block adds four buttons to top-left that selects time invertals
    fig.update_xaxes(
        rangeselector=dict(
            buttons=[
                dict(count=6, label="6m", step="month", stepmode="backward"),
                dict(count=1, label="1y", step="year", stepmode="backward"),
                dict(count=3, label="3y", step="year", stepmode="backward"),
                dict(step="all", label="All"),
            ]
        ),
        row=1,
        col=1,
    )
    #! ----- AI code block -----

    return fig


def show_fig(fig):
    """this functions shows each chart given to it"""

    fig.show()


def change_affect_dynamic(company_df, material_df, change_prc=0):
    """this function simulates a price change in material and it's effect on the company stock price"""

    if bool(change_prc):

        company_df["Close"] = company_df["Close"].ffill()
        material_df["Close"] = material_df["Close"].ffill()

        company_df["pct_change"] = company_df["Close"].pct_change()
        material_df["pct_change"] = material_df["Close"].pct_change().shift(90)

        rolled_pct_change = company_df["pct_change"].rolling(90, min_periods=60)
        company_df["correlation"] = rolled_pct_change.corr(material_df["pct_change"])

        change_in_company = (change_prc / 100) * company_df["correlation"].fillna(0)

        company_df["new_price"] = company_df["Close"] * (1 + change_in_company)


if __name__ == "__main__":

    # ticker_rec_1, ticker_rec_2 = get_ticker()
    ticker_rec_1, ticker_rec_2 = yf.Ticker("NVDA"), yf.Ticker("TSLA")

    dataframes_received = get_df(ticker_rec_1, ticker_rec_2)

    data_frames_with_average = make_avg(dataframes_received)

    figs_created = make_fig(data_frames_with_average)
    print(data_frames_with_average)
    show_fig(figs_created)
