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

def skip_irrelevant_rows(df):
    """
    Remove irrelevant rows like timestamps and URLs.
    """
    irrelevant_row_condition = df['Sl'].apply(lambda x: pd.to_numeric(x, errors='coerce')).isna()
    df_cleaned = df[~irrelevant_row_condition]
    return df_cleaned

def clean_data(sheet_id):
    """
    Clean the dataset by removing unnecessary rows, converting the 'month' field to datetime, 
    and handling mixed types.
    """
    df = load_data_from_google_sheets(sheet_id)
    
    df.columns = df.columns.str.strip().str.lower()

    df = skip_irrelevant_rows(df)

    # Convert columns to appropriate types
    df['month'] = pd.to_datetime(df['month'], errors='coerce')
    numeric_columns = ['sales', 'qty', 'strategy1', 'strategy2', 'strategy3', 'salesvisit1', 'salesvisit2', 'salesvisit3', 'salesvisit4', 'salesvisit5']
    df[numeric_columns] = df[numeric_columns].apply(pd.to_numeric, errors='coerce')

    df['accid'] = df['accid'].astype(str)
    
    df = df.dropna(subset=['month'])
    
    return df
