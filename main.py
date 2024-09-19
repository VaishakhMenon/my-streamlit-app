import pandas as pd
from data_cleaning import clean_data
from eda import plot_correlation_matrix, plot_sales_by_account_type, plot_sales_trend
from regression import perform_regression
from time_series_analysis import analyze_time_series
from market_segmentation import perform_segmentation
from competitor_analysis import analyze_competitors
from future_budget import forecast_budget
from dollar_value_sales import calculate_dollar_value_sales
from simulate_reallocation_and_switching_cost import simulate_reallocation_and_switching_costs

# Airtable credentials (replace with your actual credentials or load from a config file)
airtable_token = 'your_personal_access_token'  # Replace with your actual token
base_id = 'your_base_id'  # Replace with your actual base ID
table_name = 'Your Table Name'  # Replace with your actual table name

# Load and clean data from Airtable
try:
    # Load the data from Airtable (replace with your Airtable API calls)
    df = pd.DataFrame(data_from_airtable)

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

        # Dollar Value of Sales
        print("Calculating Dollar Value of Sales...")
        calculate_dollar_value_sales(df_cleaned)

        # Reallocation and switching costs
        print("Simulating Reallocation & Switching Costs...")
        simulate_reallocation_and_switching_costs(df_cleaned)

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

    except Exception as e:
        print(f"An error occurred during analysis: {e}")
else:
    print("No data to process. Exiting...")
