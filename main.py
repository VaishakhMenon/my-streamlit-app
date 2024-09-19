import pandas as pd
from data_cleaning import clean_data
from eda import plot_correlation_matrix, plot_sales_by_account_type, plot_sales_trend
from regression import perform_regression
from time_series import analyze_time_series
from segmentation import perform_segmentation
from competitor_analysis import analyze_competitors
from budgeting import forecast_budget
from dollar_value_sales import calculate_sales_from_strategy  # Import the new function
from pyairtable import Api
import matplotlib.pyplot as plt
import seaborn as sns

# Airtable credentials (replace with your actual credentials or load from a config file)
airtable_token = 'your_personal_access_token'  # Replace with your actual token
base_id = 'your_base_id'  # Replace with your actual base ID
table_name = 'Your Table Name'  # Replace with your actual table name

# Initialize the Airtable API
api = Api(airtable_token)

# Load and clean data from Airtable
try:
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
    print("Data successfully loaded and cleaned.")
except Exception as e:
    print(f"Error loading/cleaning data: {e}")
    df_cleaned = None

if df_cleaned is not None:
    try:
        # Perform EDA
        print("Starting Exploratory Data Analysis (EDA)...")
        plot_correlation_matrix(df_cleaned)
        plot_sales_by_account_type(df_cleaned)
        plot_sales_trend(df_cleaned)

        # Perform regression analysis
        print("Running regression analysis...")
        perform_regression(df_cleaned)

        # Time series analysis
        print("Starting time series analysis...")
        analyze_time_series(df_cleaned)

        # Market segmentation
        print("Performing market segmentation...")
        perform_segmentation(df_cleaned)

        # Competitor impact analysis
        print("Analyzing competitor impact...")
        analyze_competitors(df_cleaned)

        # Future budgeting and resource allocation
        print("Calculating future budgeting and resource allocation...")
        forecast_budget(df_cleaned)

        # Calculate sales from strategy and net sales
        print("Calculating sales and net sales from strategy...")
        calculate_sales_from_strategy(df_cleaned)

    except Exception as e:
        print(f"An error occurred during analysis: {e}")
else:
    print("No data to process. Exiting...")
