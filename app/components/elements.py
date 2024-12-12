"""Define the elements of the app."""

import matplotlib.pyplot as plt
import pandas as pd

from app.schemas.strats import BackTestComponents
from app.strats.moving_window import back_testing
from app.utils.fetch_stock import fetch_stock_history


def plot_stock_back_test(stock_symbol, start_date, end_date, drops):
    # Fetch the historical stock data
    history_data = fetch_stock_history(stock_symbol, start_date, end_date)

    # Extract all "close" elements from the history data
    close_prices = history_data["Close"].tolist()
    all_dates = history_data.index.tolist()

    # Pass the close prices to the back_testing function
    intervals = back_testing(close_prices, drops)

    # Plot the intervals against the dates
    fig, ax = plt.subplots()
    ax.plot(all_dates, close_prices, label="Back Test Intervals")
    ax.set_xlabel("Date")
    ax.set_ylabel("Intervals")
    ax.set_title(f"Stock Back Test for {stock_symbol}")
    ax.legend()
    ax.grid(True)

    result_df = []

    for left, right, top_v, bottom_v in intervals:
        result_df.append(
            {
                "High Date": all_dates[left].strftime("%Y-%m-%d"),
                "Low Date": all_dates[right].strftime("%Y-%m-%d"),
                "High Value": top_v,
                "Low Value": bottom_v,
            }
        )

        ax.axvspan(all_dates[left], all_dates[right], color="yellow", alpha=0.3)

    return BackTestComponents(fig=fig, result_df=pd.DataFrame(result_df))
