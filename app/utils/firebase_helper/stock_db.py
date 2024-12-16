"""Module to interact with Firebase Firestore."""

import os
from datetime import datetime
from typing import Optional, Tuple

import pandas as pd
from firebase_admin import credentials, firestore, initialize_app
from google.cloud.firestore import FieldFilter

from app.utils.fetch_stock import fetch_stock_from_yfinance


class FirebaseStockDatabaseManager:
    """
    A manager class for interacting with Firebase Firestore database.
    Attributes:
        db (firestore.client): Firestore client instance.
    """

    def __init__(self, db: firestore.client):  # type: ignore
        self.db = db

    def save_stock_history_to_firebase(self, stock_code: str, df: pd.DataFrame) -> bool:
        """
        Save DataFrame to Firebase Firestore.

        Args:
            stock_code (str): Stock ticker symbol
            df (pd.DataFrame): DataFrame to save.
                - Date
                - Open
                - High
                - Low
                - Close
                - Volume
                - Dividends
                - Stock Splits
        """
        collection_ref = (
            self.db.collection("stock_data").document(stock_code).collection("history")
        )

        # Convert DataFrame to dictionary and save each row as a document
        for index, row in df.iterrows():
            if isinstance(index, pd.Timestamp):
                doc_ref = collection_ref.document(index.strftime("%Y%m%d"))
            else:
                raise ValueError("Index is not a datetime object")
            row_dict = row.to_dict()
            row_dict["Date"] = index
            doc_ref.set(row_dict)

        # Get the latest and earliest date of the DataFrame
        latest_date = df.index.max()
        earliest_date = df.index.min()
        # get current stock meta date
        hist_latest_date, hist_earliest_date = self.get_stock_last_update(stock_code)

        stock_doc_ref = self.db.collection("stock_data").document(stock_code)
        # Save the latest and earliest date to the document(stock_code)

        if (not hist_latest_date) or (
            datetime.strptime(hist_latest_date, "%Y-%m-%d") < latest_date
        ):
            stock_doc_ref.set({"latest_date": latest_date}, merge=True)

        if (not hist_earliest_date) or (
            datetime.strptime(hist_earliest_date, "%Y-%m-%d") > earliest_date
        ):
            stock_doc_ref.set({"earliest_date": earliest_date}, merge=True)

        return True

    def fetch_stock_history(
        self, stock_code: str, start_date: str, end_date: str
    ) -> pd.DataFrame:
        """
        Fetch stock history from Firebase Firestore within a date range.

        Args:
            stock_code (str): Stock ticker symbol
            start_date (str): Start date in 'YYYY-MM-DD' format
            end_date (str): End date in 'YYYY-MM-DD' format

        Returns:
            pd.DataFrame: DataFrame containing the stock history
        """
        collection_ref = (
            self.db.collection("stock_data").document(stock_code).collection("history")
        )

        # Get the current db date range, if not exist, ask for update
        status = self.check_update(stock_code, start_date, end_date)

        if status is False:
            raise ValueError("Update error!!!")

        # Convert date strings to datetime objects
        # query
        start_ds = datetime.strptime(start_date, "%Y-%m-%d")
        end_ds = datetime.strptime(end_date, "%Y-%m-%d")
        query = collection_ref.where(filter=FieldFilter("Date", ">=", start_ds)).where(
            filter=FieldFilter("Date", "<=", end_ds)
        )
        docs = query.stream()
        data = []
        for doc in docs:
            data.append(doc.to_dict())

        return pd.DataFrame(data)

    def get_stock_last_update(
        self, stock_code: str
    ) -> Tuple[Optional[str], Optional[str]]:
        """
        Get the last update date of the stock data in Firebase Firestore.

        Args:
            stock_code (str): Stock ticker symbol

        Returns:
            latest_date (Optional[datetime]): The latest date of the stock data
            earliest_date (Optional[datetime]): The earliest date of the stock data
        """

        stock_doc_ref = self.db.collection("stock_data").document(stock_code)
        stock_doc = stock_doc_ref.get()

        if stock_doc.exists:
            stock_data = stock_doc.to_dict()
            latest_date = stock_data.get("latest_date", None)
            earliest_date = stock_data.get("earliest_date", None)

            if latest_date:
                latest_date = latest_date.strftime("%Y-%m-%d")
            if earliest_date:
                earliest_date = earliest_date.strftime("%Y-%m-%d")

            return latest_date, earliest_date

        return None, None

    def check_update(
        self, stock_code: str, target_start_date: str, target_end_date: str
    ) -> bool:
        """
        Check if the stock data in Firebase Firestore needs to be updated.

        Args:
            stock_code (str): Stock ticker symbol
            target_start_date (str): The start date of the target date range
            target_end_time (str): The end date of the target date range

        Returns:
            bool: True if the stock data needs to be updated, False otherwise
        """

        hist_latest_date, hist_earliest_date = self.get_stock_last_update(stock_code)

        target_start_date_dt = datetime.strptime(target_start_date, "%Y-%m-%d")
        target_end_date_dt = datetime.strptime(target_end_date, "%Y-%m-%d")

        # double way update
        if (not hist_latest_date) or (not hist_earliest_date):
            # Fetch stock history
            stock_df = fetch_stock_from_yfinance(
                stock_code, target_start_date, target_end_date
            )
            # Save to Firebase
            _ = self.save_stock_history_to_firebase(stock_code, stock_df)
            return True

        hist_earliest_date_dt = datetime.strptime(hist_earliest_date, "%Y-%m-%d")
        hist_latest_date_dt = datetime.strptime(hist_latest_date, "%Y-%m-%d")

        # tail update
        if hist_earliest_date_dt > target_start_date_dt:
            # Fetch stock history
            stock_df = fetch_stock_from_yfinance(
                stock_code, target_start_date, hist_earliest_date
            )
            # Save to Firebase
            _ = self.save_stock_history_to_firebase(stock_code, stock_df)
            return True

        # head update
        if hist_latest_date_dt < target_end_date_dt:
            # Fetch stock history
            stock_df = fetch_stock_from_yfinance(
                stock_code, hist_latest_date, target_end_date
            )
            # Save to Firebase
            _ = self.save_stock_history_to_firebase(stock_code, stock_df)
            return True

        # if no update needed
        if (target_start_date_dt >= hist_earliest_date_dt) and (
            target_end_date_dt <= hist_latest_date_dt
        ):
            return True

        return False


# Create a global instance of FirebaseManager
# Get the path from an environment variable
cred_path = os.getenv("FIREBASE_CREDENTIALS")
cred = credentials.Certificate(cred_path)
initialize_app(cred)
firebase_db = firestore.client()
firebase_stock_database = FirebaseStockDatabaseManager(firebase_db)
