import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import streamlit as st

def load_data_from_google_sheets(sheet_id):
    """
    Load data from a Google Sheet using its Sheet ID via gspread.
    """
    # Define the scope and authorize the credentials
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
   
    # Access secrets stored in Streamlit
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

    # Authenticate and initialize the gspread client using credentials from Streamlit Secrets
    creds = ServiceAccountCredentials.from_json_keyfile_dict(google_creds, scope)
    client = gspread.authorize(creds)

    # Open the Google Sheet by ID
    sheet = client.open_by_key(sheet_id).sheet1

    # Get all data from the Google Sheet and convert it into a DataFrame
    data = sheet.get_all_records()
    df = pd.DataFrame(data)

    return df

def skip_irrelevant_rows(df):
    """
    Skip rows that contain irrelevant data such as timestamps or URLs and start processing from the first row of actual data.
    """
    irrelevant_row_condition = (df['month'].str.contains(r'https://|drive.google|timestamp', na=False)) | (df['month'].isna())
    df_cleaned = df[~irrelevant_row_condition]
    return df_cleaned

def clean_data(sheet_id):
    """
    Clean the dataset by removing unnecessary rows, and converting the 'month' field to datetime format.
    """
    df = load_data_from_google_sheets(sheet_id)

    # Strip leading/trailing whitespace from column names and ensure lowercase
    df.columns = df.columns.str.strip().str.lower()

    # Skip irrelevant rows (containing timestamps/URLs)
    df = skip_irrelevant_rows(df)

    # Drop 'Sl' and other problematic columns if they exist
    if 'sl' in df.columns:
        df = df.drop(columns=['sl'])

    if '0' in df.columns:
        df = df.drop(columns=['0'])

    # Replace any empty strings or whitespace in 'month' column with NaN
    df['month'] = df['month'].replace(r'^\s*$', None, regex=True)

    # Convert 'month' to datetime format
    df['month'] = pd.to_datetime(df['month'], errors='coerce')

    # Drop rows where 'month' could not be parsed to a valid datetime
    df = df.dropna(subset=['month'])

    # Convert all object-type columns to strings
    df = df.astype(str)

    return df

# Example usage (for testing):
# sheet_id = 'your_google_sheet_id'
# cleaned_df = clean_data(sheet_id)
# print(cleaned_df.head())
