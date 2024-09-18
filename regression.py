# regression.py

import streamlit as st
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression, Ridge, Lasso
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
import matplotlib.pyplot as plt

def perform_regression(df):
    """
    Perform regression analysis to estimate the impact of selected features on the target variable.
    """
    st.header("Regression Analysis")

    # Allow the user to select features and target variable
    st.write("### Select Variables for Regression")
    all_columns = df.columns.tolist()
    numeric_columns = df.select_dtypes(include=[np.number]).columns.tolist()

    features = st.multiselect("Select feature columns (independent variables):", numeric_columns)
    target = st.selectbox("Select the target column (dependent variable):", numeric_columns)

    if features and target:
        if target in features:
            st.error("The target variable cannot be one of the features.")
            return

        # Prepare the data
        X = df[features]
        y = df[target]

        # Handle missing values
        data = pd.concat([X, y], axis=1).dropna()
        X = data[features]
        y = data[target]

        # Split the dataset into training and testing sets
        test_size = st.slider("Select the test set size (as a percentage):", 10, 50, 20)
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=test_size / 100, random_state=42
        )

        # Select regression model
        st.write("### Select Regression Model")
        regression_model = st.selectbox(
            "Choose a regression model:",
            ("Linear Regression", "Ridge Regression", "Lasso Regression")
        )

        # Model parameters
        if regression_model == "Ridge Regression" or regression_model == "Lasso Regression":
            alpha = st.number_input("Select regularization strength (alpha):", min_value=0.01, max_value=10.0, value=1.0, step=0.01)
        else:
            alpha = None

        # Create and train the model
        if regression_model == "Linear Regression":
            model = LinearRegression()
        elif regression_model == "Ridge Regression":
            model = Ridge(alpha=alpha)
        elif regression_model == "Lasso Regression":
            model = Lasso(alpha=alpha)
        else:
            st.error("Invalid regression model selected.")
            return

        model.fit(X_train, y_train)

        # Predict on the test set
        y_pred = model.predict(X_test)

        # Evaluate the model
        mse = mean_squared_error(y_test, y_pred)
        rmse = np.sqrt(mse)
        mae = mean_absolute_error(y_test, y_pred)
        r2 = r2_score(y_test, y_pred)

        # Display the results
        st.write("## Regression Results")
        st.write("### Model Coefficients:")
        coefficients = pd.DataFrame({
            'Feature': features,
            'Coefficient': model.coef_
        })
        st.table(coefficients)

        st.write(f"### Intercept: {model.intercept_:.4f}")
        st.write("### Model Performance Metrics:")
        st.write(f"- Mean Squared Error (MSE): {mse:.4f}")
        st.write(f"- Root Mean Squared Error (RMSE): {rmse:.4f}")
        st.write(f"- Mean Absolute Error (MAE): {mae:.4f}")
        st.write(f"- R-squared (R²): {r2:.4f}")

        # Plot Actual vs. Predicted values
        st.write("### Actual vs. Predicted Values")
        fig, ax = plt.subplots()
        ax.scatter(y_test, y_pred, alpha=0.7)
        ax.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'r--')
        ax.set_xlabel('Actual Values')
        ax.set_ylabel('Predicted Values')
        ax.set_title('Actual vs. Predicted Values')
        st.pyplot(fig)

        # Residual Plot
        st.write("### Residual Plot")
        residuals = y_test - y_pred
        fig2, ax2 = plt.subplots()
        ax2.scatter(y_pred, residuals, alpha=0.7)
        ax2.hlines(y=0, xmin=y_pred.min(), xmax=y_pred.max(), colors='r', linestyles='dashed')
        ax2.set_xlabel('Predicted Values')
        ax2.set_ylabel('Residuals')
        ax2.set_title('Residual Plot')
        st.pyplot(fig2)

        # Optionally, display the distribution of residuals
        st.write("### Residuals Distribution")
        fig3, ax3 = plt.subplots()
        ax3.hist(residuals, bins=20, alpha=0.7)
        ax3.set_xlabel('Residual')
        ax3.set_ylabel('Frequency')
        ax3.set_title('Histogram of Residuals')
        st.pyplot(fig3)

    else:
        st.warning("Please select at least one feature and a target variable to perform regression.")
