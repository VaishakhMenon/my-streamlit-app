# budgeting.py

import streamlit as st
import pandas as pd

def forecast_budget(df):
    """
    Simulate future budget allocation based on the efficiency of marketing strategies.
    """
    st.header("Future Budgeting and Resource Allocation")

    # Check if required columns are present
    required_columns = ['sales', 'strategy1', 'strategy2', 'strategy3']
    missing_columns = [col for col in required_columns if col not in df.columns]
    if missing_columns:
        st.warning(f"The following required columns are missing from the data: {', '.join(missing_columns)}")
        return

    # Allow user to input total future budget
    total_future_budget = st.number_input(
        "Enter the total future budget for marketing strategies:",
        min_value=0.0,
        value=30000000.0,
        step=1000000.0,
        format="%.2f"
    )

    # Calculate efficiency of each strategy
    efficiency = calculate_efficiency(df)

    # Display the efficiency of each strategy
    st.write("### Strategy Efficiency (Sales per Dollar Spent)")
    efficiency_df = pd.DataFrame({
        'Strategy': ['Strategy 1', 'Strategy 2', 'Strategy 3'],
        'Efficiency': [
            efficiency['strategy1_efficiency'],
            efficiency['strategy2_efficiency'],
            efficiency['strategy3_efficiency']
        ]
    })
    st.table(efficiency_df)

    # Reallocate budget based on efficiency
    new_budget_allocation = reallocate_budget(df, total_future_budget)

    # Display new budget allocation
    st.write("### New Budget Allocation Based on Efficiency")
    allocation_df = pd.DataFrame({
        'Strategy': ['Strategy 1', 'Strategy 2', 'Strategy 3'],
        'New Budget Allocation': [
            new_budget_allocation['strategy1_efficiency'],
            new_budget_allocation['strategy2_efficiency'],
            new_budget_allocation['strategy3_efficiency']
        ]
    })
    st.table(allocation_df)

    # Optionally, display the proportion of total budget for each strategy
    total_allocated = sum(new_budget_allocation.values())
    allocation_df['Proportion (%)'] = (allocation_df['New Budget Allocation'] / total_allocated) * 100
    st.write("### Budget Allocation Proportions")
    st.table(allocation_df[['Strategy', 'Proportion (%)']])

def calculate_efficiency(df):
    """
    Calculate the efficiency of each strategy in terms of sales per dollar spent.

    Args:
    df: DataFrame containing the sales and strategy expenditure

    Returns:
    A dictionary of strategy efficiencies
    """
    # Avoid division by zero
    efficiencies = {}
    for i in range(1, 4):
        strategy_col = f'strategy{i}'
        if df[strategy_col].sum() == 0:
            efficiencies[f'strategy{i}_efficiency'] = 0
        else:
            efficiencies[f'strategy{i}_efficiency'] = df['sales'].sum() / df[strategy_col].sum()
    return efficiencies

def reallocate_budget(df, total_budget):
    """
    Simulate reallocation of resources based on strategy efficiency.

    Args:
    df: DataFrame containing the sales and strategy expenditure
    total_budget: Total future budget to be allocated

    Returns:
    New budget allocation across strategies
    """
    efficiency = calculate_efficiency(df)

    # Sort strategies by efficiency in descending order
    sorted_efficiency = sorted(efficiency.items(), key=lambda x: x[1], reverse=True)

    # Handle cases where all efficiencies are zero
    total_efficiency = sum([eff[1] for eff in sorted_efficiency])
    if total_efficiency == 0:
        # Allocate budget equally if efficiencies are zero
        num_strategies = len(sorted_efficiency)
        equal_allocation = total_budget / num_strategies
        budget_allocation = {strategy: equal_allocation for strategy, _ in sorted_efficiency}
    else:
        # Allocate budget proportionally based on efficiency
        budget_allocation = {}
        for strategy, eff in sorted_efficiency:
            proportion = eff / total_efficiency
            budget_allocation[strategy] = total_budget * proportion

    return budget_allocation
