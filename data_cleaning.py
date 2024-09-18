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

    # Drop the first column if it's unnamed or problematic (e.g., '0', 'sl', etc.)
    if df.columns[0] == '' or df.columns[0] == '0':
        df = df.drop(df.columns[0], axis=1)

    # Convert all object-type columns to strings to avoid serialization issues
    df = df.astype(str)

    # Ensure 'month' column is datetime
    if 'month' in df.columns:
        df['month'] = pd.to_datetime(df['month'], errors='coerce')

    # Drop rows where 'month' could not be parsed to a valid datetime
    df = df.dropna(subset=['month'])

    # Convert relevant columns to numeric types while retaining 0 values
    numeric_columns = ['sales', 'strategy1', 'strategy2', 'strategy3', 'qty']
    
    for col in numeric_columns:
        df[col] = pd.to_numeric(df[col], errors='coerce')  # Convert to numeric, coerce errors to NaN

    # Handle any remaining NaN values in numeric columns
    df = df.dropna(subset=numeric_columns, how='all')

    # Call the diagnostic function here to check for any issues
    print_column_info(df, num_rows=5)  # Call this function to print info for all columns

    return df

def print_column_info(df, problematic_column=None, num_rows=5):
    """
    Prints column names, data types, and the first few values of specific columns to diagnose issues.

    Args:
    df: DataFrame containing the data.
    problematic_column: The name of the column to focus on. If None, prints info for all columns.
    num_rows: The number of rows to display for each column.
    """
    if problematic_column:
        if problematic_column in df.columns:
            print(f"\n--- Column '{problematic_column}' Info ---")
            print(f"Data Type: {df[problematic_column].dtype}")
            print(f"First {num_rows} values:\n", df[problematic_column].head(num_rows))
        else:
            print(f"Column '{problematic_column}' does not exist in the DataFrame.")
    else:
        print("\n--- DataFrame Columns ---")
        print(df.columns)
        print("\n--- Data Types ---")
        print(df.dtypes)
        print(f"\n--- First {num_rows} Rows ---")
        print(df.head(num_rows))

    # Check for any object types that might cause issues
    object_columns = df.select_dtypes(include=['object']).columns
    if len(object_columns) > 0:
        print("\n--- Object Type Columns ---")
        for col in object_columns:
            print(f"Column '{col}': First {num_rows} values")
            print(df[col].head(num_rows))
