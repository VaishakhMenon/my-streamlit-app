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
    if 'acctype' not in df.columns or 'sales' not in df.columns:
        st.warning("Columns 'acctype' and 'sales' are required for this plot.")
        return

    plt.figure(figsize=(8, 6))
    sns.boxplot(x='acctype', y='sales', data=df)
    plt.title("Sales Distribution by Account Type")
    plt.xticks(rotation=45)
    plt.tight_layout()
    st.pyplot(plt.gcf())

def plot_sales_trend(df):
    """
    Plot the monthly sales trend over time.
    """
    if 'month' not in df.columns or 'sales' not in df.columns:
        st.warning("Columns 'month' and 'sales' are required for this plot.")
        return

    df_grouped = df.groupby('month')['sales'].sum().reset_index()

    # Ensure 'month' is sorted in chronological order
    df_grouped = df_grouped.sort_values('month')

    plt.figure(figsize=(10, 6))
    sns.lineplot(x='month', y='sales', data=df_grouped, marker='o')
    plt.title("Monthly Sales Trend")
    plt.xlabel("Month")
    plt.ylabel("Total Sales")
    plt.xticks(rotation=45)
    plt.tight_layout()
    st.pyplot(plt.gcf())
