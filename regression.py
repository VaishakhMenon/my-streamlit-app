import streamlit as st
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score

def perform_regression(df):
    """
    Perform linear regression to estimate the impact of marketing strategies on sales.
    """
    required_columns = ['strategy1', 'strategy2', 'strategy3', 'sales']
    missing_columns = [col for col in required_columns if col not in df.columns]

    if missing_columns:
        st.warning(f"Missing columns for regression analysis: {', '.join(missing_columns)}")
        return None

    # Ensure that the relevant columns for regression are numeric
    X = df[['strategy1', 'strategy2', 'strategy3']].astype(float)
    y = df['sales'].astype(float)

    # Handle potential NaN values after type conversion
    X = X.dropna()
    y = y.loc[X.index]  # Align y with X after dropping NaNs in X

    # Split the dataset into training and testing sets
    try:
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )
    except ValueError as e:
        st.error(f"Error splitting data: {e}")
        return None

    # Create the regression model and fit it to the training data
    model = LinearRegression()
    model.fit(X_train, y_train)

    # Predict on the test set and evaluate performance
    y_pred = model.predict(X_test)
    mse = mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)

    # Display the results using Streamlit
    st.subheader("Regression Analysis Results")
    st.write("### Model Coefficients:")
    coefficients = pd.DataFrame({
        'Feature': ['strategy1', 'strategy2', 'strategy3'],
        'Coefficient': model.coef_
    })
    st.table(coefficients)

    st.write(f"### Intercept: {model.intercept_:.2f}")
    st.write(f"### Mean Squared Error: {mse:.2f}")
    st.write(f"### R-squared: {r2:.2f}")

    # Optionally, display a scatter plot of actual vs. predicted values
    st.write("### Actual vs. Predicted Sales")
    comparison_df = pd.DataFrame({
        'Actual Sales': y_test,
        'Predicted Sales': y_pred
    })
    st.scatter_chart(comparison_df)

    return model
