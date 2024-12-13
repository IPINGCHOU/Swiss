"""module to get stock data"""

from datetime import datetime
from typing import Optional

import pandas as pd
import yfinance as yf  # type: ignore


def fetch_stock_from_yfinance(
    stock_code: str, start_date: datetime, end_date: Optional[datetime] = None
) -> pd.DataFrame:
    """
    Fetch historical stock data for a given stock code between start and end dates.

    Args:
        stock_code (str): Stock ticker symbol (e.g., 'AAPL' for Apple)
        start_date (str): Start date in 'YYYY-MM-DD' format
        end_date (str): End date in 'YYYY-MM-DD' format (optional, defaults to today)

    Returns:
        pd.DataFrame: Historical stock data
    """
    try:
        # If end_date is not provided, use today's date
        if end_date is None:
            input_end_date = datetime.now()
        else:
            input_end_date = end_date
        # Create ticker object
        ticker = yf.Ticker(stock_code)

        # Fetch historical data
        hist = ticker.history(
            start=start_date,
            end=input_end_date,
            interval="1d",
            auto_adjust=True,
        )

        return hist

    except ValueError as e:
        print(f"ValueError fetching data for {stock_code}: {str(e)}")
        return pd.DataFrame()
