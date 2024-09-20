import streamlit as st
import pandas as pd
from data_cleaning import clean_data
from eda import plot_correlation_matrix, plot_sales_by_account_type, plot_sales_trend
from regression import perform_regression
from time_series_analysis import analyze_time_series
from market_segmentation import perform_segmentation
from competitor_analysis import run_competitor_analysis
from future_budget import future_budget_forecasting, plot_weighted_budget_allocation
from dollar_value_sales import calculate_sales_from_strategy
from simulate_reallocation_and_switching_cost import (
    simulate_reallocation_and_switching_costs,
    calculate_average_marginal_impact
)
from inference import generate_inference
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
                corr_matrix = plot_correlation_matrix(st.session_state.df_cleaned)
                inference = generate_inference(f"Correlation matrix values: {corr_matrix}", "Correlation Matrix")
                st.write(inference)
            except Exception as e:
                st.error(f"Error plotting correlation matrix: {e}")

        # Sales by Account Type
        if st.sidebar.button("Plot Sales by Account Type"):
            try:
                sales_summary = plot_sales_by_account_type(st.session_state.df_cleaned)
                inference = generate_inference(f"Sales summary by account type: {sales_summary}", "Sales by Account Type")
                st.write(inference)
            except Exception as e:
                st.error(f"Error plotting sales by account type: {e}")


        # Sales Trend
        if st.sidebar.button("Plot Sales Trend"):
            try:
                sales_trend = plot_sales_trend(st.session_state.df_cleaned)
                inference = generate_inference(f"Sales trend over time: {sales_trend}", "Sales Trend")
                st.write(inference)
            except Exception as e:
                st.error(f"Error plotting sales trend: {e}")


        # Regression Analysis
        if st.sidebar.button("Run Regression Analysis"):
            try:
                model_summary = perform_regression(st.session_state.df_cleaned)
                st.session_state.model = model_summary  # Store model in session state
                inference = generate_inference(f"Regression results: {model_summary}", "Regression Analysis")
                st.write(inference)
            except Exception as e:
                st.error(f"Error performing regression analysis: {e}")

        # Time Series Analysis
        if st.sidebar.button("Time Series Analysis"):
            try:
                time_series_summary = analyze_time_series(st.session_state.df_cleaned)
                inference = generate_inference(f"Time series analysis results: {time_series_summary}", "Time Series Analysis")
                st.write(inference)
            except Exception as e:
                st.error(f"Error performing time series analysis: {e}")

        # Market Segmentation
        if st.sidebar.button("Market Segmentation"):
            try:
                segmentation_summary = perform_segmentation(st.session_state.df_cleaned)
                inference = generate_inference(f"Market segmentation summary: {segmentation_summary}", "Market Segmentation")
                st.write(inference)
            except Exception as e:
                st.error(f"Error performing market segmentation: {e}")

        # Competitor Analysis
        if st.sidebar.button("Competitor Analysis"):
            try:
                competitor_summary = run_competitor_analysis(st.session_state.df_cleaned)
                inference = generate_inference(f"Competitor analysis results: {competitor_summary}", "Competitor Analysis")
                st.write(inference)
            except Exception as e:
                st.error(f"Error performing competitor analysis: {e}")

        if st.sidebar.button("Future Budget Forecasting"):
            try:
                budget_forecast = future_budget_forecasting()
                inference = generate_inference(f"Budget forecasting results: {budget_forecast}", "Future Budget Forecasting")
                st.write(inference)
            except Exception as e:
                st.error(f"Error in Future Budget Forecasting: {e}")


        # Weighted Budget Allocation
        if st.sidebar.button("Weighted Budget Allocation"):
            try:
                weighted_budget_summary = plot_weighted_budget_allocation()
                inference = generate_inference(f"Weighted budget allocation results: {weighted_budget_summary}", "Weighted Budget Allocation")
                st.write(inference)
            except Exception as e:
                st.error(f"Error in Weighted Budget Allocation: {e}")

        # Dollar Value Sales Analysis
        if st.sidebar.button("Dollar Value Sales Analysis"):
            try:
                dollar_sales_summary = calculate_sales_from_strategy(st.session_state.df_cleaned)
                inference = generate_inference(f"Dollar value sales analysis: {dollar_sales_summary}", "Dollar Value Sales Analysis")
                st.write(inference)
            except Exception as e:
                st.error(f"Error calculating dollar value sales: {e}")

        # Simulate Strategy Reallocation & Switching Costs
        if st.sidebar.button("Simulate Strategy Reallocation & Switching Costs"):
            try:
                if 'model' in st.session_state:
                    # Assuming the function `simulate_reallocation_and_switching_costs()` returns a summary or result
                    reallocation_summary = simulate_reallocation_and_switching_costs(st.session_state.df_cleaned, st.session_state.model)
            
                    # Generate inference for the reallocation and switching costs analysis
                    inference = generate_inference(f"Reallocation and switching cost results: {reallocation_summary}", "Strategy Reallocation & Switching Costs")
                    st.write(inference)
                else:
                    st.warning("Please run the regression analysis first to create a model.")
            except Exception as e:
                    st.error(f"Error simulating reallocation and switching costs: {e}")


        # Example for Average Marginal Impact calculation
        if st.sidebar.button("Calculate Average Marginal Impact"):
            try:
                ami_summary = calculate_average_marginal_impact(st.session_state.df_cleaned)
                inference = generate_inference(f"Average Marginal Impact results: {ami_summary}", "Average Marginal Impact")
                st.write(inference)
            except Exception as e:
                st.error(f"Error calculating Average Marginal Impact: {e}")


else:
    st.info("Please provide your Airtable credentials to load and clean data.")
