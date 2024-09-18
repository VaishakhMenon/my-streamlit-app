# segmentation.py

import streamlit as st
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import seaborn as sns
import matplotlib.pyplot as plt

def perform_segmentation(df):
    """
    Perform market segmentation using K-Means clustering.
    """
    st.header("Market Segmentation")

    # Allow the user to select features for clustering
    st.write("### Select Features for Clustering")
    numeric_columns = df.select_dtypes(include=['float', 'int']).columns.tolist()

    if not numeric_columns:
        st.warning("No numeric columns available for clustering.")
        return

    selected_features = st.multiselect("Select features:", numeric_columns, default=numeric_columns)

    if len(selected_features) < 2:
        st.warning("Please select at least two features for clustering.")
        return

    # Select number of clusters
    n_clusters = st.slider("Select number of clusters (k):", min_value=2, max_value=10, value=3, step=1)

    # Prepare the data
    X = df[selected_features].dropna()

    # Standardize the data
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    # Apply K-Means clustering
    kmeans = KMeans(n_clusters=n_clusters, random_state=42)
    clusters = kmeans.fit_predict(X_scaled)

    # Add cluster assignments to the DataFrame
    df_clustered = df.copy()
    df_clustered['Segment'] = clusters

    # Display cluster centers
    st.write("### Cluster Centers (in Original Scale):")
    centers = pd.DataFrame(scaler.inverse_transform(kmeans.cluster_centers_), columns=selected_features)
    st.dataframe(centers)

    # Visualize clusters
    st.write("### Cluster Visualization")
    if len(selected_features) >= 2:
        # Select features for x and y axes
        x_axis = st.selectbox("Select feature for X-axis:", selected_features)
        y_axis_options = [col for col in selected_features if col != x_axis]
        if y_axis_options:
            y_axis = st.selectbox("Select feature for Y-axis:", y_
