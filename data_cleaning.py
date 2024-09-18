import pandas as pd
import numpy as np

def clean_data(df):
    """
    Clean the dataset by converting data types and handling missing or invalid values.
    """
    # Ensure column names are standardized
    df.columns = df.columns.str.strip().str.lower()

    # Convert 'month' column to datetime
    if 'month' in df.columns:
        df['month'] = pd.to_datetime(df['month'], errors='coerce')
        # Drop rows where 'month' could not be converted to datetime
        df = df.dropna(subset=['month'])
    else:
        raise KeyError("The 'month' column is missing from the data.")

    # Define expected numeric columns
    numeric_columns = [
        'sales', 'qty', 'strategy1', 'strategy2', 'strategy3',
        'salesvisit1', 'salesvisit2', 'salesvisit3', 'salesvisit4', 'salesvisit5'
    ]

    # Convert existing numeric columns to float
    for col in numeric_columns:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')

    # Handle infinite values
    df.replace([np.inf, -np.inf], np.nan, inplace=True)

    # Convert 'accid' column to string if it exists
    if 'accid' in df.columns:
        df['accid'] = df['accid'].astype(str)

    # Convert remaining object columns to string
    object_columns = df.select_dtypes(include='object').columns
    for col in object_columns:
        df[col] = df[col].astype(str)

    return df
