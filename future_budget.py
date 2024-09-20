import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
import numpy as np
from inference import generate_inference  # Import the inference function

def future_budget_forecasting():
    """
    Simulate two future budget allocation scenarios, compare expected sales and expenditures,
    and generate visualizations to compare both scenarios using line graphs in SGD.
    """

    # Example spending and sales based on previous analysis (in SGD)
    spending_strategy1 = 9_916_652  # SGD
    spending_strategy2 = 56_924_812  # SGD
    spending_strategy3 = 1_648_700  # SGD

    total_sales_strategy1 = 712_806_328.76  # Total sales from Strategy 1 (SGD)
    total_sales_strategy2 = 3_667_628_376.09  # Total sales from Strategy 2 (SGD)
    total_sales_strategy3 = 50_496_439.04  # Total sales from Strategy 3 (SGD)

    # Future budget allocations for Scenario 1 (in SGD)
    future_budget_strategy1 = 10_000_000  # Future budget for Strategy 1 (SGD)
    future_budget_strategy2 = 15_000_000  # Future budget for Strategy 2 (SGD)
    future_budget_strategy3 = 5_000_000   # Future budget for Strategy 3 (SGD)

    # Calculate sales efficiency (sales per dollar spent) for each strategy
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

    # Create data for line graphs
    strategies = ['Strategy 1', 'Strategy 2', 'Strategy 3']

    # Expected Sales for Scenario 1 (with Strategy 3)
    expected_sales_with_strategy3 = [expected_sales_strategy1_with_3,
                                     expected_sales_strategy2_with_3,
                                     expected_sales_strategy3_with_3]

    # Expected Sales for Scenario 2 (without Strategy 3)
    expected_sales_without_strategy3 = [expected_sales_strategy1_without_3,
                                        expected_sales_strategy2_without_3,
                                        0]  # No Strategy 3

    # Line graph: Expected Sales per Strategy
    plt.figure(figsize=(12, 6))
    plt.plot(strategies, expected_sales_with_strategy3, marker='o', label='With Strategy 3', color='blue')
    plt.plot(strategies, expected_sales_without_strategy3, marker='x', label='Without Strategy 3', color='orange')
    plt.title('Expected Sales by Strategy (With vs. Without Strategy 3) [SGD]')
    plt.ylabel('Expected Sales (SGD)')
    plt.legend()
    plt.grid(True)
    plt.show()

    # Expenditure for Scenario 1 (with Strategy 3)
    expenditure_with_strategy3 = [future_budget_strategy1, future_budget_strategy2, future_budget_strategy3]

    # Expenditure for Scenario 2 (without Strategy 3)
    expenditure_without_strategy3 = [reallocated_budget_strategy1, reallocated_budget_strategy2, 0]

    # Line graph: Expenditures per Strategy
    plt.figure(figsize=(12, 6))
    plt.plot(strategies, expenditure_with_strategy3, marker='o', label='With Strategy 3', color='blue')
    plt.plot(strategies, expenditure_without_strategy3, marker='x', label='Without Strategy 3', color='orange')
    plt.title('Expenditures by Strategy (With vs. Without Strategy 3) [SGD]')
    plt.ylabel('Expenditures (SGD)')
    plt.legend()
    plt.grid(True)
    plt.show()

    # Displaying the results in a table using Streamlit
    sales_data = {
        'Strategy': strategies,
        'Sales with Strategy 3 (SGD)': [f"${x:,.2f}" for x in expected_sales_with_strategy3],
        'Sales without Strategy 3 (SGD)': [f"${x:,.2f}" for x in expected_sales_without_strategy3],
    }
    expenditure_data = {
        'Strategy': strategies,
        'Expenditure with Strategy 3 (SGD)': [f"${x:,.2f}" for x in expenditure_with_strategy3],
        'Expenditure without Strategy 3 (SGD)': [f"${x:,.2f}" for x in expenditure_without_strategy3],
    }

    st.subheader("Expected Sales Comparison (SGD)")
    st.table(pd.DataFrame(sales_data))

    st.subheader("Expenditure Comparison (SGD)")
    st.table(pd.DataFrame(expenditure_data))

    # Displaying total sales and expenditures
    st.write(f"**Total Expected Sales with Strategy 3: ${sum(expected_sales_with_strategy3):,.2f} SGD**")
    st.write(f"**Total Expenditure with Strategy 3: ${total_expenditure_with_strategy3:,.2f} SGD**")
    st.write(f"**Total Expected Sales without Strategy 3: ${sum(expected_sales_without_strategy3):,.2f} SGD**")
    st.write(f"**Total Expenditure without Strategy 3: ${total_expenditure_without_strategy3:,.2f} SGD**")

    # Generate inference using the sales and expenditure data
    forecast_summary = {
        "Expected Sales with Strategy 3": sum(expected_sales_with_strategy3),
        "Expected Sales without Strategy 3": sum(expected_sales_without_strategy3),
        "Total Expenditure with Strategy 3": total_expenditure_with_strategy3,
        "Total Expenditure without Strategy 3": total_expenditure_without_strategy3
    }
    inference_result = generate_inference(forecast_summary)
    st.write(f"Inference: {inference_result}")

