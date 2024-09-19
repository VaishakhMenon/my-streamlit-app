import pandas as pd
import numpy as np
import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt
from scipy import stats

def convert_to_numeric(df, columns):
    """
    Convert the specified columns to numeric and handle non-numeric values.
    """
    for col in columns:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')
    return df

def clean_categorical_columns(df, categorical_columns):
    """
    Convert categorical columns to numeric (using one-hot encoding or label encoding).
    """
    for col in categorical_columns:
        if col in df.columns:
            df[col] = df[col].astype('category').cat.codes  # Label encoding
    return df

def plot_correlation_matrix(df):
    """
    Plot a correlation matrix for all variables in the dataset, including those converted to numeric.
    """
    # List of columns to include in the correlation matrix
    numeric_columns = ['accsize', 'acctargets', 'sales', 'qty', 'strategy1', 'strategy2', 
                       'strategy3', 'salesvisit1', 'salesvisit2', 'salesvisit3', 
                       'salesvisit4', 'salesvisit5', 'compbrand', 'quantity']

    categorical_columns = ['accid', 'acctype', 'compbrand']

    # Convert categorical columns to numeric
    df = clean_categorical_columns(df, categorical_columns)

    # Ensure numeric conversion for selected columns
    df = convert_to_numeric(df, numeric_columns + categorical_columns)

    # Remove rows with missing or NaN values in the selected columns
    df_cleaned = df[numeric_columns].dropna()

    # Calculate the correlation matrix
    corr_matrix = df_cleaned.corr()

    # Plot the correlation matrix
    plt.figure(figsize=(14, 10))
    sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', linewidths=0.5)
    plt.title('Correlation Matrix of All Key Metrics')
    plt.tight_layout()
    st.pyplot(plt)

    # Display the correlation matrix as a table
    st.write("Correlation Matrix:")
    st.write(corr_matrix)

def plot_sales_by_account_type(df):
    """
    Plot the distribution of sales by account type.
    """
    # Ensure columns are in lowercase and clean them
    df = df.copy()
    df.columns = df.columns.str.strip().str.lower()

    # Check if required columns are present
    if 'acctype' not in df.columns or 'sales' not in df.columns:
        st.warning("Columns 'acctype' and 'sales' are required for this plot.")
        return

    # Convert 'sales' to numeric and drop NaNs
    df['sales'] = pd.to_numeric(df['sales'], errors='coerce')
    df = df.dropna(subset=['acctype', 'sales'])

    # Optionally handle outliers
    df['sales'] = df['sales'].clip(lower=df['sales'].quantile(0.01), upper=df['sales'].quantile(0.99))

    # Plot with logarithmic scale for better visualization
    plt.figure(figsize=(8, 6))
    sns.boxplot(x='acctype', y='sales', data=df)
    plt.yscale('log')  # Apply log scale to Y-axis
    plt.title("Sales Distribution by Account Type (Log Scale)")
    plt.xticks(rotation=45)
    plt.tight_layout()
    st.pyplot(plt)

def plot_sales_trend(df):
    """
    Plot the monthly sales trend over time with competitor entries.
    """
    # Ensure column names are in lowercase
    df = df.copy()
    df.columns = df.columns.str.strip().str.lower()

    # Check if the required columns are present
    if 'month' not in df.columns or 'sales' not in df.columns:
        st.warning("Columns 'month' and 'sales' are required for this plot.")
        return

    # Convert 'month' to datetime and 'sales' to numeric
    df['month'] = pd.to_datetime(df['month'], errors='coerce')
    df['sales'] = pd.to_numeric(df['sales'], errors='coerce')

    # Drop rows with missing 'month' or 'sales' values
    df = df.dropna(subset=['month', 'sales'])

    # Group the data by month and sum the sales
    df_grouped = df.groupby('month')['sales'].sum().reset_index()

    # Ensure 'month' is sorted in chronological order
    df_grouped = df_grouped.sort_values('month')

    # Competitor entry dates (adjust according to actual data)
    competitor_entry_dates = ['2014-06', '2015-01']

    # Plot the sales trend
    plt.figure(figsize=(10, 6))
    plt.plot(df_grouped['month'], df_grouped['sales'], marker='o', linestyle='-', label='Total Sales in SGD')
    plt.title("Monthly Sales Trend Over Time with Competitor Entries")
    plt.xlabel("Month")
    plt.ylabel("Total Sales in SGD")
    plt.xticks(rotation=45)

    # Add vertical lines for competitor entry dates
    for date in competitor_entry_dates:
        plt.axvline(pd.to_datetime(date), color='red', linestyle='--', label=f'Competitor Entry {date}')

    # Add a legend and grid
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    st.pyplot(plt)


