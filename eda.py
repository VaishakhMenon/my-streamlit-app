import matplotlib.pyplot as plt
import seaborn as sns

def plot_correlation_matrix(df):
    """
    Plot a correlation matrix for numerical variables in the dataset.
    """
    plt.figure(figsize=(10, 8))
    corr_matrix = df.corr(numeric_only=True)
    sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', fmt='.2f')
    plt.title("Correlation Matrix")
    plt.show()

def plot_sales_by_account_type(df):
    """
    Plot the distribution of sales by account type.
    """
    plt.figure(figsize=(8, 6))
    sns.boxplot(x='acctype', y='sales', data=df)
    plt.title("Sales Distribution by Account Type")
    plt.xticks(rotation=45)
    plt.show()

def plot_sales_trend(df):
    """
    Plot the monthly sales trend over time.
    """
    plt.figure(figsize=(10, 6))
    df_grouped = df.groupby('month')['sales'].sum().reset_index()
    sns.lineplot(x='month', y='sales', data=df_grouped)
    plt.title("Monthly Sales Trend")
    plt.xticks(rotation=45)
    plt.show()
