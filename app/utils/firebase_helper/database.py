import pandas as pd
from google.cloud import firestore


def save_stock_history_to_firebase(
    db: firestore.Client, stock_code: str, df: pd.DataFrame
) -> None:
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
        db.collection("stock_data").document(stock_code).collection("history")
    )

    # Convert DataFrame to dictionary and save each row as a document
    for index, row in df.iterrows():
        if isinstance(index, pd.Timestamp):
            doc_ref = collection_ref.document(index.strftime("%Y%m%d"))
        else:
            raise ValueError("Index is not a datetime object")
        doc_ref.set(row.to_dict())
        row_dict = row.to_dict()
        row_dict["Date"] = index
        doc_ref.set(row_dict)
