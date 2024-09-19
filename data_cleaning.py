import pandas as pd
import numpy as np
import streamlit as st

def clean_data(df):
    """
    Clean the dataset by converting data types, handling missing or invalid values,
    and ensuring compatibility with Arrow serialization.
    """
    # Ensure column names are standardized
    df.columns = df.columns.str.strip().str.lower()
    
    # Keep track of the original column order
    original_column_order = df.columns.tolist()

    # Drop the 'Unnamed: 0' column if it exists
    if 'unnamed: 0' in df.columns:
        df.drop(columns=['unnamed: 0'], inplace=True)
    
    # Convert 'month' column to datetime
    if 'month' in df.columns:
        df['month'] = pd.to_datetime(df['month'], errors='coerce')
        df['month'].fillna(pd.Timestamp('1970-01-01'), inplace=True)
    else:
        raise KeyError("The 'month' column is missing from the data.")
    
    # Convert columns to appropriate data types
    if 'accid' in df.columns:
        df['accid'] = df['accid'].astype(str)
    if 'acctype' in df.columns:
        df['acctype'] = df['acctype'].astype('category')
    if 'accsize' in df.columns:
        df['accsize'] = df['accsize'].astype(int)
    if 'acctargets' in df.columns:
        df['acctargets'] = df['acctargets'].astype(int)
    if 'district' in df.columns:
        df['district'] = df['district'].astype(int)
    if 'sales' in df.columns:
        df['sales'] = df['sales'].astype(int)
    if 'qty' in df.columns:
        df['qty'] = pd.to_numeric(df['qty'], errors='coerce')
        df = df.dropna(subset=['qty'])  # Drop rows where 'qty' is NaN
    if 'strategy1' in df.columns:
        df['strategy1'] = df['strategy1'].astype(float)
    if 'strategy2' in df.columns:
        df['strategy2'] = df['strategy2'].astype(float)
    if 'strategy3' in df.columns:
        df['strategy3'] = df['strategy3'].astype(float)
    if 'salesvisit1' in df.columns:
        df['salesvisit1'] = df['salesvisit1'].astype(float)
    if 'salesvisit2' in df.columns:
        df['salesvisit2'] = df['salesvisit2'].astype(float)
    if 'salesvisit3' in df.columns:
        df['salesvisit3'] = df['salesvisit3'].astype(float)
    if 'salesvisit4' in df.columns:
        df['salesvisit4'] = df['salesvisit4'].astype(float)
    if 'salesvisit5' in df.columns:
        df['salesvisit5'] = df['salesvisit5'].astype(float)
    if 'compbrand' in df.columns:
        df['compbrand'] = df['compbrand'].astype(int)

    # Restore the original column order
    df = df[original_column_order]

    # Display data types and first few rows
    st.write("Data Types of Cleaned DataFrame:")
    st.write(df.dtypes)

    st.write("First few rows of the DataFrame:")
    st.write(df.head())

    return df
