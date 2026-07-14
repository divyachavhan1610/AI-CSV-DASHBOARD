import pandas as pd


def clean_data(df):
    """
    Cleans the uploaded dataframe and returns:
    - cleaned dataframe
    - cleaning statistics
    """

    original_rows = df.shape[0]

    # Remove duplicate rows
    duplicates = df.duplicated().sum()
    df = df.drop_duplicates()

    # Count missing values
    missing_before = df.isnull().sum().sum()

    # Fill numeric columns
    numeric_cols = df.select_dtypes(include="number").columns
    df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].median())

    # Fill text columns
    text_cols = df.select_dtypes(include="object").columns
    df[text_cols] = df[text_cols].fillna("Unknown")

    # Convert Date column if available
    if "Date" in df.columns:
        df["Date"] = pd.to_datetime(df["Date"], errors="coerce")

    missing_after = df.isnull().sum().sum()

    cleaning_report = {
        "Rows Before": original_rows,
        "Rows After": df.shape[0],
        "Duplicates Removed": duplicates,
        "Missing Before": missing_before,
        "Missing After": missing_after,
    }

    return df, cleaning_report