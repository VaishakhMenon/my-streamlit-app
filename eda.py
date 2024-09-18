import pandas as pd
import numpy as np
import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt
from scipy import stats as ss

def calculate_cramers_v(x, y):
    """Calculate Cramer's V statistic for categorical-categorical association."""
    confusion_matrix = pd.crosstab(x, y)
    chi2 = ss.chi2_contingency(confusion_matrix)[0]
    n = confusion_matrix.sum().sum()
    min_dim = min(confusion_matrix.shape) - 1
    return np.sqrt(chi2 / (n * min_dim))

def plot_correlation_matrix(df):
    """
    Plot a correlation matrix for all variables in the dataset, including categorical ones.
    """
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
    
    # Display information about data types and unique values
    st.write("Data types and unique values of each column:")
    for col in df_corr.columns:
        st.write(f"{col}: {df_corr[col].dtype.name}, Unique values: {df_corr[col].nunique()}")

# Example usage (you can comment this out if you're importing these functions elsewhere)
# def main():
#     st.title("Correlation Analysis")
#
#     # Assume df is your cleaned dataframe
#     # df = clean_data(your_original_dataframe)
#     
#     plot_correlation_matrix(df)
#
# if __name__ == "__main__":
#     main()
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


