import pandas as pd
from data_cleaning import clean_data
from eda import plot_correlation_matrix, plot_sales_by_account_type, plot_sales_trend
from regression import perform_regression
from time_series_analysis import analyze_time_series
from market_segmentation import perform_segmentation
from competitor_analysis import analyze_competitors
from future_budget import forecast_budget
from simulate_reallocation_and_switching_cost import simulate_strategy_reallocation
from pyairtable import Api

airtable_token = 'your_personal_access_token'
base_id = 'your_base_id'
table_name = 'Your Table Name'

api = Api(airtable_token)

try:
    table = api.table(base_id, table_name)
    records = table.all()
    data = [record['fields'] for record in records]
    df = pd.DataFrame(data)
    df_cleaned = clean_data(df)
    print("Data loaded and cleaned.")
except Exception as e:
    print(f"Error loading/cleaning data: {e}")
    df_cleaned = None

if df_cleaned is not None:
    try:
        plot_correlation_matrix(df_cleaned)
        plot_sales_by_account_type(df_cleaned)
        plot_sales_trend(df_cleaned)
        perform_regression(df_cleaned)
        analyze_time_series(df_cleaned)
        perform_segmentation(df_cleaned)
        analyze_competitors(df_cleaned)
        forecast_budget(df_cleaned)
        simulate_strategy_reallocation(df_cleaned)
    except Exception as e:
        print(f"Error during analysis: {e}")
else:
    print("No data to process.")
