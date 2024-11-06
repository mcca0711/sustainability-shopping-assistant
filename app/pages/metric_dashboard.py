# app/pages/metric_dashboard.py

import streamlit as st

missing_libraries = []

try:
    import matplotlib.pyplot as plt
    import seaborn as sns
except ImportError:
    missing_libraries.append("matplotlib seaborn")

try:
    import plotly.express as px
except ImportError:
    missing_libraries.append("plotly")

if missing_libraries:
    st.error(f"Required libraries are not installed. Please run 'pip install {' '.join(missing_libraries)}' to install them.")
    st.stop()

# ... rest of your imports ...


import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
import numpy as np
import datetime
import plotly.express as px

st.title("📈 Metrics Dashboard")

# Function to load data
@st.cache_data
def load_data():
    products = pd.read_csv('../data/products.csv')
    shopping_lists = pd.read_csv('../data/shopping_lists.csv')
    alternative_products = pd.read_csv('../data/alternative_products.csv')

    # Add 'UserID' column if it doesn't exist
    if 'UserID' not in shopping_lists.columns:
        shopping_lists['UserID'] = np.arange(len(shopping_lists))

    # Add 'Month' column for demonstration purposes
    current_date = datetime.datetime.now()
    shopping_lists['Month'] = pd.date_range(end=current_date, periods=len(shopping_lists), freq='D').strftime('%Y-%m')

    return products, shopping_lists, alternative_products 

products_df, shopping_lists_df, alternative_products_df = load_data()

# Ensure 'UserID' column exists
if 'UserID' not in shopping_lists_df.columns:
    st.error("'UserID' column is missing from the shopping lists data. Please check the data loading process.")
    st.stop()

st.write("Columns in shopping_lists_df:", shopping_lists_df.columns.tolist())

# Sidebar Filters
st.sidebar.header("Filters")

# Date Filter 
current_date = datetime.datetime.now()
num_months = 12
months = [current_date - pd.DateOffset(months=i) for i in range(num_months)]
months_str = [date.strftime('%Y-%m') for date in months]

# Select Month Range
start_month = st.sidebar.selectbox("Start Month", options=months_str)
end_month = st.sidebar.selectbox("End Month", options=months_str)

# Validate Month Selection
start_idx = months_str.index(start_month)
end_idx = months_str.index(end_month)
if start_idx > end_idx:
    st.sidebar.error("Start Month must be earlier than or equal to End Month.")
    selected_months = months_str[end_idx:start_idx+1]
else:
    selected_months = months_str[start_idx:end_idx+1]

# Category Filter
categories = ["All"] + list(products_df['Category'].unique())
selected_category = st.sidebar.selectbox("Select Product Category", options=categories)

# Apply Filters to Data
if selected_category == "All":
    filtered_products = products_df
else:
    filtered_products = products_df[products_df['Category'] == selected_category]

# Since shopping_lists_df doesn't have date information, we'll simulate it
# Assign random months to each shopping list for demonstration purposes
np.random.seed(42)  # For reproducibility
shopping_lists_df['Month'] = np.random.choice(months_str, size=shopping_lists_df.shape[0])

filtered_shopping_lists = shopping_lists_df[
    (shopping_lists_df['Month'].isin(selected_months)) 
]

# User Acquisition Metrics
st.header("🚀 User Acquisition Metrics")

# Total Users
total_users = filtered_shopping_lists['UserID'].nunique()
st.metric("Total Users", total_users)

# Generate synthetic user acquisition over time
# Since we don't have real date data, we'll simulate it
# For demonstration, assume users registered uniformly over the selected months

new_users_per_month = np.random.randint(50, 150, size=len(selected_months))
user_acquisition = pd.DataFrame({
    'Month': selected_months,
    'New Users': new_users_per_month
})

# Plot User Acquisition with Plotly
st.subheader("📅 New Users per Month")
fig = px.bar(user_acquisition, x='Month', y='New Users', title='New Users per Month',
             color='New Users', color_continuous_scale='Viridis')
st.plotly_chart(fig)

# User Retention Metrics
st.header("🔄 User Retention Metrics")

# Retention Rate
user_shopping_counts = filtered_shopping_lists['UserID'].value_counts()
retained_users = user_shopping_counts[user_shopping_counts > 1].count()
retention_rate = (retained_users / total_users) * 100 if total_users > 0 else 0
st.metric("User Retention Rate", f"{retention_rate:.2f}%")

# Plot Retention Over Time (Simulated)
retention_rates = np.linspace(50, 70, len(selected_months))
user_retention = pd.DataFrame({
    'Month': selected_months,
    'Retention Rate (%)': retention_rates
})

st.subheader("📈 User Retention Over Time")
fig = px.line(user_retention, x='Month', y='Retention Rate (%)',
              title='User Retention Over Time', markers=True)
