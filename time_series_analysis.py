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

    # Rescale sales if necessary
    max_sales = df['sales'].max()
    if max_sales > 1000000:
        df['sales'] = df['sales'] / 1000000
        sales_unit = " (in millions)"
    elif max_sales > 1000:
        df['sales'] = df['sales'] / 1000
        sales_unit = " (in thousands)"
    else:
        sales_unit = ""

    # Set 'month' as the index
    df.set_index('month', inplace=True)

    # Decompose the time series (additive model by default)
    st.subheader("Seasonal Decomposition")
    decomposition = seasonal_decompose(df['sales'], model='additive', period=12)
    fig = decomposition.plot()
    fig.suptitle(f'Seasonal Decomposition of Sales{sales_unit}', fontsize=16)
    plt.tight_layout()
    st.pyplot(fig)

    # Perform ARIMA forecasting
    st.subheader("ARIMA Forecasting")
    model = ARIMA(df['sales'], order=(1, 1, 1))
    model_fit = model.fit()

    # Forecast for the next 12 months
    forecast_steps = 12
    forecast = model_fit.forecast(steps=forecast_steps)

    # Generate future dates for the forecast, starting from the last date in the data
    last_date = df.index[-1]  # Get the last date in the dataset
    forecast_dates = pd.date_range(last_date, periods=forecast_steps + 1, freq='M')[1:]  # Generate future dates

    # Plot the forecast along with the historical data
    st.subheader("Sales Forecast for the Next 12 Months")
    plt.figure(figsize=(10, 6))
    pl
