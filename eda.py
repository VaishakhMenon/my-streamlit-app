import pandas as pd
import numpy as np
import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt
from scipy import stats
from scipy.stats import chi2_contingency
from inference import generate_inference  # Import the inference function

# Function to calculate Cramér's V
def calculate_cramers_v(x, y):
    """
    Calculate Cramér's V statistic for categorical-categorical association.
    """
    confusion_matrix = pd.crosstab(x, y)
    chi2 = chi2_contingency(confusion_matrix)[0]
    n = confusion_matrix.sum().sum()
    r, k = confusion_matrix.shape
    cramers_v = np.sqrt(chi2 / (n * (min(r, k) - 1)))
    return cramers_v


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
    st.write("Column Headers in Cleaned DataFrame:")
    st.write(df.columns)
    st.write("First few rows of the DataFrame:")
    st.write(df.head())

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

    # Generate Inference
    inference_result = generate_inference(corr_matrix.to_dict())  # Pass correlation matrix summary
    st.write(f"Inference: {inference_result}")


def plot_sales_by_account_type(df):
    """
    Plot the distribution of sales by account type.
    """
    df = df.copy()
    df.columns = df.columns.str.strip().str.lower()

    if 'acctype' not in df.columns or 'sales' not in df.columns:
        st.warning("Columns 'acctype' and 'sales' are required for this plot.")
        return

    df['sales'] = pd.to_numeric(df['sales'], errors='coerce')
    df = df.dropna(subset=['acctype', 'sales'])

    df['sales'] = df['sales'].clip(lower=df['sales'].quantile(0.01), upper=df['sales'].quantile(0.99))

    plt.figure(figsize=(8, 6))
    sns.boxplot(x='acctype', y='sales', data=df)
    plt.yscale('log')
    plt.title("Sales Distribution by Account Type (Log Scale)")
    plt.xticks(rotation=45)
    plt.tight_layout()
    st.pyplot(plt)

    # Generate Inference
    sales_summary = df.groupby('acctype')['sales'].describe().to_dict()  # Summary statistics of sales
    inference_result = generate_inference(sales_summary)
    st.write(f"Inference: {inference_result}")


def plot_sales_trend(df):
    """
    Plot the monthly sales trend over time with competitor entries.
    """
    df = df.copy()
    df.columns = df.columns.str.strip().str.lower()

    if 'month' not in df.columns or 'sales' not in df.columns:
        st.warning("Columns 'month' and 'sales' are required for this plot.")
        return

    df['month'] = pd.to_datetime(df['month'], errors='coerce')
    df['sales'] = pd.to_numeric(df['sales'], errors='coerce')

    df = df.dropna(subset=['month', 'sales'])

    df_grouped = df.groupby('month')['sales'].sum().reset_index()

    df_grouped = df_grouped.sort_values('month')

    competitor_entry_dates = ['2014-06', '2015-01']

    plt.figure(figsize=(10, 6))
    plt.plot(df_grouped['month'], df_grouped['sales'], marker='o', linestyle='-', label='Total Sales in SGD')
    plt.title("Monthly Sales Trend Over Time with Competitor Entries")
    plt.xlabel("Month")
    plt.ylabel("Total Sales in SGD")
    plt.xticks(rotation=45)

    for date in competitor_entry_dates:
        plt.axvline(pd.to_datetime(date), color='red', linestyle='--', label=f'Competitor Entry {date}')

    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    st.pyplot(plt)

    # Generate Inference
    sales_trend_summary = df_grouped.to_dict()  # Pass the sales trend data summary
    inference_result = generate_inference(sales_trend_summary)
    st.write(f"Inference: {inference_result}")
