import streamlit as st
import yfinance as yf
import summer

#* -----Defining a function for getting user tickers-----

def get_ticker():
    """this function gets a ticker from user and checks whether its valid or not"""


    first_ticker = st.text_input("Target Company")
    st.caption("e.g., NVDA, TSLA...")
    second_ticker = st.text_input('Critical Raw Material')
    st.caption("e.g., Copper (HG=F) or Aluminum (ALI=F)")

    if (not first_ticker) or (not second_ticker):
        st.error('You must fill every inputs!')
        st.stop()

    first_converted = yf.Ticker(first_ticker)
    second_converted = yf.Ticker(second_ticker)

    # checking to see if tickers are valid
    if len(first_converted.info) < 2:
        st.error(f'Ticker "{first_ticker}" does not exist!')
        st.stop()

    elif len(second_converted.info) < 2:
        st.error(f'Ticker "{second_ticker}" does not exist!')
        st.stop()

    elif first_ticker == second_ticker:
        st.error("You can't type the same thing twice!")
        st.stop()

    return ((first_converted, first_ticker), (second_converted, second_ticker))


#! -----Setting up the steamlit page-----
#* Initial page settings
st.set_page_config(page_title='Chart Showcase',
                   page_icon="📊",
                   layout="wide")

#* Adding a title
st.markdown("<h1 style='text-align: center;'>Chart Showcase</h1>", unsafe_allow_html=True)
st.space('small')

#* Defining two columns
col_1, col_2 = st.columns([1,4])

#* -----Running column one-----
with col_1:
    with st.container(border=True):

        # Getting the tickers from user
        (first_tick, first_str), (second_tick, second_str) = get_ticker()

        # Requesting the data frame
        dataframes_received = summer.get_df(first_tick, second_tick)

        # checking for empty data frames
        dataframes_list = list(dataframes_received.values())

        company_df = dataframes_list[0]
        material_df = dataframes_list[1]

        if company_df.empty:
            st.error(f'The data frame founded for "{first_str}" is empty!')
            st.stop()

        elif material_df.empty:
            st.error(f'The data frame founded for "{second_str}" is empty!')
            st.stop()

        #* Moving average
        ma_toggle = st.toggle("Moving average")
        if ma_toggle:
            # Making a number input to get moving average period
            ma_n = st.number_input('Enter the moving average day period', value=30)

            # Creating the moving average column in the data frame
            data_frames_with_average = summer.make_avg(dataframes_received, ma_n)

        user_pct = st.slider('Simulate Material Price Shock (%)', value=0, min_value=-100, max_value=100)
        summer.change_affect_dynamic(company_df, material_df, user_pct)

        # Creating the plot in plotly
        figs_created = summer.make_fig(dataframes_received, bool(user_pct), ma_toggle)


#* -----Running column two-----
with col_2:
    with st.container(border=True):

        # Displaying the plot
        st.plotly_chart(figs_created, config={'displayModeBar': False})
