import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
import numpy as np

def future_budget_forecasting():
    """
    This function simulates two future budget allocation scenarios, compares expected sales and expenditures,
    and generates visualizations to compare both scenarios.
    """
    
    # Example spending and sales based on previous analysis
    spending_strategy1 = 9_916_652  # Example: $9,916,652
    spending_strategy2 = 56_924_812  # Example: $56,924,812
    spending_strategy3 = 1_648_700  # Example: $1,648,700

    total_sales_strategy1 = 749_703_582.20  # Total sales from Strategy 1
    total_sales_strategy2 = 3_676_109_835.12  # Total sales from Strategy 2
    total_sales_strategy3 = 52_375_297.77  # Total sales from Strategy 3

    # Set future budget allocations for Scenario 1
    future_budget_strategy1 = 10_000_000  # Future budget for Strategy 1
    future_budget_strategy2 = 15_000_000  # Future budget for Strategy 2
    future_budget_strategy3 = 5_000_000   # Future budget for Strategy 3

    # Calculate sales efficiency (sales per dollar spent)
    efficiency_strategy1 = total_sales_strategy1 / spending_strategy1
    efficiency_strategy2 = total_sales_strategy2 / spending_strategy2
    efficiency_strategy3 = total_sales_strategy3 / spending_strategy3

    # Scenario 1: All strategies included
    expected_sales_strategy1_with_3 = efficiency_strategy1 * future_budget_strategy1
    expected_sales_strategy2_with_3 = efficiency_strategy2 * future_budget_strategy2
    expected_sales_strategy3_with_3 = efficiency_strategy3 * future_budget_strategy3

    total_expenditure_with_strategy3 = future_budget_strategy1 + future_budget_strategy2 + future_budget_strategy3

    # Scenario 2: Strategy 3 excluded, with its budget reallocated to Strategies 1 and 2
    reallocated_budget_strategy1 = future_budget_strategy1 + future_budget_strategy3 / 2
    reallocated_budget_strategy2 = future_budget_strategy2 + future_budget_strategy3 / 2

    expected_sales_strategy1_without_3 = efficiency_strategy1 * reallocated_budget_strategy1
    expected_sales_strategy2_without_3 = efficiency_strategy2 * reallocated_budget_strategy2

    total_expenditure_without_strategy3 = reallocated_budget_strategy1 + reallocated_budget_strategy2

    # Plot the individual results for each strategy: Expected Sales and Expenditures for both scenarios
    strategies = ['Strategy 1', 'Strategy 2', 'Strategy 3']

    # Expected Sales for Scenario 1 (with Strategy 3)
    expected_sales_with_strategy3 = [expected_sales_strategy1_with_3,
                                     expected_sales_strategy2_with_3,
                                     expected_sales_strategy3_with_3]

    # Expected Sales for Scenario 2 (without Strategy 3)
    expected_sales_without_strategy3 = [expected_sales_strategy1_without_3,
                                        expected_sales_strategy2_without_3,
                                        0]  # No Strategy 3

    # Plot Expected Sales per Strategy
    plt.figure(figsize=(12, 6))
    plt.bar(strategies, expected_sales_with_strategy3, color='blue', label='With Strategy 3')
    plt.bar(strategies, expected_sales_without_strategy3, color='orange', alpha=0.7, label='Without Strategy 3')
    plt.title('Expected Sales by Strategy (With vs. Without Strategy 3)')
    plt.ylabel('Expected Sales (USD)')
    plt.legend()
    plt.grid(True)
    plt.show()

    # Expenditure for Scenario 1 (with Strategy 3)
    expenditure_with_strategy3 = [future_budget_strategy1, future_budget_strategy2, future_budget_strategy3]

    # Expenditure for Scenario 2 (without Strategy 3)
    expenditure_without_strategy3 = [reallocated_budget_strategy1, reallocated_budget_strategy2, 0]

    # Plot Expenditures per Strategy
    plt.figure(figsize=(12, 6))
    plt.bar(strategies, expenditure_with_strategy3, color='blue', label='With Strategy 3')
    plt.bar(strategies, expenditure_without_strategy3, color='orange', alpha=0.7, label='Without Strategy 3')
    plt.title('Expenditures by Strategy (With vs. Without Strategy 3)')
    plt.ylabel('Expenditures (USD)')
    plt.legend()
    plt.grid(True)
    plt.show()

    # Displaying the results
    st.write(f"Expected Sales with Strategy 3: ${sum(expected_sales_with_strategy3):,.2f}")
    st.write(f"Total Expenditure with Strategy 3: ${total_expenditure_with_strategy3:,.2f}")

    st.write(f"Expected Sales without Strategy 3: ${sum(expected_sales_without_strategy3):,.2f}")
    st.write(f"Total Expenditure without Strategy 3: ${total_expenditure_without_strategy3:,.2f}")

