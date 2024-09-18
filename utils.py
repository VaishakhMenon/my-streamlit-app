# utils.py

import pandas as pd
import streamlit as st
from pyairtable import Api

# Load data from Airtable
def load_data_from_airtable(api_token, base_id, table_name):
    """
    Load data from an Airtable table using the provided credentials.

    Args:
    api_token: Airtable API token
    base_id: Airtable base ID
    table_name: Airtable table name

    Returns:
    DataFrame containing the loaded data
    """
    try:
        # Initialize Airtable API
        api = Api(api_token)

        # Get the table object
        table = api.table(base_id, table_name)

        # Fetch all records from the Airtable table
        records = table.all()

        # Extract fields and convert to DataFrame
        data = [record['fields'] for record in records]
        df = pd.DataFrame(data)

        return df
    except Exception as e:
        st.error(f"Error loading data from Airtable: {e}")
        return None

# Handle missing values
def handle_missing_values(df, strategy='mean'):
    """
    Handle missing values in the DataFrame.

    Args:
    df: DataFrame containing the data
    strategy: Strategy to handle missing values ('mean', 'median', 'drop')

    Returns:
    DataFrame with missing values handled
    """
    if strategy == 'mean':
        return df.fillna(df.mean(numeric_only=True))
    elif strategy == 'median':
        return df.fillna(df.median(numeric_only=True))
    elif strategy == 'drop':
        return df.dropna()
    else:
        return df  # No handling applied

# Clean and process data
def clean_and_process_data(df, missing_value_strategy='mean'):
    """
    Clean the loaded data by handling missing values and performing other data cleaning steps.

    Args:
    df: DataFrame to clean and process
    missing_value_strategy: Strategy to handle missing values ('mean', 'median', 'drop')

    Returns:
    Cleaned DataFrame
    """
    # Handle missing values
    df_cleaned = handle_missing_values(df, strategy=missing_value_strategy)

    # Additional cleaning steps can be added here as needed

    return df_cleaned

# Load and clean data from Airtable
def load_and_clean_data_from_airtable(api_token, base_id, table_name, missing_value_strategy='mean'):
    """
    Load data from Airtable and clean it by handling missing values.

    Args:
    api_token: Airtable API token
    base_id: Airtable base ID
    table_name: Airtable table name
    missing_value_strategy: Strategy to handle missing values ('mean', 'median', 'drop')

    Returns:
    Cleaned DataFrame
    """
    # Load data from Airtable
    df = load_data_from_airtable(api_token, base_id, table_name)
    
    # Clean and process the data
    if df is not None:
        df_cleaned = clean_and_process_data(df, missing_value_strategy)
        return df_cleaned
    else:
        return None
