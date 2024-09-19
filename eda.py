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
    Plot a correlation matrix for all variables in the dataset, including categorical ones.
    """
    # Display the columns and first few rows for debugging
    st.write("Column Headers in Cleaned DataFrame:")
    st.write(df.columns)  # Shows the columns available in the cleaned DataFrame
    st.write("First few rows of the DataFrame:")
    st.write(df.head())  # Shows the first few rows of the cleaned DataFrame

    # List of all columns we want to include
    all_columns = [
        'accid', 'acctype', 'accsize', 'acctargets', 'district', 'sales', 'qty',
        'strategy1', 'strategy2', 'strategy3', 'salesvisit1', 'salesvisit2',
        'salesvisit3', 'salesvisit4', 'salesvisit5', 'compbrand'
    ]
    
    # Filter to only the columns that exist in the DataFrame
    available_columns = [col for col in all_columns if col in df.columns]
    
    if not available_columns:
        st.warning("No columns available for correlation matrix.")
        return
    
    # Create a copy of the DataFrame with only the available columns
    df_corr = df[available_columns].copy()

    # Function to convert to numeric if possible, otherwise to categorical
    def to_numeric_or_categorical(column):
        if pd.api.types.is_numeric_dtype(column):
            return column
        else:
            try:
                return pd.to_numeric(column)
            except ValueError:
                return column.astype('category')
    
    # Apply the conversion function to each column
    for col in df_corr.columns:
        df_corr[col] = to_numeric_or_categorical(df_corr[col])
    
    # Create a correlation matrix
    corr_matrix = pd.DataFrame(index=df_corr.columns, columns=df_corr.columns)
    
    for col1 in df_corr.columns:
        for col2 in df_corr.columns:
            if df_corr[col1].dtype.name == 'category' or df_corr[col2].dtype.name == 'category':
                # Use Cramer's V for categorical variables
                try:
                    cramers_v = calculate_cramers_v(df_corr[col1], df_corr[col2])
                    corr_matrix.loc[col1, col2] = cramers_v
                except ValueError:
                    corr_matrix.loc[col1, col2] = np.nan
            else:
                # Use Pearson correlation for numeric variables
                corr_matrix.loc[col1, col2] = df_corr[col1].corr(df_corr[col2])
    
    # Convert correlation matrix to float
    corr_matrix = corr_matrix.astype(float)
    
    # Plot correlation matrix
    plt.figure(figsize=(20, 16))
    sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', linewidths=0.5, fmt='.2f', square=True)
    plt.title("Correlation Matrix of All Key Metrics")
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


