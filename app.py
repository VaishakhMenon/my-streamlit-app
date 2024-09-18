import streamlit as st
import pandas as pd
from data_cleaning import clean_data
from eda import plot_correlation_matrix, plot_sales_by_account_type, plot_sales_trend
from regression import perform_regression

# Sidebar for Google Sheet ID input
st.sidebar.header("Google Sheets Input")
sheet_id = st.sidebar.text_input("Enter your Google Sheet ID:", "")

# Initialize a variable for the cleaned data
df_cleaned = None

# Load data from Google Sheets if a sheet_id is provided
if sheet_id:
    st.sidebar.header("Data Processing")

    if st.sidebar.button("Load and Clean Data"):
        # Attempt to clean data
        df_cleaned = clean_data(sheet_id)
        
        if df_cleaned is None or df_cleaned.empty:
            st.error("Failed to load or clean data. Please check the Google Sheet ID and ensure data is valid.")
        else:
            # Drop the first column if irrelevant (like an index column or unnamed column)
            df_cleaned = df_cleaned.iloc[:, 1:]

            # Drop any completely empty or irrelevant columns
            df_cleaned = df_cleaned.dropna(axis=1, how='all')  # Drop columns with all NaN values

            # Ensure the 'Sl' column is treated as a string
            if 'Sl' in df_cleaned.columns:
                df_cleaned['Sl'] = df_cleaned['Sl'].astype(str)

            # Convert all other object-type columns to strings to prevent serialization issues
            df_cleaned = df_cleaned.applymap(lambda x: str(x) if isinstance(x, (int, float, str)) else '')

            # Display cleaned data
            st.write("Cleaned Data (with explicit type conversion):")
            
            try:
                # Display the first few rows of the cleaned data
                st.write(df_cleaned.head())
                
                # Display data types of each column for debugging purposes
                st.write("Data types of cleaned DataFrame:")
                st.write(df_cleaned.dtypes)
                
            except Exception as e:
                st.error(f"Error processing data: {e}")

            # Sidebar options after data is successfully loaded and cleaned
            st.sidebar.header("Analysis")

            if st.sidebar.button("Plot Correlation Matrix"):
                st.subheader('Correlation Matrix')
                plot_correlation_matrix(df_cleaned)

            if st.sidebar.button("Plot Sales by Account Type"):
                st.subheader('Sales Distribution by Account Type')
                plot_sales_by_account_type(df_cleaned)

            if st.sidebar.button("Plot Sales Trend"):
                st.subheader('Monthly Sales Trend')
                plot_sales_trend(df_cleaned)

            if st.sidebar.button("Run Regression"):
                st.subheader('Regression Analysis')
                model, X_test, y_test = perform_regression(df_cleaned)
                st.write(f"Model Coefficients: {model.coef_}")
                st.write(f"Intercept: {model.intercept_}")
else:
    st.write("Please enter a Google Sheet ID to load and clean data.")
