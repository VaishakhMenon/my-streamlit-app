import streamlit as st
import pandas as pd
from data_cleaning import clean_data, check_mixed_types
from eda import plot_correlation_matrix
from regression import perform_regression
from utils import load_data_from_google_sheets

# Sidebar for Google Sheet ID input
st.sidebar.header("Google Sheets Input")
sheet_id = st.sidebar.text_input("Enter your Google Sheet ID:", "")

# Load data from Google Sheets
if sheet_id:
    st.sidebar.header("Data Processing")
    
    if st.sidebar.button("Load and Clean Data"):
        df_cleaned = clean_data(sheet_id)
        st.write("Cleaned Data:")
        st.write(df_cleaned.head())

        # Check for mixed data types in the cleaned data
        check_mixed_types(df_cleaned)

        # Sidebar options after data is loaded and cleaned
        st.sidebar.header("Analysis")
        
        # Plot correlation matrix
        if st.sidebar.button("Plot Correlation Matrix"):
           st.write("Correlation Matrix button clicked")  # Debugging button click
           st.subheader('Correlation Matrix')
           try:
                plot_correlation_matrix(df_cleaned)
                st.write("Correlation matrix plotted successfully!")
            except Exception as e:
                st.error(f"Error plotting correlation matrix: {str(e)}")
        
        # Run regression
        if st.sidebar.button("Run Regression"):
            st.subheader("Regression Results")
            st.write("Running regression...")
            try:
                model, X_test, y_test = perform_regression(df_cleaned)
                st.write(f"Model Coefficients: {model.coef_}")
                st.write(f"Intercept: {model.intercept_}")
                st.write("Regression run successfully!")
            except Exception as e:
                st.error(f"Error running regression: {str(e)}")
else:
    st.write("Please enter a Google Sheet ID to load and clean data.")
