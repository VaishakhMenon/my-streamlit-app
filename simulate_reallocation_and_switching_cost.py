import pandas as pd
import streamlit as st
import altair as alt

def calculate_efficiency(df):
    """
    Calculate the efficiency of each strategy in terms of sales per dollar spent.
    """
    # Calculate total spending for each strategy
    total_spending_strategy1 = df['spending_strategy1'].sum()
    total_spending_strategy2 = df['spending_strategy2'].sum()
    total_spending_strategy3 = df['spending_strategy3'].sum()

    # Calculate total sales for each strategy
    total_sales_strategy1 = df['sales_from_strategy1'].sum()
    total_sales_strategy2 = df['sales_from_strategy2'].sum()
    total_sales_strategy3 = df['sales_from_strategy3'].sum()

    # Calculate Efficiency (Sales per Dollar Spent)
    efficiency_strategy1 = total_sales_strategy1 / total_spending_strategy1
    efficiency_strategy2 = total_sales_strategy2 / total_spending_strategy2
    efficiency_strategy3 = total_sales_strategy3 / total_spending_strategy3

    # Display Efficiency of Each Strategy
    st.write("### Efficiency of Each Strategy (Sales per Dollar Spent)")
    st.write(f"**Strategy 1:** ${efficiency_strategy1:.2f} per dollar")
    st.write(f"**Strategy 2:** ${efficiency_strategy2:.2f} per dollar")
    st.write(f"**Strategy 3:** ${efficiency_strategy3:.2f} per dollar")

    return efficiency_strategy1, efficiency_strategy2, efficiency_strategy3


def simulate_reallocation(df, efficiency_strategy1, efficiency_strategy2, reallocation_percentage=0.5):
    """
    Simulate reallocating resources from Strategy 3 to Strategies 1 and 2.
    """
    total_spending_strategy3 = df['spending_strategy3'].sum()

    # Calculate the amount of spending to reallocate from Strategy 3
    spending_reallocated = total_spending_strategy3 * reallocation_percentage

    # Split the reallocated amount equally between Strategy 1 and Strategy 2
    spending_to_strategy1 = spending_reallocated / 2
    spending_to_strategy2 = spending_reallocated / 2

    total_spending_strategy1 = df['spending_strategy1'].sum() + spending_to_strategy1
    total_spending_strategy2 = df['spending_strategy2'].sum() + spending_to_strategy2

    new_sales_strategy1 = total_spending_strategy1 * efficiency_strategy1
    new_sales_strategy2 = total_spending_strategy2 * efficiency_strategy2

    new_total_sales = new_sales_strategy1 + new_sales_strategy2

    st.write(f"### Total New Sales After Reallocation: ${new_total_sales:,.2f}")
    return new_sales_strategy1, new_sales_strategy2, new_total_sales


def calculate_switching_cost(df, efficiency_strategy1, efficiency_strategy2, switching_cost_percentage=0.1):
    """
    Simulate switching costs by adjusting efficiency and recalculating sales.
    """
    total_spending_strategy3 = df['spending_strategy3'].sum()

    spending_to_strategy1 = 0.5 * total_spending_strategy3
    spending_to_strategy2 = 0.5 * total_spending_strategy3

    adjusted_efficiency_strategy1 = efficiency_strategy1 * (1 - switching_cost_percentage)
    adjusted_efficiency_strategy2 = efficiency_strategy2 * (1 - switching_cost_percentage)

    new_sales_strategy1_after_switching = adjusted_efficiency_strategy1 * spending_to_strategy1
    new_sales_strategy2_after_switching = adjusted_efficiency_strategy2 * spending_to_strategy2

    new_total_sales_after_switching = (
        new_sales_strategy1_after_switching + new_sales_strategy2_after_switching
    )

    st.write(f"### Total Sales After Switching Costs: ${new_total_sales_after_switching:,.2f}")
    
    # Display the chart
    chart_data = pd.DataFrame({
        'Strategy': ['Strategy 1', 'Strategy 2'],
        'New Sales After Switching': [new_sales_strategy1_after_switching, new_sales_strategy2_after_switching]
    })

    chart = alt.Chart(chart_data).mark_bar().encode(
        x='Strategy',
        y='New Sales After Switching'
    ).properties(title='Sales Impact After Switching Costs')

    st.altair_chart(chart, use_container_width=True)


def simulate_strategy_reallocation(df):
    """
    Combine all the steps into one function.
    """
    st.header("Simulate Strategy Reallocation and Switching Costs")

    # Calculate efficiency
    efficiency_strategy1, efficiency_strategy2, efficiency_strategy3 = calculate_efficiency(df)

    # Simulate reallocation of budget
    st.subheader("Simulate Reallocation of Strategy 3 Budget")
    new_sales_strategy1, new_sales_strategy2, new_total_sales = simulate_reallocation(
        df, efficiency_strategy1, efficiency_strategy2
    )

    # Calculate sales impact after switching costs
    st.subheader("Simulate Impact of Switching Costs")
    calculate_switching_cost(df, efficiency_strategy1, efficiency_strategy2)
