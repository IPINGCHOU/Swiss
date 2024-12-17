"""Tests for the app.utils module."""

from datetime import datetime

import pytest

from app.utils.external_data_helper import fetch_stock


@pytest.mark.parametrize(
    "symbol, start_d, end_d", [("SPY", datetime(2024, 11, 1), datetime(2024, 11, 30))]
)
def test_fetch_stock(symbol, start_d, end_d):
    """
    This test checks if the fetch_stock_history function correctly fetches
    """
    result = fetch_stock.fetch_stock_from_yfinance(symbol, start_d, end_d)

    assert result is not None
