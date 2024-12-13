"""Module to interact with Firebase Firestore."""

import os

import pandas as pd
from firebase_admin import credentials, firestore, initialize_app


class FirebaseDatabaseManager:
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

        return True

    def fetch_stock_history(self) -> bool:
        """todo"""
        return True


# Create a global instance of FirebaseManager
# Get the path from an environment variable
cred_path = os.getenv("FIREBASE_CREDENTIALS")
cred = credentials.Certificate(cred_path)
initialize_app(cred)
firebase_db = firestore.client()
firebase_manager = FirebaseDatabaseManager(firebase_db)
