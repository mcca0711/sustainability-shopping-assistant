# app/pages/sustainability_report.py

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.title("📊 Sustainability Report")

if 'sustainability_report' in st.session_state:
    report_df = st.session_state['sustainability_report']
    st.dataframe(report_df)

    # Visualize sustainability ratings
    st.subheader("Sustainability Ratings")
    rating_counts = report_df['Sustainability Rating'].value_counts().reindex(['High', 'Medium', 'Low', 'Unknown'], fill_value=0)
    fig, ax = plt.subplots()
    sns.barplot(x=rating_counts.index, y=rating_counts.values, palette='viridis', ax=ax)
    ax.set_xlabel('Sustainability Rating')
    ax.set_ylabel('Count')
    ax.set_title('Distribution of Sustainability Ratings')
    st.pyplot(fig)

    # Display alternative suggestions
    st.subheader("Alternative Product Suggestions")
    for index, row in report_df.iterrows():
        if isinstance(row['Alternative Suggestions'], list) and row['Alternative Suggestions']:
            alternatives = ', '.join(row['Alternative Suggestions'][:3])  # Show top 3 suggestions
            st.write(f"**{row['Product']}**: {alternatives}")
        else:
            st.write(f"**{row['Product']}**: {row['Alternative Suggestions']}")
else:
    st.write("No sustainability report available. Please upload a shopping list first.")
 
