import pandas as pd
import numpy as np
import streamlit as st
from scipy import stats
import seaborn as sns
import matplotlib.pyplot as plt

def clean_data(df):
    """
    Clean the dataset by converting data types, handling missing or invalid values,
    and ensuring compatibility with Arrow serialization.
    """
    # Ensure column names are standardized
    df.columns = df.columns.str.strip().str.lower()
    
    # Drop the 'Unnamed: 0' column if it exists
    if 'unnamed: 0' in df.columns:
        df.drop(columns=['unnamed: 0'], inplace=True)
    
    # Convert 'month' column to datetime
    if 'month' in df.columns:
        df['month'] = pd.to_datetime(df['month'], errors='coerce')
        df['month'].fillna(pd.Timestamp('1970-01-01'), inplace=True)
    else:
        raise KeyError("The 'month' column is missing from the data.")
    
    # Convert 'acctype' to categorical type
    if 'acctype' in df.columns:
        df['acctype'] = df['acctype'].astype('category')
    
    # Handle 'qty' column specifically
    if 'qty' in df.columns:
        df['qty'] = pd.to_numeric(df['qty'], errors='coerce')
        df = df.dropna(subset=['qty'])  # Drop rows where 'qty' is NaN
    
    # Handle other numerical columns similarly
    numeric_columns = [
        'sales', 'qty', 'strategy1', 'strategy2', 'strategy3',
        'salesvisit1', 'salesvisit2', 'salesvisit3', 'salesvisit4', 'salesvisit5'
    ]
    
    # Convert all numeric columns
    for col in numeric_columns:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')
            df[col] = df[col].replace([np.inf, -np.inf], np.nan)
            # Keep NaN values if necessary, but ensure the column is numeric
    
    # Handle 'accid' column as before (if required)

    st.write("Data Types of Cleaned DataFrame:")
    st.write(df_cleaned.dtypes)

    st.write("First few rows of the DataFrame:")
    st.write(df_cleaned[['qty']].head())

    
    return df
