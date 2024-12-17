"""Main function for the Swiss, runs streamlit app"""

from datetime import datetime

import pytz
import streamlit as st

from app.components.elements import plot_stock_back_test

st.set_page_config(layout="wide")


def main() -> None:
    """
    Main function for the Swiss
    """

    st.title("Stock Backtest Analysis")

    # Create input boxes
    stock_symbol = st.text_input("Enter Stock Symbol", "AAPL")

    # Add country selector
    country = st.selectbox("Select Country", ["US", "JP"])

    # Get timezone based on country
    timezone = (
        pytz.timezone("America/New_York")
        if country == "US"
        else pytz.timezone("Asia/Tokyo")
    )

    col1, col2 = st.columns(2)
    with col1:
        start_date = datetime.combine(
            st.date_input("Start Date", datetime(2024, 11, 1)),  # type: ignore
            datetime.min.time(),
        ).replace(tzinfo=timezone)
    with col2:
        end_date = datetime.combine(
            st.date_input("End Date", datetime.today().date()),  # type: ignore
            datetime.min.time(),
        ).replace(tzinfo=timezone)

    # # Convert to datetime
    # start_date = datetime.combine(start_date, datetime.min.time())
    # end_date = datetime.combine(end_date, datetime.min.time())

    drop_rate = st.number_input(
        "Drop Rate (%)", min_value=0.0, max_value=100.0, value=10.0, step=0.1
    )

    if st.button("Run Backtest"):
        # Convert drop rate to decimal
        drop_rate_decimal = drop_rate / 100.0

        # Create figure using the imported function
        back_test_res = plot_stock_back_test(
            stock_symbol, start_date, end_date, drop_rate_decimal
        )
        # Display the plot and dataframe in two columns
        col1, col2 = st.columns([5, 3])
        with col1:
            st.pyplot(back_test_res.fig)
        with col2:
            st.dataframe(back_test_res.result_df)


if __name__ == "__main__":
    main()
