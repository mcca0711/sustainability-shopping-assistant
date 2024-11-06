 # app/pages/recommendations.py

import streamlit as st
import pandas as pd

st.title("🔍 Recommendations")

st.write("This page will provide eco-friendly product recommendations based on your shopping list.")

# Placeholder for recommendations
st.write("Recommended Products:")
dummy_recommendations = ['Product D', 'Product E', 'Product F']
for product in dummy_recommendations:
    st.write(f"- {product}")

