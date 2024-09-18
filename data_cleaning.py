import pandas as pd
import numpy as np  # Importing NumPy for handling numeric data
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import streamlit as st

def load_data_from_google_sheets(sheet_id):
    """
    Load data from a Google Sheet using its Sheet ID via gspread.
    """
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
   
    google_creds = {
        "type": st.secrets["google_api"]["type"],
        "project_id": st.secrets["google_api"]["project_id"],
        "private_key_id": st.secrets["google_api"]["private_key_id"],
        "private_key": st.secrets["google_api"]["private_key"].replace('\\n', '\n'),  # Handle line breaks in the private key
        "client_email": st.secrets["google_api"]["client_email"],
        "client_id": st.secrets["google_api"]["client_id"],
        "auth_uri": st.secrets["google_api"]["auth_uri"],
        "token_uri": st.secrets["google_api"]["token_uri"],
        "auth_provider_x509_cert_url": st.secrets["google_api"]["auth_provider_x509_cert_url"],
        "client_x509_cert_url": st.secrets["google_api"]["client_x509_cert_url"]
    }

    creds = ServiceAccountCredentials.from_json_keyfile_dict(google_creds, scope)
    client = gspread.authorize(creds)

    # Open the Google Sheet by ID
    sheet = client.open_by_key(sheet_id).sheet1

    # Get all data from the Google Sheet and convert it into a DataFrame
    data = sheet.get_all_records()
    df = pd.DataFrame(data)

    return df

def clean_data(sheet_id):
    """
    Clean the dataset by removing unnecessary rows and ensuring proper data types,
    while retaining 0 values for numeric columns.
    """
    df = load_data_from_google_sheets(sheet_id)

    # Drop columns that might be problematic, such as unnamed columns or index columns
    if 'sl' in df.columns:
        df = df.drop(columns=['sl'])
    if '0' in df.columns:
        df = df.drop(columns=['0'])

    # Ensure all object-type columns are converted to strings to avoid serialization issues
    df = df.applymap(lambda x: str(x) if isinstance(x, (str, int, float)) else x)

    # Ensure 'month' column is datetime
    if 'month' in df.columns:
        df['month'] = pd.to_datetime(df['month'], errors='coerce')

    # Drop rows where 'month' could not be parsed to a valid datetime
    df = df.dropna(subset=['month'])

    # Convert other relevant columns to numeric types while retaining 0 values
    numeric_columns = ['sales', 'strategy1', 'strategy2', 'strategy3', 'qty']
    
    for col in numeric_columns:
        df[col] = pd.to_numeric(df[col], errors='coerce')  # Use NumPy to convert to numeric (coerce invalid values)

    # Handle any remaining NaN values in numeric columns (retain 0 but drop NaNs)
    df = df.dropna(subset=numeric_columns, how='all')  # Drop rows where all numeric columns are NaN

    return df

# Example usage:
# sheet_id = 'your_google_sheet_id'
# cleaned_df = clean_data(sheet_id)
