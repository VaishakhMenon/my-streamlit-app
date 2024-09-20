import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import streamlit as st
from inference import generate_inference  # Import the inference function

def perform_segmentation(df):
    """
    Segment the market by account types and analyze the sales performance with respect to 
    the number of competitor brands. Visualize the relationship and correlation.
    """
    st.header("Market Segmentation by Account Type")

    # Ensure 'compBrand', 'sales', and 'accType' columns exist in the dataset
    if 'compbrand' in df.columns and 'sales' in df.columns and 'acctype' in df.columns:
        
        # Group by account type and competitor brands, then calculate average sales
        segmented_data = df.groupby(['acctype', 'compbrand'])['sales'].mean().reset_index()

        # Display the segmented data in Streamlit (optional, to check the structure)
        st.write("Segmented Data (Average Sales by Account Type and Competitor Brands):")
        st.dataframe(segmented_data)

        # Calculate correlation between competitor brands and sales for each account type
        correlations_by_accType = df.groupby('acctype').apply(
            lambda x: x['compbrand'].corr(x['sales'])
        ).reset_index()

        # Rename columns for clarity
        correlations_by_accType.columns = ['Account Type', 'Correlation']

        # Display correlations in Streamlit
        st.write("Correlation Between Competitor Brands and Sales by Account Type:")
        st.dataframe(correlations_by_accType)

        # Plot sales vs competitor brands for each account type
        st.subheader("Sales vs Competitor Brands for Each Account Type")
        plt.figure(figsize=(14, 8))

        # Creating subplots for each account type
        account_types = df['acctype'].unique()
        for i, accType in enumerate(account_types, 1):
            plt.subplot(2, 2, i)
            subset = df[df['acctype'] == accType]
            sns.scatterplot(data=subset, x='compbrand', y='sales', hue='compbrand', palette='coolwarm')
            plt.title(f"Sales vs Competitor Brands for {accType}")
            plt.xlabel("Number of Competitor Brands")
            plt.ylabel("Sales (USD)")
            plt.grid(True)

        plt.tight_layout()
        st.pyplot(plt)

        # Bar plot of correlation by account type
        st.subheader("Correlation Between Competitor Brands and Sales by Account Type")
        plt.figure(figsize=(10, 6))
        sns.barplot(data=correlations_by_accType, x='Account Type', y='Correlation', palette='Blues_d')
        plt.title('Correlation Between Competitor Brands and Sales by Account Type')
        plt.xlabel('Account Type')
        plt.ylabel('Correlation')
        plt.xticks(rotation=45)
        plt.grid(True)
        st.pyplot(plt)

        # Generate inference based on the segmentation analysis
        segmentation_summary = {
            "Segmented Data Summary": segmented_data.describe().to_dict(),
            "Correlation Summary": correlations_by_accType.describe().to_dict(),
        }
        inference_result = generate_inference(segmentation_summary)
        st.write(f"Inference: {inference_result}")

    else:
        st.error("Required columns 'compbrand', 'sales', or 'acctype' are missing in the dataset.")
