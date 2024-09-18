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
        # Instead of dropping, fill NaT values with a default date
        df['month'].fillna(pd.Timestamp('1970-01-01'), inplace=True)
    else:
        raise KeyError("The 'month' column is missing from the data.")
    
    # Convert 'acctype' to categorical type
    if 'acctype' in df.columns:
        df['acctype'] = df['acctype'].astype('category')
    
    # Instead of removing rows with negative values, replace them with NaN
    for col in ['sales', 'strategy1', 'strategy2', 'strategy3']:
        df.loc[df[col] < 0, col] = np.nan
    
    # Handle outliers in 'sales' and 'qty' using the IQR method
    if 'sales' in df.columns and 'qty' in df.columns:
        # Boxplots to visualize outliers (optional: for display during cleaning)
        plt.figure(figsize=(10, 6))
        sns.boxplot(data=df['sales'])
        plt.title('Boxplot of Sales')
        st.pyplot(plt)
        plt.figure(figsize=(10, 6))
        sns.boxplot(data=df['qty'])
        plt.title('Boxplot of Quantity')
        st.pyplot(plt)
        
        # Instead of removing outliers, cap them at 3 standard deviations
        for col in ['sales', 'qty']:
            mean = df[col].mean()
            std = df[col].std()
            df[col] = df[col].clip(lower=mean - 3*std, upper=mean + 3*std)
    
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
            # Instead of filling NaN with zero, we'll keep them as NaN for now
    
    # Convert 'accid' column to string if it exists and handle NaNs
    if 'accid' in df.columns:
        df['accid'] = df['accid'].astype(str)
        df['accid'] = df['accid'].replace('nan', '')
    
    # Convert any remaining object columns to string and fill NaN with empty string
    object_columns = df.select_dtypes(include=['object']).columns
    for col in object_columns:
        df[col] = df[col].astype(str)
        df[col] = df[col].replace('nan', '')
    
    # Handle remaining columns based on data type
    for col in df.columns:
        if df[col].dtype.kind in 'O':  # Object types
            df[col] = df[col].astype(str)
            df[col] = df[col].replace('nan', '')
        elif df[col].dtype.kind in 'iufc':  # Numeric types
            # Keep NaN values instead of filling them
            pass
        elif df[col].dtype.kind == 'b':  # Boolean types
            df[col] = df[col].fillna(False)
        elif df[col].dtype.kind == 'M':  # Datetime types
            df[col] = df[col].fillna(pd.Timestamp('1970-01-01'))
        else:
            df[col] = df[col].astype(str)
            df[col] = df[col].replace('nan', '')
    
    # After cleaning, print the data types and available columns
    st.write("Columns after cleaning:", df.columns)
    st.write("Data types after cleaning:")
    st.write(df.dtypes)
    
    # Print the number of NaN values in each column
    st.write("Number of NaN values in each column:")
    st.write(df.isna().sum())
    
    return df