def plot_weighted_budget_allocation():
    """
    Simulates weighted budget allocation based on historical sales and efficiency for each strategy.
    """
    # Historical sales and efficiency values (example)
    total_sales_strategy1 = 749_703_582.20
    total_sales_strategy2 = 3_676_109_835.12
    total_sales_strategy3 = 52_375_297.77

    efficiency_strategy1 = 75.60
    efficiency_strategy2 = 64.58
    efficiency_strategy3 = 31.77

    total_future_budget = 40_000_000  # Total future budget to be allocated

    # Weighted budget allocation
    weight_strategy1 = (efficiency_strategy1 * total_sales_strategy1) / (efficiency_strategy1 + total_sales_strategy1)
    weight_strategy2 = (efficiency_strategy2 * total_sales_strategy2) / (efficiency_strategy2 + total_sales_strategy2)
    weight_strategy3 = (efficiency_strategy3 * total_sales_strategy3) / (efficiency_strategy3 + total_sales_strategy3)

    total_weight_sum = weight_strategy1 + weight_strategy2 + weight_strategy3

    recommended_budget_strategy1 = (weight_strategy1 / total_weight_sum) * total_future_budget
    recommended_budget_strategy2 = (weight_strategy2 / total_weight_sum) * total_future_budget
    recommended_budget_strategy3 = (weight_strategy3 / total_weight_sum) * total_future_budget

    # Expected sales based on new budget
    expected_sales_strategy1 = efficiency_strategy1 * recommended_budget_strategy1
    expected_sales_strategy2 = efficiency_strategy2 * recommended_budget_strategy2
    expected_sales_strategy3 = efficiency_strategy3 * recommended_budget_strategy3

    # Plot results
    strategies = ['Strategy 1', 'Strategy 2', 'Strategy 3']
    recommended_budgets = [recommended_budget_strategy1, recommended_budget_strategy2, recommended_budget_strategy3]
    expected_sales = [expected_sales_strategy1, expected_sales_strategy2, expected_sales_strategy3]

    # Plot Recommended Budget Allocation
    plt.figure(figsize=(12, 6))
    plt.bar(strategies, recommended_budgets, color='blue')
    plt.title('Recommended Budget Allocation by Strategy (Weighted)')
    plt.ylabel('Budget Allocation (USD)')
    plt.grid(True)
    plt.show()

    # Plot Expected Sales from Allocated Budget
    plt.figure(figsize=(12, 6))
    plt.bar(strategies, expected_sales, color='orange')
    plt.title('Expected Sales from Recommended Budget Allocation (Weighted)')
    plt.ylabel('Expected Sales (USD)')
    plt.grid(True)
    plt.show()

    # Display recommended budget and expected sales
    st.write(f"Recommended Budget for Strategy 1: ${recommended_budget_strategy1:,.2f}")
    st.write(f"Expected Sales for Strategy 1: ${expected_sales_strategy1:,.2f}")

    st.write(f"Recommended Budget for Strategy 2: ${recommended_budget_strategy2:,.2f}")
    st.write(f"Expected Sales for Strategy 2: ${expected_sales_strategy2:,.2f}")

    st.write(f"Recommended Budget for Strategy 3: ${recommended_budget_strategy3:,.2f}")
    st.write(f"Expected Sales for Strategy 3: ${expected_sales_strategy3:,.2f}")

    total_expected_sales = sum(expected_sales)
    st.write(f"Total Expected Sales from Allocated Budget: ${total_expected_sales:,.2f}")

