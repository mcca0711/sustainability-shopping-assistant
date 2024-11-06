 # app/pages/upload_shopping_list.py

import streamlit as st
import pandas as pd
from PIL import Image
import pytesseract
import os

st.title("📋 Upload Shopping List")

@st.cache_data
def load_product_data():
    return pd.read_csv('../data/products.csv')

@st.cache_data
def load_alternative_products():
    return pd.read_csv('../data/alternative_products.csv')

product_df = load_product_data()
alternative_df = load_alternative_products()

upload_method = st.radio("Choose upload method:", ("Text Input", "Image Upload"))

def get_sustainability_report(items, product_df, alternative_df):
    report = []
    for item in items:
        product = product_df[product_df['Name'].str.contains(item, case=False, na=False)]
        if not product.empty:
            product_info = product.iloc[0]
            alternatives = alternative_df[alternative_df['OriginalProductID'] == product_info['ProductID']]['AlternativeProductID']
            alternative_names = product_df[product_df['ProductID'].isin(alternatives)]['Name'].tolist()
            report.append({
                'Product': product_info['Name'],
                'Sustainability Rating': product_info['SustainabilityRating'],
                'Alternative Suggestions': alternative_names if alternative_names else ['No alternatives available']
            })
        else:
            report.append({
                'Product': item,
                'Sustainability Rating': 'Unknown',
                'Alternative Suggestions': ['No data available']
            })
    return pd.DataFrame(report)

if upload_method == "Text Input":
    shopping_list_text = st.text_area("Enter your shopping list (one item per line):")
    if st.button("Submit"):
        items = [item.strip() for item in shopping_list_text.split('\n') if item.strip()]
        st.write(f"You have entered {len(items)} items.")
        st.write("Items:", items)
        # Generate sustainability report
        report_df = get_sustainability_report(items, product_df, alternative_df)
        st.session_state['sustainability_report'] = report_df
        st.success("Sustainability report generated!")
elif upload_method == "Image Upload":
    uploaded_image = st.file_uploader("Upload an image of your shopping list", type=["png", "jpg", "jpeg"])
    if uploaded_image is not None:
        image = Image.open(uploaded_image)
        st.image(image, caption='Uploaded Image', use_column_width=True)
        if st.button("Extract Text"):
            # Specify the path to the Tesseract executable if necessary
            # pytesseract.pytesseract.tesseract_cmd = r'/path/to/tesseract'
            extracted_text = pytesseract.image_to_string(image)
            st.write("Extracted Shopping List:")
            st.text_area("Extracted Text:", value=extracted_text, height=200)
            items = [item.strip() for item in extracted_text.split('\n') if item.strip()]
            st.write(f"Detected {len(items)} items.")
            st.write("Items:", items)
            # Generate sustainability report
            report_df = get_sustainability_report(items, product_df, alternative_df)
            st.session_state['sustainability_report'] = report_df
            st.success("Sustainability report generated!")

