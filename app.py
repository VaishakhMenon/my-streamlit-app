import streamlit as st
import pandas as pd
from data_cleaning import clean_data
from eda import plot_correlation_matrix, plot_sales_by_account_type, plot_sales_trend
from regression import perform_regression
from time_series_analysis import analyze_time_series
from market_segmentation import perform_segmentation
from competitor_analysis import run_competitor_analysis  # Import for competitor analysis
from future_budget import future_budget_forecasting, plot_weighted_budget_allocation
from dollar_value_sales import calculate_sales_from_strategy
from simulate_reallocation_and_switching_cost import (
    simulate_reallocation_and_switching_costs,
    calculate_average_marginal_impact
)
from inference import generate_inference  # Import the inference function
from pyairtable import Api


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

# Initialize session state for the data if not already set
if 'df_cleaned' not in st.session_state:
    st.session_state.df_cleaned = None

# Load data from Airtable
if airtable_token and base_id and table_name:
    st.sidebar.header("Data Processing")

    if st.sidebar.button("Load and Clean Data"):
        try:
            api = Api(airtable_token)
            table = api.table(base_id, table_name)
            records = table.all()
            df = pd.DataFrame([record['fields'] for record in records])
            df_cleaned = clean_data(df)
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

        # Correlation Matrix
        if st.sidebar.button("Plot Correlation Matrix"):
            try:
                plot_correlation_matrix(st.session_state.df_cleaned)
                generate_inference(st.session_state.df_cleaned, "Correlation Matrix")  # Inference
            except Exception as e:
                st.error(f"Error plotting correlation matrix: {e}")

        # Sales by Account Type
        if st.sidebar.button("Plot Sales by Account Type"):
            try:
                plot_sales_by_account_type(st.session_state.df_cleaned)
                generate_inference(st.session_state.df_cleaned, "Sales by Account Type")  # Inference
            except Exception as e:
                st.error(f"Error plotting sales by account type: {e}")

        # Sales Trend
        if st.sidebar.button("Plot Sales Trend"):
            try:
                plot_sales_trend(st.session_state.df_cleaned)
                generate_inference(st.session_state.df_cleaned, "Sales Trend")  # Inference
            except Exception as e:
                st.error(f"Error plotting sales trend: {e}")

        # Regression Analysis
        if st.sidebar.button("Run Regression Analysis"):
            try:
                model = perform_regression(st.session_state.df_cleaned)
                st.session_state.model = model  # Store model in session state
                generate_inference(st.session_state.df_cleaned, "Regression analysis")  # Inference
            except Exception as e:
                st.error(f"Error performing regression analysis: {e}")

        # Time Series Analysis
        if st.sidebar.button("Time Series Analysis"):
            try:
                analyze_time_series(st.session_state.df_cleaned)
                generate_inference(st.session_state.df_cleaned, "Time Series analysis")  # Inference
            except Exception as e:
                st.error(f"Error performing time series analysis: {e}")

        # Market Segmentation
        if st.sidebar.button("Market Segmentation"):
            try:
                perform_segmentation(st.session_state.df_cleaned)
                generate_inference(st.session_state.df_cleaned, "Market Segmentation")  # Inference
            except Exception as e:
                st.error(f"Error performing market segmentation: {e}")

        # Competitor Analysis
        if st.sidebar.button("Competitor Analysis"):
            try:
                run_competitor_analysis(st.session_state.df_cleaned)
                generate_inference(st.session_state.df_cleaned, "Competitor Analysis")  # Inference
            except Exception as e:
                st.error(f"Error performing competitor analysis: {e}")

        # Future Budget Forecasting
        if st.sidebar.button("Future Budget Forecasting"):
            try:
                future_budget_forecasting()
                generate_inference(st.session_state.df_cleaned, "Future Budget Forecasting")  # Inference
            except Exception as e:
                st.error(f"Error in Future Budget Forecasting: {e}")

        # Weighted Budget Allocation
        if st.sidebar.button("Weighted Budget Allocation"):
            try:
                plot_weighted_budget_allocation()
                generate_inference(st.session_state.df_cleaned, "Weighted Budget Allocation")  # Inference
            except Exception as e:
                st.error(f"Error in Weighted Budget Allocation: {e}")

        # Dollar Value Sales Analysis
        if st.sidebar.button("Dollar Value Sales Analysis"):
            try:
                calculate_sales_from_strategy(st.session_state.df_cleaned)
                generate_inference(st.session_state.df_cleaned, "Dollar Value Sales Analysis")  # Inference
            except Exception as e:
                st.error(f"Error calculating dollar value sales: {e}")

        # Simulate Strategy Reallocation & Switching Costs
        if st.sidebar.button("Simulate Strategy Reallocation & Switching Costs"):
            try:
                if 'model' in st.session_state:
                    simulate_reallocation_and_switching_costs(st.session_state.df_cleaned, st.session_state.model)
                    generate_inference(st.session_state.df_cleaned, "Strategy Reallocation & Switching Costs")  # Inference
                else:
                    st.warning("Please run the regression analysis first to create a model.")
            except Exception as e:
                st.error(f"Error simulating reallocation and switching costs: {e}")

        # Average Marginal Impact
        if st.sidebar.button("Calculate Average Marginal Impact"):
            try:
                # Correct the call by passing only df_cleaned, no model required
                calculate_average_marginal_impact(st.session_state.df_cleaned)
                generate_inference(st.session_state.df_cleaned, "Average Marginal Impact")  # Inference
            except Exception as e:
                st.error(f"Error calculating Average Marginal Impact: {e}")

else:
    st.info("Please provide your Airtable credentials to load and clean data.")
