import streamlit as st
import pandas as pd
from data_cleaning import clean_data
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
        try:
            df_cleaned = clean_data(sheet_id)
            st.write("Cleaned Data:")
            st.write(df_cleaned.head())
            
            # Sidebar options after data is loaded and cleaned
            st.sidebar.header("Analysis")

             try:
            from data_cleaning import clean_data
            except Exception as e:
            st.error(f"Error importing clean_data: {e}")

            
            if st.sidebar.button("Plot Correlation Matrix"):
                try:
                    st.subheader('Correlation Matrix')
                    plot_correlation_matrix(df_cleaned)
                except Exception as e:
                    st.write(f"Error plotting correlation matrix: {e}")
            
            if st.sidebar.button("Run Regression"):
                try:
                    model, X_test, y_test = perform_regression(df_cleaned)
                    st.subheader("Regression Results")
                    st.write(f"Model Coefficients: {model.coef_}")
                    st.write(f"Intercept: {model.intercept_}")
                except Exception as e:
                    st.write(f"Error running regression: {e}")
        except Exception as e:
            st.write(f"Error cleaning data: {e}")
           
else:
    st.write("Please enter a Google Sheet ID to load and clean data.")
