"""Main function for the Swiss, runs streamlit app"""

from datetime import date

import streamlit as st

from app.components.elements import plot_stock_back_test


def main() -> None:
    """
    Main function for the Swiss
    """

    st.title("Stock Backtest Analysis")

    # Create input boxes
    stock_symbol = st.text_input("Enter Stock Symbol", "AAPL")

    col1, col2 = st.columns(2)
    with col1:
        start_date = st.date_input("Start Date", date(2020, 1, 1))
    with col2:
        end_date = st.date_input("End Date", date.today())

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
        col1, col2 = st.columns(2)
        with col1:
            st.pyplot(back_test_res.fig)
        with col2:
            st.dataframe(back_test_res.result_df)
            print("hi")


if __name__ == "__main__":
    main()
