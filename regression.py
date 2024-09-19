import streamlit as st
import pandas as pd
import statsmodels.api as sm
import matplotlib.pyplot as plt
import seaborn as sns
import altair as alt

def segmented_strategy_analysis(segment_data, segment_name):
    """
    Perform regression analysis for each account type segment and generate plots for each strategy.
    """
    st.header(f"Regression Analysis for {segment_name}")

    # Independent variables (strategies)
    X = segment_data[['strategy1', 'strategy2', 'strategy3']]
    X = sm.add_constant(X)  # Adds a constant term for the regression
    # Dependent variable (sales)
    y = segment_data['sales']

    # Fit the model
    model = sm.OLS(y, X).fit()

    # Display the summary of the regression model
    st.subheader(f"Regression Summary for {segment_name}")
    st.text(model.summary())

    # Plot strategy1 vs. sales with regression line
    base = alt.Chart(segment_data).mark_point().encode(
        x='strategy1', y='sales', tooltip=['strategy1', 'sales']
    ).properties(
        title=f"{segment_name}: Strategy 1 Impact on Sales"
    )
    line = base.transform_regression('strategy1', 'sales').mark_line()
    plot1 = base + line
    st.altair_chart(plot1, use_container_width=True)

    # Plot strategy2 vs. sales with regression line
    base2 = alt.Chart(segment_data).mark_point().encode(
        x='strategy2', y='sales', tooltip=['strategy2', 'sales']
    ).properties(
        title=f"{segment_name}: Strategy 2 Impact on Sales"
    )
    line2 = base2.transform_regression('strategy2', 'sales').mark_line()
    plot2 = base2 + line2
    st.altair_chart(plot2, use_container_width=True)

    # Plot strategy3 vs. sales with regression line
    base3 = alt.Chart(segment_data).mark_point().encode(
        x='strategy3', y='sales', tooltip=['strategy3', 'sales']
    ).properties(
        title=f"{segment_name}: Strategy 3 Impact on Sales"
    )
    line3 = base3.transform_regression('strategy3', 'sales').mark_line()
    plot3 = base3 + line3
    st.altair_chart(plot3, use_container_width=True)

def perform_regression(df):
    """
    Perform regression analysis by account type and plot regression lines for each strategy.
    """
    st.header("Segmented Strategy Regression Analysis")

    # Ensure columns are in lowercase for consistency
    df.columns = df.columns.str.strip().str.lower()

    # Check if 'acctype' exists after cleaning
    if 'acctype' not in df.columns:
        st.error("The 'acctype' column is missing from the data after cleaning.")
        return

    # Ensure 'sales' and strategies are numeric
    df['sales'] = pd.to_numeric(df['sales'], errors='coerce')
    df['strategy1'] = pd.to_numeric(df['strategy1'], errors='coerce')
    df['strategy2'] = pd.to_numeric(df['strategy2'], errors='coerce')
    df['strategy3'] = pd.to_numeric(df['strategy3'], errors='coerce')

    # Drop rows with missing values in these columns
    df = df.dropna(subset=['sales', 'strategy1', 'strategy2', 'strategy3'])

    # Ensure 'acctype' has non-empty values
    if df['acctype'].isnull().all():
        st.warning("No valid 'acctype' data found after cleaning.")
        return

    # Segment the data by account type
    for segment_name in df['acctype'].unique():
        segment_data = df[df['acctype'] == segment_name]
        segmented_strategy_analysis(segment_data, segment_name)


 import statsmodels.api as sm

    # Define independent variables (strategies)
    X = df[['strategy1', 'strategy2', 'strategy3']]
    X = sm.add_constant(X)  # Adds a constant term for the regression

    # Dependent variable (sales)
    y = df['sales']

    # Fit the model
    model = sm.OLS(y, X).fit()

    # Return the model to be used in AMI calculations
    return model



