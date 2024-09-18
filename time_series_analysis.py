# time_series.py

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.tsa.seasonal import seasonal_decompose
from statsmodels.tsa.arima.model import ARIMA
import numpy as np

def analyze_time_series(df):
    """
    Perform time series analysis, including decomposition and forecasting.
    """
    st.header("Time Series Analysis")

    # Allow the user to select the date column and the value column
    date_columns = df.select_dtypes(include=['datetime', 'object']).columns.tolist()
    numeric_columns = df.select_dtypes(include=[np.number]).columns.tolist()

    if not date_columns:
        st.warning("No date columns available in the dataset.")
        return

    if not numeric_columns:
        st.warning("No numeric columns available in the dataset.")
        return

    date_column = st.selectbox("Select the date column:", date_columns)
    value_column = st.selectbox("Select the value column for time series analysis:", numeric_columns)

    # Convert the date column to datetime if not already
    df[date_column] = pd.to_datetime(df[date_column], errors='coerce')

    # Drop rows with missing dates or values
    df_ts = df[[date_column, value_column]].dropna()
    df_ts = df_ts.sort_values(by=date_column)
    df_ts.set_index(date_column, inplace=True)

    if df_ts.empty:
        st.warning("No data available after processing. Please check your date and value columns.")
        return

    # Display the time series plot
    st.write("### Time Series Plot")
    st.line_chart(df_ts[value_column])

    # Decomposition
    st.write("### Time Series Decomposition")
    decomposition_model = st.selectbox("Select decomposition model:", ["Additive", "Multiplicative"])
    frequency = st.number_input("Set the period for decomposition (e.g., 12 for yearly seasonality in monthly data):", min_value=1, value=12, step=1)

    try:
        decomposition = seasonal_decompose(df_ts[value_column], model=decomposition_model.lower(), period=frequency)
        fig, axes = plt.subplots(4, 1, figsize=(10, 8))
        decomposition.observed.plot(ax=axes[0], legend=False)
        axes[0].set_ylabel('Observed')
        decomposition.trend.plot(ax=axes[1], legend=False)
        axes[1].set_ylabel('Trend')
        decomposition.seasonal.plot(ax=axes[2], legend=False)
        axes[2].set_ylabel('Seasonal')
        decomposition.resid.plot(ax=axes[3], legend=False)
        axes[3].set_ylabel('Residual')
        plt.tight_layout()
        st.pyplot(fig)
    except Exception as e:
        st.error(f"Error in decomposition: {e}")
        return

    # Forecasting
    st.write("### Forecasting with ARIMA Model")
    p = st.number_input("AR term (p):", min_value=0, value=1, step=1)
    d = st.number_input("Differencing term (d):", min_value=0, value=1, step=1)
    q = st.number_input("MA term (q):", min_value=0, value=1, step=1)
    steps = st.number_input("Number of periods to forecast:", min_value=1, value=12, step=1)

    try:
        model = ARIMA(df_ts[value_column], order=(p, d, q))
        model_fit = model.fit()
        forecast = model_fit.forecast(steps=steps)
        forecast_index = pd.date_range(start=df_ts.index[-1], periods=steps+1, freq=pd.infer_freq(df_ts.index))[1:]

        # Plot forecast
        st.write("### Forecasted Values")
        fig2, ax2 = plt.subplots(figsize=(10, 6))
        ax2.plot(df_ts[value_column], label='Historical Data')
        ax2.plot(forecast_index, forecast, label='Forecasted Data', color='red')
        ax2.legend()
        ax2.set_xlabel('Date')
        ax2.set_ylabel(value_column)
        st.pyplot(fig2)
    except Exception as e:
        st.error(f"Error in forecasting: {e}")
        return

    # Display forecasted values
    forecast_df = pd.DataFrame({value_column: forecast}, index=forecast_index)
    st.write("### Forecasted Data")
    st.dataframe(forecast_df)
