# app/main.py

import streamlit as st

st.set_page_config(page_title="Sustainable Shopping App", layout="wide")

st.title("🌿 Sustainable Shopping App")
st.write("""
Welcome to the Sustainable Shopping App! Analyze your shopping lists for sustainability and make eco-friendly choices effortlessly.
""")

st.sidebar.title("Navigation")
page = st.sidebar.selectbox("Go to", [
    "Home",
    "Upload Shopping List",
    "Sustainability Report",
    "Barcode Scanning",
    "Recommendations",
    "Metrics Dashboard"  # Added Metrics Dashboard
])

if page == "Home":
    st.write("Welcome to the Sustainable Shopping App! Use the sidebar to navigate through different features.")
elif page == "Upload Shopping List":
    st.write("This is the Upload Shopping List page.")
elif page == "Sustainability Report":
    st.write("This is the Sustainability Report page.")
elif page == "Barcode Scanning":
    st.write("This is the Barcode Scanning page.")
elif page == "Recommendations":
    st.write("This is the Recommendations page.")
elif page == "Metrics Dashboard":
    st.write("### Loading Metrics Dashboard...")
    # Streamlit automatically loads pages from the 'pages' directory