def plot_weighted_budget_allocation():
    """
    Calculate weighted budget allocation and expected sales for each strategy and display results.
    """

    # Example spending and sales based on previous analysis (in SGD)
    total_sales_strategy1 = 712_806_328.76  # Example value
    total_sales_strategy2 = 3_667_628_376.09  # Example value
    total_sales_strategy3 = 50_496_439.04  # Example value

    efficiency_strategy1 = 17.14  # Example efficiency values
    efficiency_strategy2 = 13.41
    efficiency_strategy3 = 8.23

    # Total future budget to allocate (SGD)
    total_future_budget = 40_000_000  # SGD

    # Weighting based on both efficiency and historical sales
    total_sales_sum = total_sales_strategy1 + total_sales_strategy2 + total_sales_strategy3
    weight_strategy1 = (efficiency_strategy1 * total_sales_strategy1) / (efficiency_strategy1 + total_sales_strategy1)
    weight_strategy2 = (efficiency_strategy2 * total_sales_strategy2) / (efficiency_strategy2 + total_sales_strategy2)
    weight_strategy3 = (efficiency_strategy3 * total_sales_strategy3) / (efficiency_strategy3 + total_sales_strategy3)
    total_weight_sum = weight_strategy1 + weight_strategy2 + weight_strategy3

    # Allocate budget proportionally based on the weighted contributions
    recommended_budget_strategy1 = (weight_strategy1 / total_weight_sum) * total_future_budget
    recommended_budget_strategy2 = (weight_strategy2 / total_weight_sum) * total_future_budget
    recommended_budget_strategy3 = (weight_strategy3 / total_weight_sum) * total_future_budget

    # Calculate expected sales based on the new budget allocation
    expected_sales_strategy1 = efficiency_strategy1 * recommended_budget_strategy1
    expected_sales_strategy2 = efficiency_strategy2 * recommended_budget_strategy2
    expected_sales_strategy3 = efficiency_strategy3 * recommended_budget_strategy3

    # Plot the recommended budget allocation for each strategy
    strategies = ['Strategy 1', 'Strategy 2', 'Strategy 3']
    recommended_budgets = [recommended_budget_strategy1, recommended_budget_strategy2, recommended_budget_strategy3]
    expected_sales = [expected_sales_strategy1, expected_sales_strategy2, expected_sales_strategy3]

    # Line graph: Weighted Budget Allocation
    plt.figure(figsize=(12, 6))
    plt.plot(strategies, recommended_budgets, marker='o', color='green', label='Weighted Budget')
    plt.title('Weighted Budget Allocation by Strategy [SGD]')
    plt.ylabel('Budget Allocation (SGD)')
    plt.grid(True)
    plt.show()

    # Line graph: Expected Sales from Weighted Budget
    plt.figure(figsize=(12, 6))
    plt.plot(strategies, expected_sales, marker='x', color='purple', label='Expected Sales from Weighted Budget')
    plt.title('Expected Sales from Weighted Budget Allocation [SGD]')
    plt.ylabel('Expected Sales (SGD)')
    plt.grid(True)
    plt.show()

    # Display results in Streamlit
    st.subheader("Weighted Budget Allocation and Expected Sales (SGD)")
    st.write(f"**Recommended Budget for Strategy 1: ${recommended_budget_strategy1:,.2f} SGD**")
    st.write(f"**Expected Sales for Strategy 1: ${expected_sales_strategy1:,.2f} SGD**")
    st.write(f"**Recommended Budget for Strategy 2: ${recommended_budget_strategy2:,.2f} SGD**")
    st.write(f"**Expected Sales for Strategy 2: ${expected_sales_strategy2:,.2f} SGD**")
    st.write(f"**Recommended Budget for Strategy 3: ${recommended_budget_strategy3:,.2f} SGD**")
    st.write(f"**Expected Sales for Strategy 3: ${expected_sales_strategy3:,.2f} SGD**")

    st.write(f"**Total Expected Sales from Allocated Budget: ${sum(expected_sales):,.2f} SGD**")

    # Generate inference using the weighted budget allocation data
    allocation_summary = {
        "Recommended Budget Strategy 1": recommended_budget_strategy1,
        "Recommended Budget Strategy 2": recommended_budget_strategy2,
        "Recommended Budget Strategy 3": recommended_budget_strategy3,
        "Expected Sales Strategy 1": expected_sales_strategy1,
        "Expected Sales Strategy 2": expected_sales_strategy2,
        "Expected Sales Strategy 3": expected_sales_strategy3
    }
    inference_result = generate_inference(allocation_summary)
    st.write(f"Inference: {inference_result}")
