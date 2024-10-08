import streamlit as st
import pandas as pd
import statsmodels.api as sm
from inference import generate_inference  # Import the inference function

def calculate_sales_from_strategy(df):
    """
    Calculate total and net sales from each strategy using dynamically calculated coefficients.
    """
    st.header("Dollar Value of Sales from Each Strategy (in SGD)")

    # Ensure columns are in lowercase
    df.columns = df.columns.str.strip().str.lower()

    # Check if required columns are present
    required_columns = ['strategy1', 'strategy2', 'strategy3', 'sales']
    missing_columns = [col for col in required_columns if col not in df.columns]
    
    if missing_columns:
        st.error(f"Missing columns for analysis: {', '.join(missing_columns)}")
        return

    # Ensure required columns are numeric
    df['strategy1'] = pd.to_numeric(df['strategy1'], errors='coerce')
    df['strategy2'] = pd.to_numeric(df['strategy2'], errors='coerce')
    df['strategy3'] = pd.to_numeric(df['strategy3'], errors='coerce')
    df['sales'] = pd.to_numeric(df['sales'], errors='coerce')

    # Drop rows with missing values in these columns
    df = df.dropna(subset=['sales', 'strategy1', 'strategy2', 'strategy3'])

    # Add dummy spending data if spending columns do not exist
    if 'spending_strategy1' not in df.columns:
        df['spending_strategy1'] = 0.10 * df['strategy1']  # 10% of strategy value
    if 'spending_strategy2' not in df.columns:
        df['spending_strategy2'] = 0.12 * df['strategy2']  # 12% of strategy value
    if 'spending_strategy3' not in df.columns:
        df['spending_strategy3'] = 0.08 * df['strategy3']  # 8% of strategy value

    # Define independent variables (strategies) and dependent variable (sales)
    X = df[['strategy1', 'strategy2', 'strategy3']]
    X = sm.add_constant(X)  # Adds a constant term for the regression
    y = df['sales']

    # Fit the regression model
    model = sm.OLS(y, X).fit()

    # Extract the coefficients from the model parameters dynamically
    coeff_strategy1 = model.params['strategy1']
    coeff_strategy2 = model.params['strategy2']
    coeff_strategy3 = model.params['strategy3']

    # Calculate the dollar value of sales for each strategy
    df['sales_from_strategy1'] = coeff_strategy1 * df['strategy1']
    df['sales_from_strategy2'] = coeff_strategy2 * df['strategy2']
    df['sales_from_strategy3'] = coeff_strategy3 * df['strategy3']

    # Calculate net sales after subtracting spending
    df['net_sales_from_strategy1'] = df['sales_from_strategy1'] - df['spending_strategy1']
    df['net_sales_from_strategy2'] = df['sales_from_strategy2'] - df['spending_strategy2']
    df['net_sales_from_strategy3'] = df['sales_from_strategy3'] - df['spending_strategy3']

    # Summing up the dollar value of sales and net sales for each strategy
    total_sales_strategy1 = df['sales_from_strategy1'].sum()
    total_sales_strategy2 = df['sales_from_strategy2'].sum()
    total_sales_strategy3 = df['sales_from_strategy3'].sum()

    net_sales_strategy1 = df['net_sales_from_strategy1'].sum()
    net_sales_strategy2 = df['net_sales_from_strategy2'].sum()
    net_sales_strategy3 = df['net_sales_from_strategy3'].sum()

    # Display the results in Streamlit
    st.subheader("Total Sales from Each Strategy (SGD)")
    st.write(f"Total Sales from Strategy 1: SGD {total_sales_strategy1:,.2f}")
    st.write(f"Total Sales from Strategy 2: SGD {total_sales_strategy2:,.2f}")
    st.write(f"Total Sales from Strategy 3: SGD {total_sales_strategy3:,.2f}")

    st.subheader("Net Sales from Each Strategy (After Spending, in SGD)")
    st.write(f"Net Sales from Strategy 1: SGD {net_sales_strategy1:,.2f}")
    st.write(f"Net Sales from Strategy 2: SGD {net_sales_strategy2:,.2f}")
    st.write(f"Net Sales from Strategy 3: SGD {net_sales_strategy3:,.2f}")

    # Optionally, display the updated dataframe
    st.write("Updated Dataframe with Sales and Net Sales from Each Strategy:")
    st.dataframe(df)

    # Format the sales summary as strings to avoid garbling
    sales_summary = {
        "Total Sales Strategy 1": f"SGD {total_sales_strategy1:,.2f}",
        "Total Sales Strategy 2": f"SGD {total_sales_strategy2:,.2f}",
        "Total Sales Strategy 3": f"SGD {total_sales_strategy3:,.2f}",
        "Net Sales Strategy 1": f"SGD {net_sales_strategy1:,.2f}",
        "Net Sales Strategy 2": f"SGD {net_sales_strategy2:,.2f}",
        "Net Sales Strategy 3": f"SGD {net_sales_strategy3:,.2f}"
    }

    # Better prompt to guide the AI with actionable recommendations
    prompt = f"""
    The business is analyzing three strategies with the following sales performance in SGD:

    Total Sales:
    - Strategy 1: {sales_summary["Total Sales Strategy 1"]}
    - Strategy 2: {sales_summary["Total Sales Strategy 2"]}
    - Strategy 3: {sales_summary["Total Sales Strategy 3"]}

    Net Sales after spending:
    - Strategy 1: {sales_summary["Net Sales Strategy 1"]}
    - Strategy 2: {sales_summary["Net Sales Strategy 2"]}
    - Strategy 3: {sales_summary["Net Sales Strategy 3"]}

    Please provide:
    1. The best performing strategy in terms of sales and net profit.
    2. Specific recommendations to improve the performance of underperforming strategies.
    3. Potential risks associated with these strategies and suggestions to mitigate them.
    4. Any other actionable insights to optimize overall sales performance.
    """


    # Call the generate_inference function with the formatted sales summary
    inference_result = generate_inference(sales_summary, "Dollar Value Sales Analysis")
    st.write(f"Inference: {inference_result}")
