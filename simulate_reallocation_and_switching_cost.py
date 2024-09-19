import pandas as pd
import altair as alt
import streamlit as st

def calculate_efficiency(df):
    """
    Calculate the efficiency of each strategy in terms of sales per unit spent.
    Efficiency = (Total Sales from Strategy) / (Total Spending on Strategy)
    """
    # Total spending for each strategy is the sum of the strategy values
    total_spending_strategy1 = df['strategy1'].sum()
    total_spending_strategy2 = df['strategy2'].sum()
    total_spending_strategy3 = df['strategy3'].sum()

    # Sales from each strategy is calculated as the contribution from each strategy directly
    total_sales_strategy1 = df['sales'] * (df['strategy1'] / (df['strategy1'] + df['strategy2'] + df['strategy3']))
    total_sales_strategy2 = df['sales'] * (df['strategy2'] / (df['strategy1'] + df['strategy2'] + df['strategy3']))
    total_sales_strategy3 = df['sales'] * (df['strategy3'] / (df['strategy1'] + df['strategy2'] + df['strategy3']))

    # Summing up the total sales for each strategy
    total_sales_strategy1 = total_sales_strategy1.sum()
    total_sales_strategy2 = total_sales_strategy2.sum()
    total_sales_strategy3 = total_sales_strategy3.sum()

    # Calculate efficiency: sales per dollar spent
    efficiency_strategy1 = total_sales_strategy1 / total_spending_strategy1
    efficiency_strategy2 = total_sales_strategy2 / total_spending_strategy2
    efficiency_strategy3 = total_sales_strategy3 / total_spending_strategy3

    # Display the results
    st.write(f"Efficiency of Strategy 1 (Sales per Dollar Spent): ${efficiency_strategy1:,.2f}")
    st.write(f"Efficiency of Strategy 2 (Sales per Dollar Spent): ${efficiency_strategy2:,.2f}")
    st.write(f"Efficiency of Strategy 3 (Sales per Dollar Spent): ${efficiency_strategy3:,.2f}")

    return efficiency_strategy1, efficiency_strategy2, efficiency_strategy3

def display_efficiency_table(df):
    """
    Display the calculated efficiency scores of each strategy in a table.
    """
    efficiency_strategy1, efficiency_strategy2, efficiency_strategy3 = calculate_efficiency(df)

    efficiency_data = {
        'Strategy': ['Strategy 1', 'Strategy 2', 'Strategy 3'],
        'Efficiency (Sales per Dollar Spent)': [
            efficiency_strategy1,
            efficiency_strategy2,
            efficiency_strategy3
        ]
    }

    efficiency_df = pd.DataFrame(efficiency_data)

    # Display the efficiency table
    st.subheader("Efficiency of Each Strategy")
    st.table(efficiency_df)

def simulate_strategy_reallocation(df):
    """
    Simulate reallocating resources from the least efficient strategy (Strategy 3) to the more efficient ones.
    """
    efficiency_strategy1, efficiency_strategy2, efficiency_strategy3 = calculate_efficiency(df)

    reallocation_percentage = 0.50  # 50% of strategy3's budget
    spending_reallocated = df['strategy3'].sum() * reallocation_percentage
    spending_to_strategy1 = spending_reallocated / 2
    spending_to_strategy2 = spending_reallocated / 2

    new_total_spending_strategy1 = df['strategy1'].sum() + spending_to_strategy1
    new_total_spending_strategy2 = df['strategy2'].sum() + spending_to_strategy2

    new_sales_strategy1 = new_total_spending_strategy1 * efficiency_strategy1
    new_sales_strategy2 = new_total_spending_strategy2 * efficiency_strategy2

    # Summing the new sales values to get the total
    new_total_sales = new_sales_strategy1 + new_sales_strategy2

    # Display the results
    st.write(f"New Total Sales after Reallocation: ${new_total_sales:,.2f}")

    reallocation_chart = pd.DataFrame({
        'Strategy': ['Strategy 1', 'Strategy 2', 'Total'],
        'Sales': [new_sales_strategy1, new_sales_strategy2, new_total_sales]
    })

    chart = alt.Chart(reallocation_chart).mark_bar().encode(
        x='Strategy',
        y='Sales',
        color='Strategy'
    ).properties(title="Sales After Reallocation")

    st.altair_chart(chart)

