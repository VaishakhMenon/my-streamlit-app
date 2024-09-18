import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.tsa.seasonal import seasonal_decompose
from statsmodels.tsa.arima.model import ARIMA

def analyze_time_series(df):
    """
    Perform time series analysis by decomposing the sales data and forecasting future values.
    """
    st.header("Time Series Analysis")

    # Ensure that 'month' and 'sales' are in the correct format
    df['month'] = pd.to_datetime(df['month'], errors='coerce')
    df['sales'] = pd.to_numeric(df['sales'], errors='coerce')

    # Drop rows with missing or invalid data
    df = df.dropna(subset=['month', 'sales'])

    if df.empty:
        st.warning("No data available after processing. Please check your date and value columns.")
        return

    # Set 'month' as the index
    df.set_index('month', inplace=True)

    # Decompose the time series (additive model by default)
    st.subheader("Seasonal Decomposition")
    decomposition = seasonal_decompose(df['sales'], model='additive', period=12)
    fig = decomposition.plot()
    plt.tight_layout()
    st.pyplot(fig)

    # Perform ARIMA forecasting
    st.subheader("ARIMA Forecasting")
    model = ARIMA(df['sales'], order=(1, 1, 1))
    model_fit = model.fit()

    # Forecast for the next 12 months
    forecast = model_fit.forecast(steps=12)

    # Plot the forecast along with the historical data
    st.subheader("Sales Forecast for the Next 12 Months")
    plt.figure(figsize=(10, 6))
    plt.plot(df['sales'], label='Historical Sales')
    plt.plot(forecast, label='Forecasted Sales', color='red')
    plt.xlabel('Month')
    plt.ylabel('Sales')
    plt.title('Historical and Forecasted Sales')
    plt.legend()
    plt.xticks(rotation=45)
    plt.tight_layout()
    st.pyplot(plt)

    # Provide basic inference
    st.write(f"The ARIMA model predicts sales for the next 12 months. The forecasted values show an expected sales trend, based on historical data and seasonal patterns.")

