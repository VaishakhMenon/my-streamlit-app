import streamlit as st
import pandas as pd
from utils import load_and_clean_data_from_airtable
from eda import plot_correlation_matrix, plot_sales_by_account_type, plot_sales_trend
from regression import perform_regression
from time_series_analysis import analyze_time_series  # Corrected import statement
from segmentation import perform_segmentation
from competitor_analysis import analyze_competitors
from budgeting import forecast_budget

# Title of the Streamlit app
st.title("Airtable Data Analysis App")

# Sidebar for Airtable Base ID and Table Name input
st.sidebar.header("Airtable Input")

# Option to use secrets or manual input
use_secrets = st.sidebar.checkbox("Use credentials from secrets", value=True)

if use_secrets:
    # Access Airtable credentials from Streamlit secrets
    airtable_token = st.secrets["airtable"]["token"]
    base_id = st.secrets["airtable"]["base_id"]
    table_name = st.secrets["airtable"]["table_name"]
else:
    # Manual input for Airtable credentials
    airtable_token = st.sidebar.text_input("Enter your Airtable API Token:", "")
    base_id = st.sidebar.text_input("Enter your Airtable Base ID:", "")
    table_name = st.sidebar.text_input("Enter your Airtable Table Name:", "")

# Initialize session state for the data if not already set
if 'df_cleaned' not in st.session_state:
    st.session_state.df_cleaned = None

# Load data from Airtable
if airtable_token and base_id and table_name:
    st.sidebar.header("Data Processing")

    if st.sidebar.button("Load and Clean Data"):
        try:
            # Load and clean the data from Airtable using the utility function
            df_cleaned = load_and_clean_data_from_airtable(airtable_token, base_id, table_name)

            # Store the cleaned data in session state
            st.session_state.df_cleaned = df_cleaned

            # Display data types
            st.write("Data Types of Cleaned DataFrame:")
            st.write(df_cleaned.dtypes)

            # Display the cleaned DataFrame
            st.write("Cleaned Data:")
            st.dataframe(df_cleaned)

        except Exception as e:
            st.error(f"Error loading or cleaning data: {e}")

    # Analysis options
    if st.session_state.df_cleaned is not None:
        st.sidebar.header("Analysis")
        if st.sidebar.button("Plot Correlation Matrix"):
            try:
                plot_correlation_matrix(st.session_state.df_cleaned)
            except Exception as e:
                st.error(f"Error plotting correlation matrix: {e}")

        if st.sidebar.button("Plot Sales by Account Type"):
            try:
                plot_sales_by_account_type(st.session_state.df_cleaned)
            except Exception as e:
                st.error(f"Error plotting sales by account type: {e}")

        if st.sidebar.button("Plot Sales Trend"):
            try:
                plot_sales_trend(st.session_state.df_cleaned)
            except Exception as e:
                st.error(f"Error plotting sales trend: {e}")

        if st.sidebar.button("Run Regression Analysis"):
            try:
                perform_regression(st.session_state.df_cleaned)
            except Exception as e:
                st.error(f"Error performing regression analysis: {e}")

        if st.sidebar.button("Time Series Analysis"):
            try:
                analyze_time_series(st.session_state.df_cleaned)  # Corrected function call
            except Exception as e:
                st.error(f"Error performing time series analysis: {e}")

        if st.sidebar.button("Market Segmentation"):
            try:
                perform_segmentation(st.session_state.df_cleaned)
            except Exception as e:
                st.error(f"Error performing market segmentation: {e}")

        if st.sidebar.button("Competitor Analysis"):
            try:
                analyze_competitors(st.session_state.df_cleaned)
            except Exception as e:
                st.error(f"Error performing competitor analysis: {e}")

        if st.sidebar.button("Future Budget Allocation"):
            try:
                forecast_budget(st.session_state.df_cleaned)
            except Exception as e:
                st.error(f"Error performing future budget analysis: {e}")

else:
    st.info("Please provide your Airtable credentials to load and clean data.")
