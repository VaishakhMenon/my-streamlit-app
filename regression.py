import pandas as pd
import streamlit as st
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score

def perform_regression(df):
    """
    Perform linear regression to estimate the impact of selected variables on sales.
    """
    # Ensure column names are in lowercase and stripped of spaces
    df = df.copy()
    df.columns = df.columns.str.strip().str.lower()

    # Convert numeric columns
    df = df.apply(pd.to_numeric, errors='coerce')

    # Identify numeric columns
    numeric_columns = df.select_dtypes(include=['float64', 'int64']).columns.tolist()

    if 'sales' not in numeric_columns:
        st.warning("Column 'sales' is required for regression analysis but is missing.")
        return

    if len(numeric_columns) <= 1:
        st.warning("At least two numeric columns (including 'sales') are required for regression.")
        return

    # Allow the user to select variables for regression
    st.write("### Select Variables for Regression")
    independent_vars = st.multiselect(
        "Select independent variables (features):",
        [col for col in numeric_columns if col != 'sales']
    )

    if not independent_vars:
        st.warning("Please select at least one independent variable for regression.")
        return

    # Prepare data for regression
    X = df[independent_vars].dropna()
    y = df.loc[X.index, 'sales']  # Align 'sales' with the selected rows

    # Split the dataset into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Create the regression model and fit it to the training data
    model = LinearRegression()
    model.fit(X_train, y_train)

    # Predict on the test set and evaluate performance
    y_pred = model.predict(X_test)
    mse = mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)

    # Display results
    st.subheader("Regression Analysis Results")
    st.write("### Model Coefficients:")
    coefficients = pd.DataFrame({
        'Feature': independent_vars,
        'Coefficient': model.coef_
    })
    st.table(coefficients)

    st.write(f"### Intercept: {model.intercept_:.2f}")
    st.write(f"### Mean Squared Error: {mse:.2f}")
    st.write(f"### R-squared: {r2:.2f}")

    # Plot actual vs. predicted values
    st.write("### Actual vs. Predicted Sales")
    comparison_df = pd.DataFrame({
        'Actual Sales': y_test,
        'Predicted Sales': y_pred
    })
    st.scatter_chart(comparison_df)
