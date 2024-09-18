import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import streamlit as st

def load_data_from_google_sheets(sheet_id):
    # Load the dataset from Google Sheets
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

def check_mixed_types(df):
    """
    Check if there are columns with mixed types in the DataFrame and print the problematic rows.
    """
    mixed_columns = []
    for col in df.columns:
        if df[col].apply(lambda x: isinstance(x, str)).any() and df[col].apply(lambda x: pd.api.types.is_numeric_dtype(type(x))).any():
            mixed_columns.append(col)
            st.write(f"Column '{col}' contains mixed types.")
    
    return mixed_columns

def clean_data(sheet_id):
    """
    Clean the dataset by removing unnecessary rows and ensuring proper data types.
    """
    df = load_data_from_google_sheets(sheet_id)

    # Strip leading/trailing whitespace from column names and ensure lowercase
    df.columns = df.columns.str.strip().str.lower()

    # Skip irrelevant rows (containing timestamps/URLs)
    df = df[df['month'].notnull()]  # Adjust this based on your specific cleaning criteria

    # Convert 'month' column to datetime
    df['month'] = pd.to_datetime(df['month'], errors='coerce')

    # Drop rows where 'month' could not be parsed
    df = df.dropna(subset=['month'])

    # Check for mixed types in columns
    mixed_columns = check_mixed_types(df)
    
    # Downcast int64 columns to int32
    for col in df.select_dtypes(include='int64').columns:
        df[col] = pd.to_numeric(df[col], downcast='integer')

    # Convert object columns to strings if applicable
    for col in df.select_dtypes(include='object').columns:
        df[col] = df[col].astype('string')

    # Display types after cleaning
    st.write("Data Types of Cleaned DataFrame:")
    st.write(df.dtypes)

    return df
