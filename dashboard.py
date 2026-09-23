"""this script is for the front-end streamlit page"""

import streamlit as st
import summer

# * -----Defining a function for getting user tickers-----


def get_ticker():
    """this function gets a ticker from user and checks whether its valid or not"""

    COMPANIES = summer.COMPANIES.keys()
    MATERIALS = summer.MATERIALS.keys()

    first_ticker = st.selectbox("Target Company", COMPANIES)
    st.caption("The company's stock you wanna view")

    second_ticker = st.selectbox("Critical Raw Material", MATERIALS)
    st.caption("The material you wanna see its impact on")

    if (not first_ticker) or (not second_ticker):
        st.error("You must choose both inputs first.")
        st.stop()

    return first_ticker, second_ticker


#! -----Setting up the steamlit page-----
# * Initial page settings
st.set_page_config(page_title="Chart Showcase", page_icon="📊", layout="wide")

# * Adding a title
st.markdown(
    "<h1 style='text-align: center;'>Chart Showcase</h1>", unsafe_allow_html=True
)
st.space("small")

# * Defining two columns
col_1, col_2 = st.columns([1, 4])

# * -----Running column one-----
with col_1:
    with st.container(border=True):

        # Getting the tickers from user
        first_tick, second_tick = get_ticker()

        # Requesting the data frame
        dataframes_received = summer.get_df(first_tick, second_tick)

        user_pct = st.slider(
            "Simulate Material Price Shock (%)", value=0, min_value=-100, max_value=100
        )
        if user_pct:
            dataframes_received = summer.change_affect_dynamic(dataframes_received, user_pct)

        # Creating the plot in plotly
        figs_created = summer.make_fig(dataframes_received, bool(user_pct))


# * -----Running column two-----
with col_2:
    with st.container(border=True):

        # Displaying the plot
        st.plotly_chart(figs_created, config={"displayModeBar": False})
