""" this scripts calls APIs and gets 5 yaer history for the two tickers given to it
and it displays its charts"""

import yfinance as yf
import pandas as pd
import plotly.express as px


def get_df(user_ticker_1, user_ticker_2):
    """this function receives each tickers data frame from yahoo finance"""

    ticker_1 = yf.Ticker(str(user_ticker_1))
    ticker_2 = yf.Ticker(str(user_ticker_2))

    df_1 = ticker_1.history('5y')
    df_2 = ticker_2.history('5y')

    if df_2.empty or df_1.empty: return

    return (df_1, df_2)


def get_tickers():

def make_avg():

def make_fig():

def show_fig():