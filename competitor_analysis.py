# competitor_analysis.py

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def analyze_competitors(df):
    """
    Analyze the impact of competitor brands on sales over time.
    """
    st.header("Competitor Analysis")

    # Check if required columns are present
    required_columns = ['month', 'sales', 'compbrand']
    missing_columns = [col for col in required_columns if col not in df.columns]
    if missing_columns:
        st.warning(f"The following required columns are missing from the data: {', '.join(missing_columns)}")
        return

    # Convert 'month' column to datetime if not already
    if not pd.api.types.is_datetime64_any_dtype(df['month']):
        df['month'] = pd.to_datetime(df['month'], errors='coerce')

    # Drop rows with missing or invalid dates
    df = df.dropna(subset=['month'])
    df = df.sort_values('month')

    # Allow users to select competitors to analyze
    competitors = df['compbrand'].unique().tolist()
    selected_competitors = st.multiselect("Select Competitor Brands to Analyze:", competitors, default=competitors)

    if not selected_competitors:
        st.warning("Please select at least one competitor brand.")
        return

    # Filter the DataFrame based on selected competitors
    df_filtered = df[df['compbrand'].isin(selected_competitors)]

    # Group data if needed (e.g., sum sales by month and competitor)
    df_grouped = df_filtered.groupby(['month', 'compbrand']).agg({'sales': 'sum'}).reset_index()

    # Plot the sales trend by competitor brands
    st.write("### Sales Trend by Competitor Brands")
    plt.figure(figsize=(10, 6))
    sns.lineplot(x='month', y='sales', hue='compbrand', data=df_grouped, marker='o')
    plt.title("Sales Trend by Competitor Brands")
    plt.xlabel("Month")
    plt.ylabel("Sales")
    plt.xticks(rotation=45)
    plt.tight_layout()
    st.pyplot(plt)

    # Optionally, display the data used for the plot
    st.write("### Data Used for Analysis")
    st.dataframe(df_grouped)
