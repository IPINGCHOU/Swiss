"""Tests for the utils.firebase_helper module."""

from datetime import datetime
from zoneinfo import ZoneInfo

from app.utils.external_data_helper.fetch_stock import fetch_stock_from_yfinance
from app.utils.firebase_helper.stock_db import firebase_stock_database


def test_fetch_and_save_stock_history():
    """
    Test if the fetch_stock_history and save_stock_history_to_firebase functions work correctly.
    """
    # Prepare test data
    symbol = "AAPL"
    start_date = datetime(2024, 12, 1, tzinfo=ZoneInfo("Asia/Tokyo"))
    end_date = datetime(2024, 12, 11, tzinfo=ZoneInfo("Asia/Tokyo"))

    # Fetch stock history
    stock_df = fetch_stock_from_yfinance(symbol, start_date, end_date)

    # Save to Firebase
    result = firebase_stock_database.save_stock_history_to_firebase(symbol, stock_df)

    # Assertions
    assert stock_df is not None
    assert len(stock_df) > 0
    assert result is True


def test_fetch_stock_history():
    """
    Test if the fetch_stock_history function works correctly.
    """

    symbol = "AAPL"
    start_date = datetime(2024, 12, 1, tzinfo=ZoneInfo("Asia/Tokyo"))
    end_date = datetime(2024, 12, 11, tzinfo=ZoneInfo("Asia/Tokyo"))
    stock_df = firebase_stock_database.fetch_stock_history(symbol, start_date, end_date)
    assert stock_df is not None
