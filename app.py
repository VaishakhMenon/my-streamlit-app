import streamlit as st
import pandas as pd
from data_cleaning import clean_data
from eda import plot_correlation_matrix, plot_sales_by_account_type, plot_sales_trend

# Sidebar for Google Sheet ID input
st.sidebar.header("Google Sheets Input")
sheet_id = st.sidebar.text_input("Enter your Google Sheet ID:", "")

# Load data from Google Sheets
if sheet_id:
    st.sidebar.header("Data Processing")
    
    if st.sidebar.button("Load and Clean Data"):
        try:
            df_cleaned = clean_data(sheet_id)
            st.write("Data types:")
            st.write(df_cleaned.dtypes)
            
            # Analysis options
            st.sidebar.header("Analysis")
            if st.sidebar.button("Plot Correlation Matrix"):
                plot_correlation_matrix(df_cleaned)
                
            if st.sidebar.button("Plot Sales by Account Type"):
                plot_sales_by_account_type(df_cleaned)

            if st.sidebar.button("Plot Sales Trend"):
                plot_sales_trend(df_cleaned)

        except Exception as e:
            st.write(f"Error cleaning data or performing analysis: {e}")
else:
    st.write("Please enter a Google Sheet ID to load and clean data.")
