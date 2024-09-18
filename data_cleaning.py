import pandas as pd
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
        "private_key": st.secrets["google_api"]["private_key"].replace('\\n', '\n'),
        "client_email": st.secrets["google_api"]["client_email"],
        "client_id": st.secrets["google_api"]["client_id"],
        "auth_uri": st.secrets["google_api"]["auth_uri"],
        "token_uri": st.secrets["google_api"]["token_uri"],
        "auth_provider_x509_cert_url": st.secrets["google_api"]["auth_provider_x509_cert_url"],
        "client_x509_cert_url": st.secrets["google_api"]["client_x509_cert_url"]
    }

    creds = ServiceAccountCredentials.from_json_keyfile_dict(google_creds, scope)
    client = gspread.authorize(creds)

    sheet = client.open_by_key(sheet_id).sheet1
    data = sheet.get_all_records()
    df = pd.DataFrame(data)
    
    return df

def clean_data(sheet_id):
    """
    Clean the dataset by removing unnecessary rows and ensuring proper data types,
    while retaining zero values for numeric columns.
    """
    df = load_data_from_google_sheets(sheet_id)

    # Strip leading/trailing whitespace from column names and ensure lowercase
    df.columns = df.columns.str.strip().str.lower()

    # Ensure 'month' column is datetime
    if 'month' in df.columns:
        df['month'] = pd.to_datetime(df['month'], errors='coerce')

    # Drop rows where 'month' could not be parsed to a valid datetime
    df = df.dropna(subset=['month'])

    # Identify object-type columns for further inspection
    object_columns = df.select_dtypes(include=['object']).columns
    
    # Convert columns to more appropriate types
    for col in object_columns:
        if df[col].str.isnumeric().all():  # Convert columns with numeric values
            df[col] = pd.to_numeric(df[col], errors='coerce')
        else:
            df[col] = df[col].astype(str)  # Keep categorical columns as strings

    # Convert relevant columns to numeric types, retaining zero values
    numeric_columns = ['sales', 'strategy1', 'strategy2', 'strategy3', 'qty', 
                       'salesvisit1', 'salesvisit2', 'salesvisit3', 'salesvisit4', 'salesvisit5']
    
    for col in numeric_columns:
        df[col] = pd.to_numeric(df[col], errors='coerce')  # Convert to numeric, retain 0s

    # Handle rows where all numeric values are NaN
    df = df.dropna(subset=numeric_columns, how='all')

    return df

# Helper function for debugging and checking problematic columns
def check_mixed_types(df):
    """
    Check object-type columns for mixed data types.
    """
    object_columns = df.select_dtypes(include=['object']).columns
    
    for col in object_columns:
        print(f"\nChecking column: {col}")
        unique_types = df[col].map(type).unique()
        print(f"Unique data types: {unique_types}")
        print(f"First few values: {df[col].head(5)}")

# Call this function in your app for debugging
