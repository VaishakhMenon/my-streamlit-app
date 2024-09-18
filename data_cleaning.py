import pandas as pd
import numpy as np

def clean_data(df):
    """
    Clean the dataset by converting data types, handling missing or invalid values,
    and ensuring compatibility with Arrow serialization.
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
            # Replace infinite values with NaN
            df[col].replace([np.inf, -np.inf], np.nan, inplace=True)
            # Fill NaN values with zero
            df[col].fillna(0, inplace=True)

    # Convert 'accid' column to string if it exists
    if 'accid' in df.columns:
        df['accid'] = df['accid'].astype(str)
        # Replace NaN with empty string
        df['accid'].fillna('', inplace=True)

    # Convert any remaining object columns to string and fill NaN with empty string
    object_columns = df.select_dtypes(include=['object']).columns
    for col in object_columns:
        df[col] = df[col].astype(str)
        df[col].fillna('', inplace=True)

    # Handle remaining columns
    for col in df.columns:
        if df[col].dtype.kind in 'O':
            # For object types, ensure there are no problematic values
            df[col] = df[col].astype(str)
            df[col].fillna('', inplace=True)
        elif df[col].dtype.kind in 'iufc':  # integer, unsigned, float, complex
            # For numeric types, fill NaN with zero
            df[col] = df[col].fillna(0)
        elif df[col].dtype == 'bool':
            # For boolean types, fill NaN with False
            df[col] = df[col].fillna(False)
        elif df[col].dtype.kind == 'M':  # datetime
            # For datetime types, fill NaT with a default date or drop if necessary
            df[col] = df[col].fillna(pd.Timestamp('1970-01-01'))
        else:
            # Convert other types to string
            df[col] = df[col].astype(str)
            df[col].fillna('', inplace=True)

    return df
