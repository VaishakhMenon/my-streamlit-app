import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score

def perform_regression(df):
    """
    Perform regression analysis by displaying scatter plots for predefined relationships
    between features and sales, and provide inferences.
    """
    st.header("Scatter Plots with Inferences")

    # Ensure 'sales' and strategies are numeric, and coerce any invalid values
    df['sales'] = pd.to_numeric(df['sales'], errors='coerce')
    df['strategy1'] = pd.to_numeric(df['strategy1'], errors='coerce')
    df['strategy2'] = pd.to_numeric(df['strategy2'], errors='coerce')
    df['strategy3'] = pd.to_numeric(df['strategy3'], errors='coerce')

    # Drop rows with missing values in these columns
    df = df.dropna(subset=['sales', 'strategy1', 'strategy2', 'strategy3'])

    # Define predefined features to compare with sales
    features = ['strategy1', 'strategy2', 'strategy3']

    # Loop through each feature and create scatter plots with regression lines
    for feature in features:
        if feature in df.columns:
            st.subheader(f"Scatter Plot: {feature} vs. Sales")
            plt.figure(figsize=(8, 6))
            sns.regplot(x=feature, y='sales', data=df, ci=None, scatter_kws={'s': 10})
            plt.xlabel(f"{feature}")
            plt.ylabel("Sales")
            plt.title(f"Sales vs. {feature}")
            st.pyplot(plt)

            # Perform simple regression to show inference
            X = df[[feature]].dropna()
            y = df.loc[X.index, 'sales']

            if len(X) > 0 and len(y) > 0:
                model = LinearRegression()
                model.fit(X, y)
                y_pred = model.predict(X)

                mse = mean_squared_error(y, y_pred)
                r2 = r2_score(y, y_pred)

                st.write(f"**Inference for {feature}:**")
                st.write(f" - Mean Squared Error (MSE): {mse:.2f}")
                st.write(f" - R-squared (R²): {r2:.2f}")
                st.write(f" - Coefficient: {model.coef_[0]:.2f}")
                st.write(f" - Intercept: {model.intercept_:.2f}")
        else:
            st.warning(f"{feature} column not found in the data.")
