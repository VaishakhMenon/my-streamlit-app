import streamlit as st
from data_cleaning import clean_data
from eda import plot_correlation_matrix, plot_sales_by_account_type, plot_sales_trend
from pyairtable import Table
import pandas as pd

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

# Load data from Airtable
if airtable_token and base_id and table_name:
    st.sidebar.header("Data Processing")

    if st.sidebar.button("Load and Clean Data"):
        try:
            # Initialize the Airtable Table
            table = Table(airtable_token, base_id, table_name)

            # Fetch all records from the Airtable table
            records = table.all()

            # Extract the fields from the records
            data = [record['fields'] for record in records]

            # Convert the data into a DataFrame
            df = pd.DataFrame(data)

            # Clean the data using the updated function
            df_cleaned = clean_data(df)

            st.write("Data types:")
            st.write(df_cleaned.dtypes)

            # Analysis options
            st.sidebar.header("Analysis")
            if st.sidebar.button("Plot Correlation Matrix"):
                plot_correlation_matrix(df_cleaned)

            if st.sidebar.button("Plot Sales by Account Type"):
                plot_sales_by_account_type(df_cleaned)

            if st.sidebar.button("Plot Sales Trend"):
                plot_sales_trend(df_cleaned)

        except Exception as e:
            st.error(f"Error cleaning data or performing analysis: {e}")
else:
    st.info("Please provide your Airtable credentials to load and clean data.")

# Analysis options
st.sidebar.header("Analysis")
if st.sidebar.button("Plot Correlation Matrix"):
    plot_correlation_matrix(df_cleaned)

if st.sidebar.button("Plot Sales by Account Type"):
    plot_sales_by_account_type(df_cleaned)

if st.sidebar.button("Plot Sales Trend"):
    plot_sales_trend(df_cleaned)

