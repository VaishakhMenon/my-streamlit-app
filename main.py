import pandas as pd
from eda import plot_correlation_matrix
from regression import perform_regression
from data_cleaning import clean_data
# Import other analysis functions as needed
# from time_series_analysis import decompose_time_series, forecast_sales
# from market_segmentation import perform_market_segmentation
# from competitor_analysis import analyze_competitor_impact
# from future_budget import reallocate_budget
from pyairtable import Table

# Airtable credentials (you may choose to read these from environment variables or a config file)
airtable_token = 'your_personal_access_token'  # Replace with your actual token
base_id = 'your_base_id'  # Replace with your actual base ID
table_name = 'Your Table Name'  # Replace with your actual table name

# Initialize the Airtable Table
table = Table(airtable_token, base_id, table_name)

# Load and clean data from Airtable
try:
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
        print("Starting EDA...")
        plot_correlation_matrix(df_cleaned)

        # Perform regression
        print("Running regression analysis...")
        perform_regression(df_cleaned)

        # Time series analysis
        # print("Starting time series analysis...")
        # decompose_time_series(df_cleaned, 'sales')
        # forecast_sales(df_cleaned, 'sales')

        # Market segmentation
        # print("Performing market segmentation...")
        # perform_market_segmentation(df_cleaned)

        # Competitor impact analysis
        # print("Analyzing competitor impact...")
        # analyze_competitor_impact(df_cleaned)

        # Budget reallocation based on strategy efficiency
        # total_future_budget = 30_000_000  # Example future budget
        # print("Reallocating budget...")
        # new_budget_allocation = reallocate_budget(df_cleaned, total_future_budget)
        # print("New Budget Allocation:", new_budget_allocation)
    except Exception as e:
        print(f"An error occurred during analysis: {e}")
else:
    print("No data to process. Exiting...")
