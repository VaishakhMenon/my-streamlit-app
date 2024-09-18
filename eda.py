import pandas as pd  # Add this line if pandas is not imported
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

def plot_correlation_matrix(df):
    """
    Plot a correlation matrix for numerical variables in the dataset.
    """
    # Attempt to convert all columns to numeric where possible
    df_numeric = df.copy()
    df_numeric = df_numeric.apply(pd.to_numeric, errors='coerce')

    # Filter to only numeric columns
    numeric_columns = df_numeric.select_dtypes(include=['float64', 'int64']).columns.tolist()

    if not numeric_columns:
        st.warning("No numerical columns available for correlation matrix.")
        return

    # Calculate correlation matrix
    corr_matrix = df_numeric[numeric_columns].corr()

    # Plot correlation matrix
    plt.figure(figsize=(10, 8))
    sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', fmt='.2f')
    plt.title("Correlation Matrix")
    st.pyplot(plt)


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
    Plot the monthly sales trend over time.
    """
    # Ensure column names are in lowercase
    df = df.copy()
    df.columns = df.columns.str.strip().str.lower()

    # Check if the required columns are present
    if 'month' not in df.columns or 'sales' not in df.columns:
        st.warning("Columns 'month' and 'sales' are required for this plot.")
        return

    # Convert 'month' to datetime
    df['month'] = pd.to_datetime(df['month'], errors='coerce')

    # Convert 'sales' to numeric, coercing errors
    df['sales'] = pd.to_numeric(df['sales'], errors='coerce')

    # Drop rows with missing 'month' or 'sales' values
    df = df.dropna(subset=['month', 'sales'])

    # Group the data by month and sum the sales
    df_grouped = df.groupby('month')['sales'].sum().reset_index()

    # Ensure 'month' is sorted in chronological order
    df_grouped = df_grouped.sort_values('month')

    # Plot the sales trend
    plt.figure(figsize=(10, 6))
    sns.lineplot(x='month', y='sales', data=df_grouped, marker='o')
    plt.title("Monthly Sales Trend")
    plt.xlabel("Month")
    plt.ylabel("Total Sales")
    plt.xticks(rotation=45)
    plt.tight_layout()
    st.pyplot(plt.gcf())
