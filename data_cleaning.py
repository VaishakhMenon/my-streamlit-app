import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
import streamlit as st

def load_data_from_google_sheets(sheet_id):
    # Define the scope and authorize the credentials
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]

    # Access secrets stored in Streamlit
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

    # Open the Google Sheet by ID
    sheet = client.open_by_key(sheet_id).sheet1

    # Get all data from the Google Sheet and convert it into a DataFrame
    data = sheet.get_all_records()
    df = pd.DataFrame(data)

    return df


def clean_data(sheet_id):
    """
    Clean the dataset by removing unnecessary rows, handling null values,
    converting the 'month' column to datetime format, and ensuring proper data types.
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

    # Convert the first column to string explicitly
    if df.columns[0]:
        df[df.columns[0]] = df[df.columns[0]].astype(str)

    # Handle null values in the first column
    df[df.columns[0]] = df[df.columns[0]].fillna('')

    # Check if any object type columns need to be converted to string type
    for col in df.select_dtypes(include='object').columns:
        df[col] = df[col].astype(str)

    # Display types after cleaning
    st.write("Data Types of Cleaned DataFrame:")
    st.write(df.dtypes)

    # Try applying fixes before returning the DataFrame to Streamlit
    try:
        df = df.convert_dtypes()  # This will convert to the best possible types
        df = df.astype('string')  # Apply conversion to string where possible
    except Exception as e:
        st.write(f"Error in type conversion: {e}")

    return df
