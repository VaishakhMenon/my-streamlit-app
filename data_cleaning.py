import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials

def load_data_from_google_sheets(sheet_id):
    """
    Load data from a Google Sheet using its Sheet ID via gspread.
    """
    # Define the scope and authorize the credentials
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name("credentials/digital-river-319418-9cdcda1df227.json", scope)
    
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
    # Define a condition to detect rows with timestamps or Google Drive URLs (based on your specific data pattern)
    # For example, skip rows where 'month' is blank or contains irrelevant strings like '9/16/2024'
    irrelevant_row_condition = (df['month'].str.contains(r'https://|drive.google|timestamp', na=False)) | (df['month'].isna())

    # Filter out irrelevant rows
    df_cleaned = df[~irrelevant_row_condition]

    return df_cleaned

def clean_data(sheet_id):
    """
    Clean the dataset by removing unnecessary rows (timestamps/URLs),
    and converting the 'month' field to datetime format.
    """
    # Load the dataset from Google Sheets
    df = load_data_from_google_sheets(sheet_id)

    # Strip leading/trailing whitespace from column names and ensure lowercase
    df.columns = df.columns.str.strip().str.lower()

    # Skip irrelevant rows (containing timestamps/URLs)
    df = skip_irrelevant_rows(df)

    # Print the cleaned raw data to check if irrelevant rows were removed
    print("Cleaned raw data from Google Sheets after skipping irrelevant rows:")
    print(df.head())

    # Replace any empty strings or whitespace in 'month' column with NaN
    df['month'] = df['month'].replace(r'^\s*$', None, regex=True)

    # Convert 'month' to datetime format
    df['month'] = pd.to_datetime(df['month'], errors='coerce')

    # Drop rows where 'month' could not be parsed to a valid datetime
    df = df.dropna(subset=['month'])

    return df

# Example usage
sheet_id = '1JCzLJ7TmCOXyj3zjbhhSCIWd-p59jyeWfir11kfQg_0'  # Replace with your actual Google Sheet ID
cleaned_df = clean_data(sheet_id)

# View the cleaned data
if cleaned_df is not None:
    print("Cleaned Data:")
    print(cleaned_df.head())
