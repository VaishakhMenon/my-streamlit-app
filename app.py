import streamlit as st
import pandas as pd
from utils import load_and_clean_data_from_airtable
from eda import plot_correlation_matrix, plot_sales_by_account_type, plot_sales_trend
from regression import perform_regression
from time_series_analysis import analyze_time_series
from market_segmentation import perform_segmentation
from competitor_analysis import analyze_competitors
from future_budget import forecast_budget
from simulate_reallocation_and_switching_cost import simulate_reallocation_and_switching_costs

# Title of the Streamlit app
st.title("Airtable Data Analysis App")

# Sidebar for Airtable Base ID and Table Name input
st.sidebar.header("Airtable Input")

# Option to use secrets or manual input
use_secrets = st.sidebar.checkbox("Use credentials from secrets", value=True)

if use_secrets:
    airtable_token = st.secrets["airtable"]["token"]
    base_id = st.secrets["airtable"]["base_id"]
    table_name = st.secrets["airtable"]["table_name"]
else:
    airtable_token = st.sidebar.text_input("Enter your Airtable API Token:", "")
    base_id = st.sidebar.text_input("Enter your Airtable Base ID:", "")
    table_name = st.sidebar.text_input("Enter your Airtable Table Name:", "")

if 'df_cleaned' not in st.session_state:
    st.session_state.df_cleaned = None

if airtable_token and base_id and table_name:
    st.sidebar.header("Data Processing")
    
    if st.sidebar.button("Load and Clean Data"):
        try:
            df_cleaned = load_and_clean_data_from_airtable(airtable_token, base_id, table_name)
            st.session_state.df_cleaned = df_cleaned
            st.write("Cleaned Data:", df_cleaned.head())
        except Exception as e:
            st.error(f"Error loading or cleaning data: {e}")

    if st.session_state.df_cleaned is not None:
        st.sidebar.header("Analysis")
        
        if st.sidebar.button("Plot Correlation Matrix"):
            plot_correlation_matrix(st.session_state.df_cleaned)
        
        if st.sidebar.button("Plot Sales by Account Type"):
            plot_sales_by_account_type(st.session_state.df_cleaned)

        if st.sidebar.button("Plot Sales Trend"):
            plot_sales_trend(st.session_state.df_cleaned)

        if st.sidebar.button("Run Regression Analysis"):
            perform_regression(st.session_state.df_cleaned)

        if st.sidebar.button("Time Series Analysis"):
            analyze_time_series(st.session_state.df_cleaned)

        if st.sidebar.button("Market Segmentation"):
            perform_segmentation(st.session_state.df_cleaned)

        if st.sidebar.button("Competitor Analysis"):
            analyze_competitors(st.session_state.df_cleaned)

        if st.sidebar.button("Future Budget Allocation"):
            forecast_budget(st.session_state.df_cleaned)

        if st.sidebar.button("Simulate Reallocation and Switching Costs"):
            simulate_reallocation_and_switching_costs(st.session_state.df_cleaned)
else:
    st.info("Please provide your Airtable credentials to load and clean data.")
