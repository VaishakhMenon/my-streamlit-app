import pandas as pd
import altair as alt
import streamlit as st

def calculate_efficiency(df):
    """
    Calculate the efficiency of each strategy in terms of sales per unit spent.
    Efficiency = (Total Sales from Strategy) / (Total Spending on Strategy)
    """
    total_spending_strategy1 = df['strategy1'].sum()
    total_spending_strategy2 = df['strategy2'].sum()
    total_spending_strategy3 = df['strategy3'].sum()

    total_sales_strategy1 = df['sales'] * (df['strategy1'] / (df['strategy1'] + df['strategy2'] + df['strategy3']))
    total_sales_strategy2 = df['sales'] * (df['strategy2'] / (df['strategy1'] + df['strategy2'] + df['strategy3']))
    total_sales_strategy3 = df['sales'] * (df['strategy3'] / (df['strategy1'] + df['strategy2'] + df['strategy3']))

    total_sales_strategy1 = total_sales_strategy1.sum()
    total_sales_strategy2 = total_sales_strategy2.sum()
    total_sales_strategy3 = total_sales_strategy3.sum()

    efficiency_strategy1 = total_sales_strategy1 / total_spending_strategy1
    efficiency_strategy2 = total_sales_strategy2 / total_spending_strategy2
    efficiency_strategy3 = total_sales_strategy3 / total_spending_strategy3

    return efficiency_strategy1, efficiency_strategy2, efficiency_strategy3

def display_efficiency_table(df):
    """
    Display the calculated efficiency scores of each strategy in a table.
    """
    efficiency_strategy1, efficiency_strategy2, efficiency_strategy3 = calculate_efficiency(df)

    efficiency_data = {
        'Strategy': ['Strategy 1', 'Strategy 2', 'Strategy 3'],
        'Efficiency (Sales per Dollar Spent)': [
            float(efficiency_strategy1),  # Convert to float to ensure scalar value
            float(efficiency_strategy2),
            float(efficiency_strategy3)
        ]
    }

    efficiency_df = pd.DataFrame(efficiency_data)

    # Display the efficiency table
    st.subheader("Efficiency of Each Strategy")
    st.table(efficiency_df)

def simulate_strategy_reallocation(df):
    """
    Simulate reallocating resources from the least efficient strategy to the more efficient ones.
    """
    efficiency_strategy1, efficiency_strategy2, efficiency_strategy3 = calculate_efficiency(df)

    # Reallocation: Moving 50% of Strategy 3's spending
    reallocation_percentage = 0.50
    spending_reallocated = df['strategy3'].sum() * reallocation_percentage

    # Divide the reallocated budget equally between Strategies 1 and 2
    spending_to_strategy1 = spending_reallocated / 2
    spending_to_strategy2 = spending_reallocated / 2

    # New total spending for Strategies 1 and 2
    new_total_spending_strategy1 = df['strategy1'].sum() + spending_to_strategy1
    new_total_spending_strategy2 = df['strategy2'].sum() + spending_to_strategy2

    # Calculate new sales based on the reallocation and efficiency
    new_sales_strategy1 = new_total_spending_strategy1 * efficiency_strategy1
    new_sales_strategy2 = new_total_spending_strategy2 * efficiency_strategy2

    # Summing the new sales values to get the total
    new_total_sales = new_sales_strategy1 + new_sales_strategy2

    # Display the results
    st.write(f"New Total Sales after Reallocation: ${float(new_total_sales):,.2f}")  # Convert to float

    reallocation_chart = pd.DataFrame({
        'Strategy': ['Strategy 1', 'Strategy 2', 'Total'],
        'Sales': [float(new_sales_strategy1), float(new_sales_strategy2), float(new_total_sales)]  # Ensure scalar values
    })

    chart = alt.Chart(reallocation_chart).mark_bar().encode(
        x='Strategy',
        y='Sales',
        color='Strategy'
    ).properties(title="Sales After Reallocation")

    st.altair_chart(chart)

def simulate_switching_costs(df):
    """
    Simulate switching costs when reallocating resources between strategies.
    """
    # Calculate efficiency of Strategy 1 and Strategy 2
    efficiency_strategy1, efficiency_strategy2, _ = calculate_efficiency(df)

    # Reallocate 50% of Strategy 3's budget
    reallocation_percentage = 0.50
    switching_cost_percentage = 0.10

    # Total spending for Strategy 3 and reallocation amount
    spending_reallocated = df['strategy3'].sum() * reallocation_percentage
    reallocated_to_strategy1 = spending_reallocated / 2
    reallocated_to_strategy2 = spending_reallocated / 2

    # Adjust efficiencies with switching costs (only on reallocated portion)
    adjusted_efficiency_strategy1 = float(efficiency_strategy1) * (1 - switching_cost_percentage)
    adjusted_efficiency_strategy2 = float(efficiency_strategy2) * (1 - switching_cost_percentage)

    # Calculate new sales with adjusted efficiencies
    new_sales_strategy1 = reallocated_to_strategy1 * adjusted_efficiency_strategy1
    new_sales_strategy2 = reallocated_to_strategy2 * adjusted_efficiency_strategy2

    # Add original sales from Strategies 1 and 2
    original_sales_strategy1 = df['sales'] * (df['strategy1'] / (df['strategy1'] + df['strategy2'] + df['strategy3'])).sum()
    original_sales_strategy2 = df['sales'] * (df['strategy2'] / (df['strategy1'] + df['strategy2'] + df['strategy3'])).sum()

    # Calculate new total sales after switching costs
    new_total_sales_after_switching = float(new_sales_strategy1 + new_sales_strategy2 + original_sales_strategy1 + original_sales_strategy2)

    # Display new total sales after switching costs
    st.write(f"New Total Sales after Switching Costs: ${new_total_sales_after_switching:,.2f}")

    # Create a dataframe to visualize sales
    switching_cost_chart = pd.DataFrame({
        'Strategy': ['Strategy 1', 'Strategy 2', 'Total'],
        'Sales': [float(new_sales_strategy1), float(new_sales_strategy2), new_total_sales_after_switching]
    })

    # Plotting the chart using Altair
    chart = alt.Chart(switching_cost_chart).mark_bar().encode(
        x='Strategy',
        y='Sales',
        color='Strategy'
    ).properties(title="Sales After Switching Costs")

    st.altair_chart(chart)

def simulate_reallocation_and_switching_costs(df):
    st.header("Simulate Strategy Reallocation and Switching Costs")
    
    # Display Efficiency Table First
    display_efficiency_table(df)
    
    st.subheader("1. Strategy Reallocation")
    simulate_strategy_reallocation(df)
    
    st.subheader("2. Switching Costs Impact")
    simulate_switching_costs(df)
