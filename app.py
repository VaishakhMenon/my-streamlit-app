import streamlit as st
from data_cleaning import clean_data
from eda import plot_correlation_matrix, plot_sales_by_account_type, plot_sales_trend
from pyairtable import Api
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

# Initialize session state for the data if not already set
if 'df_cleaned' not in st.session_state:
    st.session_state.df_cleaned = None

# Load data from Airtable
if airtable_token and base_id and table_name:
    st.sidebar.header("Data Processing")

    if st.sidebar.button("Load and Clean Data"):
        try:
            # Initialize the Api object
            api = Api(airtable_token)

            # Get the Table object
            table = api.table(base_id, table_name)

            # Fetch all records from the Airtable table
            records = table.all()

            # Extract the fields from the records
            data = [record['fields'] for record in records]

            # Convert the data into a DataFrame
            df = pd.DataFrame(data)

            # Clean the data using your existing function
            df_cleaned = clean_data(df)

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
    else:
        st.info("Please load and clean data before performing analysis.")
else:
    st.info("Please provide your Airtable credentials to load and clean data.")
