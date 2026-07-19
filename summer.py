""" this scripts calls APIs and gets 5 yaer history for the two tickers given to it
and it displays its charts"""

import yfinance as yf
import pandas as pd
import plotly.express as px


def get_ticker(n_of_runs=2):
    """this function gets a ticker from user and checks whether its valid or not"""

    tickers = []

    for i in range(n_of_runs):

        while True:
        
            user_input = input('\n-----Enter the ticker name-----\n')
            
            try:
                input_cap = user_input.capitalize()
                ticker_obj = yf.Ticker(input_cap)

                #checking to see if the ticker is valid
                if len(ticker_obj.info) < 2:
                    raise NameError(f"Name {input_cap} does not exist.")

                tickers.append(ticker_obj)

            except AttributeError, NameError:
                print("\n-----Your input isn't valid, try again-----")
    
    return tickers


def get_df(user_ticker_1, user_ticker_2):
    """this function receives each tickers data frame from yahoo finance"""

    while True:

        ticker_1 = yf.Ticker(str(user_ticker_1))
        ticker_2 = yf.Ticker(str(user_ticker_2))

        df_1 = ticker_1.history('5y')
        df_2 = ticker_2.history('5y')

        if (not df_1.empty) and (not df_2.empty):
            return (df_1, df_2)


def make_avg(*args, n=30):
    """this function adds a new column of 'n MA' to the price data frame.(n default is 30)"""

    for df in args:

        rolled_prices = df['Close'].rolling(30)

        df['30 MA'] = rolled_prices.mean()
    
    return None

def make_fig():

def show_fig():