import streamlit as st
import pandas as pd
import statsmodels.api as sm
from inference import generate_inference  # Import the inference function

def calculate_sales_from_strategy(df):
    """
    Calculate total and net sales from each strategy using dynamically calculated coefficients.
    """
    st.header("Dollar Value of Sales from Each Strategy")

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
    st.subheader("Total Sales from Each Strategy")
    st.write(f"Total Sales from Strategy 1: ${total_sales_strategy1:,.2f}")
    st.write(f"Total Sales from Strategy 2: ${total_sales_strategy2:,.2f}")
    st.write(f"Total Sales from Strategy 3: ${total_sales_strategy3:,.2f}")

    st.subheader("Net Sales from Each Strategy (After Spending)")
    st.write(f"Net Sales from Strategy 1: ${net_sales_strategy1:,.2f}")
    st.write(f"Net Sales from Strategy 2: ${net_sales_strategy2:,.2f}")
    st.write(f"Net Sales from Strategy 3: ${net_sales_strategy3:,.2f}")

    # Optionally, display the updated dataframe
    st.write("Updated Dataframe with Sales and Net Sales from Each Strategy:")
    st.dataframe(df)

    # Generate inference based on sales and net sales results
    sales_summary = {
        "Total Sales Strategy 1": total_sales_strategy1,
        "Total Sales Strategy 2": total_sales_strategy2,
        "Total Sales Strategy 3": total_sales_strategy3,
        "Net Sales Strategy 1": net_sales_strategy1,
        "Net Sales Strategy 2": net_sales_strategy2,
        "Net Sales Strategy 3": net_sales_strategy3
    }
    inference_result = generate_inference(sales_summary)
    st.write(f"Inference: {inference_result}")
