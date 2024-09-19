import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# Function for time series analysis of sales and competitor brands over time
def time_series_analysis(df):
    """
    Time Series Analysis of Sales and Competitor Brands Over Time.
    """
    st.header("Time Series Analysis: Sales and Competitor Brands Over Time")
    
    # Step 1: Ensure 'month' is in datetime format
    df['month'] = pd.to_datetime(df['month'], errors='coerce')

    # Step 2: Filter out rows where 'month', 'compBrand', or 'sales' are missing
    df = df.dropna(subset=['month', 'compbrand', 'sales'])

    # Step 3: Convert 'sales' and 'compbrand' to numeric if needed
    df['compbrand'] = pd.to_numeric(df['compbrand'], errors='coerce')
    df['sales'] = pd.to_numeric(df['sales'], errors='coerce')

    # Step 4: Group the data by 'month' and calculate the mean sales and competitor brands per month
    monthly_sales = df.groupby(df['month'].dt.to_period('M'))['sales'].mean()
    monthly_comp_brands = df.groupby(df['month'].dt.to_period('M'))['compbrand'].mean()

    # Step 5: Plot sales and competitor brands over time in a dual-axis plot
    fig, ax1 = plt.subplots(figsize=(12, 6))

    # Plot sales over time
    ax1.plot(monthly_sales.index.astype(str), monthly_sales, color='b', marker='o', label='Sales')
    ax1.set_xlabel('Time (Year-Month)')
    ax1.set_ylabel('Average Sales (USD)', color='b')

    # Create another axis for the competitor brands
    ax2 = ax1.twinx()
    ax2.plot(monthly_comp_brands.index.astype(str), monthly_comp_brands, color='r', marker='x', label='Competitor Brands')
    ax2.set_ylabel('Average Number of Competitor Brands', color='r')

    # Customize the plot
    ax1.set_title('Sales and Competitor Brands Over Time')
    ax1.grid(True)

    fig.tight_layout()
    st.pyplot(fig)

# Function to analyze the impact of marketing strategies in the presence of competitors
def analyze_marketing_strategy_impact(df):
    """
    Analyze the impact of marketing strategies on sales, considering the number of competitor brands.
    """
    st.header("Impact of Marketing Strategies in the Presence of Competitor Brands")
    
    # Ensure 'compbrand', 'sales', 'strategy1', 'strategy2', 'strategy3' are numeric
    df['compbrand'] = pd.to_numeric(df['compbrand'], errors='coerce')
    df['sales'] = pd.to_numeric(df['sales'], errors='coerce')
    df['strategy1'] = pd.to_numeric(df['strategy1'], errors='coerce')
    df['strategy2'] = pd.to_numeric(df['strategy2'], errors='coerce')
    df['strategy3'] = pd.to_numeric(df['strategy3'], errors='coerce')

    # Drop rows with missing values
    df = df.dropna(subset=['compbrand', 'sales', 'strategy1', 'strategy2', 'strategy3'])

    # Strategy 1 vs Sales
    st.subheader("Strategy 1 Expenditure vs Sales Colored by Competitor Brands")
    plt.figure(figsize=(12, 8))
    sns.scatterplot(x='strategy1', y='sales', hue='compbrand', data=df, palette='coolwarm')
    plt.title('Strategy 1 Expenditure vs Sales Colored by Competitor Brands')
    st.pyplot(plt)

    # Strategy 2 vs Sales
    st.subheader("Strategy 2 Expenditure vs Sales Colored by Competitor Brands")
    plt.figure(figsize=(12, 8))
    sns.scatterplot(x='strategy2', y='sales', hue='compbrand', data=df, palette='coolwarm')
    plt.title('Strategy 2 Expenditure vs Sales Colored by Competitor Brands')
    st.pyplot(plt)

    # Strategy 3 vs Sales
    st.subheader("Strategy 3 Expenditure vs Sales Colored by Competitor Brands")
    plt.figure(figsize=(12, 8))
    sns.scatterplot(x='strategy3', y='sales', hue='compbrand', data=df, palette='coolwarm')
    plt.title('Strategy 3 Expenditure vs Sales Colored by Competitor Brands')
    st.pyplot(plt)

# Main function to run the competitor analysis
def run_competitor_analysis(df):
    """
    Run the competitor analysis including time series analysis and impact of marketing strategies.
    """
    time_series_analysis(df)
    analyze_marketing_strategy_impact(df)
