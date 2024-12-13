"""Tests for the app.utils module."""

import pytest

from app.utils import fetch_stock


@pytest.mark.parametrize(
    "symbol, start_d, end_d", [("SPY", "2024-11-01", "2024-11-30")]
)
def test_fetch_stock(symbol, start_d, end_d):
    """
    This test checks if the fetch_stock_history function correctly fetches
    """
    result = fetch_stock.fetch_stock_history(symbol, start_d, end_d)

    print(result)
    print("hi")
    assert result is not None
