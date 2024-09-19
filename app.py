import streamlit as st
import pandas as pd
from data_cleaning import clean_data
from eda import plot_correlation_matrix, plot_sales_by_account_type, plot_sales_trend
from regression import perform_regression
from time_series_analysis import analyze_time_series
from market_segmentation import perform_segmentation
from competitor_analysis import run_competitor_analysis  # Correct import here
from future_budget import forecast_budget
from dollar_value_sales import calculate_sales_from_strategy
from simulate_reallocation_and_switching_cost import (
    simulate_reallocation_and_switching_costs,  
    calculate_average_marginal_impact
)
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

if 'df_cleaned' not in st.session_state:
    st.session_state.df_cleaned = None

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
            st.write("Data Types of Cleaned DataFrame:")
            st.write(df_cleaned.dtypes)
            st.write("Cleaned Data:")
            st.dataframe(df_cleaned)
        except Exception as e:
            st.error(f"Error loading or cleaning data: {e}")

    if st.session_state.df_cleaned is not None:
        st.sidebar.header("Analysis")
        
        if st.sidebar.button("Competitor Analysis"):
            try:
                run_competitor_analysis(st.session_state.df_cleaned)  # Run competitor analysis
            except Exception as e:
                st.error(f"Error performing competitor analysis: {e}")
