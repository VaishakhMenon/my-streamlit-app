from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score

def perform_regression(df):
    """
    Perform linear regression to estimate the impact of marketing strategies on sales.
    """
    # Ensure that the relevant columns for regression are numeric
    X = df[['strategy1', 'strategy2', 'strategy3']].astype(float)
    y = df['sales'].astype(float)

    # Split the dataset into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Create the regression model and fit it to the training data
    model = LinearRegression()
    model.fit(X_train, y_train)

    # Predict on the test set and evaluate performance
    y_pred = model.predict(X_test)
    mse = mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)

    print(f"Model Coefficients: {model.coef_}")
    print(f"Intercept: {model.intercept_}")
    print(f"Mean Squared Error: {mse}")
    print(f"R-squared: {r2}")

    return model

# Example usage (for testing):
# model = perform_regression(cleaned_df)
