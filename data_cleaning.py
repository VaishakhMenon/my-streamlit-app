import pandas as pd
import numpy as np
import streamlit as st

def clean_data(df):
    """
    Clean the dataset by converting data types, handling missing or invalid values,
    removing outliers and negative values, and ensuring compatibility with Arrow serialization.
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

    # Remove rows with negative sales values (if applicable)
    if 'sales' in df.columns:
        df = df[df['sales'] >= 0]

    # Handle outliers in 'sales' using the IQR method
    if 'sales' in df.columns:
        Q1 = df['sales'].quantile(0.25)
        Q3 = df['sales'].quantile(0.75)
        IQR = Q3 - Q1
        # Define bounds for outliers
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR
        # Remove outliers
        df = df[(df['sales'] >= lower_bound) & (df['sales'] <= upper_bound)]

    # Define expected numeric columns
    numeric_columns = [
        'sales', 'qty', 'strategy1', 'strategy2', 'strategy3',
        'salesvisit1', 'salesvisit2', 'salesvisit3', 'salesvisit4', 'salesvisit5'
    ]

    # Convert existing numeric columns to float and handle infinities and NaNs
    for col in numeric_columns:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')
            # Replace infinite values with NaN
            df[col] = df[col].replace([np.inf, -np.inf], np.nan)
            # Fill NaN values with zero
            df[col] = df[col].fillna(0)

    # Convert 'accid' column to string if it exists and handle NaNs
    if 'accid' in df.columns:
        df['accid'] = df['accid'].astype(str)
        # Replace NaN with empty string
        df['accid'] = df['accid'].fillna('')

    # Convert any remaining object columns to string and fill NaN with empty string
    object_columns = df.select_dtypes(include=['object']).columns
    for col in object_columns:
        df[col] = df[col].astype(str)
        df[col] = df[col].fillna('')

    # Handle remaining columns based on data type
    for col in df.columns:
        if df[col].dtype.kind in 'O':  # Object types
            df[col] = df[col].astype(str)
            df[col] = df[col].fillna('')
        elif df[col].dtype.kind in 'iufc':  # Numeric types
            df[col] = df[col].fillna(0)
        elif df[col].dtype.kind == 'b':  # Boolean types
            df[col] = df[col].fillna(False)
        elif df[col].dtype.kind == 'M':  # Datetime types
            df[col] = df[col].fillna(pd.Timestamp('1970-01-01'))
        else:
            df[col] = df[col].astype(str)
            df[col] = df[col].fillna('')

    # Ensure there are no remaining NaN values
    df = df.fillna('')

    return df