fig.update_yaxes(range=[0, 100])
st.plotly_chart(fig)

# Feature Usage Metrics
st.header("📊 Feature Usage Metrics")

# Total Shopping Lists Uploaded
total_shopping_lists = filtered_shopping_lists.shape[0]
st.metric("Total Shopping Lists Uploaded", total_shopping_lists)

# Plot Shopping Lists Uploaded per Month
shopping_lists_per_month = pd.DataFrame({
    'Month': selected_months,
    'Shopping Lists': new_users_per_month * np.random.randint(1, 3, size=len(selected_months))
})

st.subheader("📝 Shopping Lists Uploaded per Month")
fig = px.bar(shopping_lists_per_month, x='Month', y='Shopping Lists',
             title='Shopping Lists Uploaded per Month',
             color='Shopping Lists', color_continuous_scale='Magma')
st.plotly_chart(fig)

# On-the-Spot Barcode Scanning Usage
st.subheader("📱 Barcodes Scanned per Month")
shopping_lists_per_month['Barcodes Scanned'] = shopping_lists_per_month['Shopping Lists'] * 10
fig = px.bar(shopping_lists_per_month, x='Month', y='Barcodes Scanned',
             title='Barcodes Scanned per Month',
             color='Barcodes Scanned', color_continuous_scale='Cividis')
st.plotly_chart(fig)

# Sustainability Impact Metrics
st.header("🌿 Sustainability Impact Metrics")

# Sustainable Alternatives Selected
total_alternatives_selected = int(shopping_lists_per_month['Barcodes Scanned'].sum() * 0.3)
st.metric("Sustainable Alternatives Selected", total_alternatives_selected)

# Estimated Reduction in Carbon Footprint
carbon_reduction = total_alternatives_selected * 0.5  # in kg CO₂
st.metric("Estimated Reduction in Carbon Footprint", f"{carbon_reduction} kg CO₂")

# Plot Carbon Reduction Over Time
carbon_df = pd.DataFrame({
    'Month': selected_months,
    'Carbon Reduction (kg CO₂)': shopping_lists_per_month['Barcodes Scanned'] * 0.3 * 0.5 / 10  # Simplified
})

st.subheader("🌍 Carbon Footprint Reduction Over Time")
fig = px.line(carbon_df, x='Month', y='Carbon Reduction (kg CO₂)',
              title='Carbon Footprint Reduction Over Time',
              markers=True, color_discrete_sequence=['green'])
st.plotly_chart(fig)

# Recommendations Metrics
st.header("💡 Recommendations Metrics")

# Recommendation Conversion Rate (Simulated)
conversion_rate = 20.0  # 20%
st.metric("Recommendation Conversion Rate", f"{conversion_rate}%")

# Plot Conversion Rate Over Time
conversion_df = pd.DataFrame({
    'Month': selected_months,
    'Conversion Rate (%)': [conversion_rate] * len(selected_months)
})

st.subheader("📈 Recommendation Conversion Rate Over Time")
fig = px.line(conversion_df, x='Month', y='Conversion Rate (%)',
              title='Recommendation Conversion Rate Over Time',
              markers=True, color_discrete_sequence=['purple'])
fig.update_yaxes(range=[0, 100])
st.plotly_chart(fig)

# Customer Satisfaction Metrics
st.header("⭐ Customer Satisfaction Metrics")

# Average Customer Satisfaction Score (Simulated)
avg_csat = 4.2  # out of 5
st.metric("Average Customer Satisfaction Score", f"{avg_csat}/5")

# Plot CSAT Scores Over Time
csat_scores = np.random.normal(loc=4.2, scale=0.1, size=len(selected_months))
csat_scores = np.clip(csat_scores, 3.5, 5.0)

csat_df = pd.DataFrame({
    'Month': selected_months,
    'CSAT Score': csat_scores
})

st.subheader("🌟 Customer Satisfaction Over Time")
fig = px.line(csat_df, x='Month', y='CSAT Score',
              title='Customer Satisfaction Over Time',
              markers=True, color_discrete_sequence=['orange'])
fig.update_yaxes(range=[3.5, 5.0])
st.plotly_chart(fig)

# Optional: Download Metrics as CSV
st.header("💾 Export Metrics Data")

if st.button("Download User Acquisition Data"):
    csv = user_acquisition.to_csv(index=False)
    st.download_button(
        label="Download User Acquisition Data",
        data=csv,
        file_name='user_acquisition.csv',
        mime='text/csv',
    )

if st.button("Download User Retention Data"):
    csv = user_retention.to_csv(index=False)
    st.download_button(
        label="Download User Retention Data",
        data=csv,
        file_name='user_retention.csv',
        mime='text/csv',
    )