def simulate_switching_costs(df, efficiency_strategy1, efficiency_strategy2, efficiency_strategy3):
    """
    Simulate switching costs when reallocating resources between strategies.
    Adjust the impact of switching costs to reflect a more meaningful portion of the budget.
    """
    reallocation_percentage = 0.50  # Percentage of strategy3's budget to be reallocated
    switching_cost_percentage = 0.10  # 10% reduction due to switching costs

    # Calculate the total reallocated spending from strategy 3
    spending_reallocated = df['strategy3'].sum() * reallocation_percentage
    reallocated_to_strategy1 = spending_reallocated / 2
    reallocated_to_strategy2 = spending_reallocated / 2

    # Adjust efficiencies after applying the switching cost penalty
    adjusted_efficiency_strategy1 = efficiency_strategy1 * (1 - switching_cost_percentage)
    adjusted_efficiency_strategy2 = efficiency_strategy2 * (1 - switching_cost_percentage)

    # Calculate new sales for strategy 1 and strategy 2 after reallocating from strategy 3
    new_sales_strategy1_after_switching = adjusted_efficiency_strategy1 * reallocated_to_strategy1
    new_sales_strategy2_after_switching = adjusted_efficiency_strategy2 * reallocated_to_strategy2

    # Add back the existing total sales for strategy 1 and strategy 2
    total_sales_strategy1 = df['sales'] * (df['strategy1'] / (df['strategy1'] + df['strategy2'] + df['strategy3']))
    total_sales_strategy2 = df['sales'] * (df['strategy2'] / (df['strategy1'] + df['strategy2'] + df['strategy3']))

    total_sales_strategy1 = total_sales_strategy1.sum()
    total_sales_strategy2 = total_sales_strategy2.sum()

    # Recalculate total sales after switching costs
    new_total_sales_after_switching = (
        new_sales_strategy1_after_switching +
        new_sales_strategy2_after_switching +
        total_sales_strategy1 + total_sales_strategy2
    )

    # Display the results
    st.write(f"Efficiency of Strategy 1 (Sales per Dollar Spent): ${efficiency_strategy1:.2f}")
    st.write(f"Efficiency of Strategy 2 (Sales per Dollar Spent): ${efficiency_strategy2:.2f}")
    st.write(f"Efficiency of Strategy 3 (Sales per Dollar Spent): ${efficiency_strategy3:.2f}")
    st.write(f"New Total Sales after Switching Costs: ${new_total_sales_after_switching:,.2f}")

    # Plot the switching cost impact in a bar chart
    switching_cost_chart = pd.DataFrame({
        'Strategy': ['Strategy 1', 'Strategy 2', 'Total'],
        'Sales': [new_sales_strategy1_after_switching, new_sales_strategy2_after_switching, new_total_sales_after_switching]
    })

    chart = alt.Chart(switching_cost_chart).mark_bar().encode(
        x='Strategy',
        y='Sales',
        color='Strategy'
    ).properties(title="Sales After Switching Costs")

    st.altair_chart(chart)

def calculate_average_marginal_impact(df):
    """
    Calculate the Average Marginal Impact (AMI) for each strategy.
    This function will include the regression calculation directly.
    """
    st.header("Average Marginal Impact (AMI) Calculation")

    # Ensure 'sales' and strategy columns are numeric
    df['sales'] = pd.to_numeric(df['sales'], errors='coerce')
    df['strategy1'] = pd.to_numeric(df['strategy1'], errors='coerce')
    df['strategy2'] = pd.to_numeric(df['strategy2'], errors='coerce')
    df['strategy3'] = pd.to_numeric(df['strategy3'], errors='coerce')

    # Drop rows with missing values in these columns
    df = df.dropna(subset=['sales', 'strategy1', 'strategy2', 'strategy3'])

    # Run the regression
    X = df[['strategy1', 'strategy2', 'strategy3']]
    X = sm.add_constant(X)  # Adds a constant term for the regression
    y = df['sales']
    
    model = sm.OLS(y, X).fit()  # Fit the model

    # Extract coefficients from the regression model
    coeff_strategy1 = model.params['strategy1']
    coeff_strategy2 = model.params['strategy2']
    coeff_strategy3 = model.params['strategy3']

    # Calculate the average spending for each strategy
    average_spending_strategy1 = df['strategy1'].mean()
    average_spending_strategy2 = df['strategy2'].mean()
    average_spending_strategy3 = df['strategy3'].mean()

    # Calculate the Average Marginal Impact (AMI) for each strategy
    ami_strategy1 = coeff_strategy1 * average_spending_strategy1
    ami_strategy2 = coeff_strategy2 * average_spending_strategy2
    ami_strategy3 = coeff_strategy3 * average_spending_strategy3

    # Display the results
    st.write(f"**Average Marginal Impact of Strategy 1:** ${ami_strategy1:,.2f}")
    st.write(f"**Average Marginal Impact of Strategy 2:** ${ami_strategy2:,.2f}")
    st.write(f"**Average Marginal Impact of Strategy 3:** ${ami_strategy3:,.2f}")

    return ami_strategy1, ami_strategy2, ami_strategy3

def simulate_reallocation_and_switching_costs(df, model):
    st.header("Simulate Strategy Reallocation and Switching Costs")
    
    # Display Efficiency Table First
    display_efficiency_table(df)
    
    st.subheader("1. Strategy Reallocation")
    simulate_strategy_reallocation(df)
    
    st.subheader("2. Switching Costs Impact")
    efficiency_strategy1, efficiency_strategy2, efficiency_strategy3 = calculate_efficiency(df)
    simulate_switching_costs(df, efficiency_strategy1, efficiency_strategy2, efficiency_strategy3)

    st.subheader("3. Average Marginal Impact (AMI) of Each Strategy")
    calculate_average_marginal_impact(df, model)
