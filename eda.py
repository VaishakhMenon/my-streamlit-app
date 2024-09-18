import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

def plot_correlation_matrix(df):
    """
    Plot a correlation matrix for numerical variables in the dataset.
    """
    numerical_cols = df.select_dtypes(include='number').columns
    if numerical_cols.empty:
        st.warning("No numerical columns available for correlation matrix.")
        return

    plt.figure(figsize=(10, 8))
    corr_matrix = df[numerical_cols].corr()
    sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', fmt='.2f')
    plt.title("Correlation Matrix")
    st.pyplot(plt.gcf())

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
