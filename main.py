import pandas as pd
from data_cleaning import clean_data
from eda import plot_correlation_matrix, plot_sales_by_account_type, plot_sales_trend
from regression import perform_regression
from time_series_analysis import analyze_time_series
from market_segmentation import perform_segmentation
from competitor_analysis import analyze_competitors
from future_budget import future_budget_forecasting, plot_weighted_budget_allocation
from dollar_value_sales import calculate_sales_from_strategy
from simulate_reallocation_and_switching_cost import simulate_reallocation_and_switching_costs
from inference import generate_inference  # Import inference function
from pyairtable import Api

# Airtable credentials (replace with your actual credentials or load from a config file)
airtable_token = 'your_personal_access_token'  # Replace with your actual token
base_id = 'your_base_id'  # Replace with your actual base ID
table_name = 'Your Table Name'  # Replace with your actual table name

# Initialize the Airtable API and load data
try:
    api = Api(airtable_token)
    table = api.table(base_id, table_name)
    records = table.all()
    data = [record['fields'] for record in records]
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
        generate_inference(df_cleaned, "Correlation Matrix")  # Add inference

        plot_sales_by_account_type(df_cleaned)
        generate_inference(df_cleaned, "Sales by Account Type")  # Add inference

        plot_sales_trend(df_cleaned)
        generate_inference(df_cleaned, "Sales Trend")  # Add inference

        # Perform regression analysis
        print("Running regression analysis...")
        model = perform_regression(df_cleaned)  # Store the regression model for later use
        generate_inference(df_cleaned, "Regression Analysis")  # Add inference

        # Dollar Value of Sales
        print("Calculating Dollar Value of Sales...")
        calculate_sales_from_strategy(df_cleaned)
        generate_inference(df_cleaned, "Dollar Value of Sales")  # Add inference

        # Simulate reallocation, switching costs, and calculate AMI
        print("Simulating reallocation and switching costs...")
        simulate_reallocation_and_switching_costs(df_cleaned, model)
        generate_inference(df_cleaned, "Reallocation & Switching Costs")  # Add inference

        # Time series analysis
        #print("Starting time series analysis...")
        #analyze_time_series(df_cleaned)
        #generate_inference(df_cleaned, "Time Series Analysis")  # Add inference

        # Market segmentation
        print("Performing market segmentation...")
        perform_segmentation(df_cleaned)
        generate_inference(df_cleaned, "Market Segmentation")  # Add inference

        # Competitor impact analysis
        print("Analyzing competitor impact...")
        analyze_competitors(df_cleaned)
        generate_inference(df_cleaned, "Competitor Analysis")  # Add inference

        # Future budgeting and resource allocation
        print("Calculating future budgeting and resource allocation...")
        future_budget_forecasting()
        generate_inference(df_cleaned, "Future Budget Forecasting")  # Add inference

        plot_weighted_budget_allocation()
        generate_inference(df_cleaned, "Weighted Budget Allocation")  # Add inference

    except Exception as e:
        print(f"An error occurred during analysis: {e}")
else:
    print("No data to process. Exiting...")
