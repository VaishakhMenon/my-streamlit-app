import streamlit as st
from data_cleaning import clean_data, check_mixed_types
from eda import plot_correlation_matrix
from regression import perform_regression

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
        
        # Show the data types for further analysis
        st.write("Data Types of Cleaned DataFrame:")
        st.write(df_cleaned.dtypes)
        
        # Call the debugging function to check for mixed types in object columns
        st.write("Checking for mixed types in object columns...")
        check_mixed_types(df_cleaned)
        
        # Sidebar options after data is loaded and cleaned
        st.sidebar.header("Analysis")
        
        if st.sidebar.button("Plot Correlation Matrix"):
            st.subheader('Correlation Matrix')
            plot_correlation_matrix(df_cleaned)

        if st.sidebar.button("Run Regression"):
            model, X_test, y_test = perform_regression(df_cleaned)
            st.subheader("Regression Results")
            st.write(f"Model Coefficients: {model.coef_}")
            st.write(f"Intercept: {model.intercept_}")

else:
    st.write("Please enter a Google Sheet ID to load and clean data.")
