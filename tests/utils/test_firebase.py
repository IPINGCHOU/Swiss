"""Tests for the utils.firebase_helper module."""

import os
from datetime import datetime, timedelta

from firebase_admin import credentials, firestore, initialize_app

from app.utils.fetch_stock import fetch_stock_history
from app.utils.firebase_helper.database import save_stock_history_to_firebase

# Get the path from an environment variable
cred_path = os.getenv("FIREBASE_CREDENTIALS")
cred = credentials.Certificate(cred_path)
initialize_app(cred)

# Create Firestore client
db = firestore.client()


def test_fetch_and_save_stock_history():
    """
    Test if the fetch_stock_history and save_stock_history_to_firebase functions work correctly.
    """
    # Prepare test data
    symbol = "AAPL"
    end_date = datetime.now().strftime("%Y-%m-%d")
    start_date = (datetime.now() - timedelta(days=10)).strftime("%Y-%m-%d")

    # Fetch stock history
    stock_df = fetch_stock_history(symbol, start_date, end_date)

    # Save to Firebase
    result = save_stock_history_to_firebase(db, symbol, stock_df)

    # Assertions
    assert stock_df is not None
    assert len(stock_df) > 0
    assert result is True
