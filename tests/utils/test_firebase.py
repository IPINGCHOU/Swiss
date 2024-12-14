"""Tests for the utils.firebase_helper module."""

from datetime import datetime, timedelta

from app.utils.fetch_stock import fetch_stock_history
from app.utils.firebase_helper.database import firebase_manager


def test_fetch_and_save_stock_history():
    """
    Test if the fetch_stock_history and save_stock_history_to_firebase functions work correctly.
    """
    # Prepare test data
    symbol = "AAPL"
    end_date = datetime.now().strftime("%Y-%m-%d")
    start_date = (datetime.now() - timedelta(days=20)).strftime("%Y-%m-%d")

    # Fetch stock history
    stock_df = fetch_stock_history(symbol, start_date, end_date)

    # Save to Firebase
    result = firebase_manager.save_stock_history_to_firebase(symbol, stock_df)

    # Assertions
    assert stock_df is not None
    assert len(stock_df) > 0
    assert result is True


def test_fetch_stock_history():
    """
    Test if the fetch_stock_history function works correctly.
    """

    symbol = "AAPL"
    start_date = "2024-12-01"
    end_date = "2024-12-12"
    stock_df = firebase_manager.fetch_stock_history(symbol, start_date, end_date)
    assert stock_df is not None

    print(stock_df)
