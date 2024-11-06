 # synthetic_data_generator.py

import pandas as pd
import numpy as np
from faker import Faker
import random
import os

fake = Faker()

def generate_product_database(num_products=1000, output_path='data/products.csv'):
    categories = ['Electronics', 'Clothing', 'Home & Kitchen', 'Beauty', 'Sports', 'Books', 'Toys']
    brands = ['EcoBrand', 'GreenLife', 'SustainIt', 'NatureWear', 'PureHome', 'BioBeauty', 'FitGear']
    sustainability_levels = ['High', 'Medium', 'Low']
    suffixes = ['Pro', 'Max', 'Plus', 'Lite', 'Eco']

    data = []
    for i in range(num_products):
        product = {
            'ProductID': i + 1,
            'Name': f"{fake.word().capitalize()} {random.choice(suffixes)} {fake.random_number(digits=3)}",
            'Brand': random.choice(brands),
            'Category': random.choice(categories),
            'Barcode': fake.ean(length=13),
            'SustainabilityRating': random.choices(sustainability_levels, weights=[0.3, 0.5, 0.2])[0],
            'Price': round(random.uniform(5.0, 500.0), 2)
        }
        data.append(product)

    product_df = pd.DataFrame(data)
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    product_df.to_csv(output_path, index=False)
    print(f"Product database generated and saved to '{output_path}'")
    return product_df

def generate_shopping_lists(product_df, num_lists=100, items_per_list=5, output_path='data/shopping_lists.csv'):
    shopping_lists = []
    for i in range(num_lists):
        shopping_list = product_df.sample(n=items_per_list)
        shopping_list['ListID'] = i + 1
        shopping_list['Quantity'] = np.random.randint(1, 5, size=items_per_list)
        shopping_lists.append(shopping_list)
    shopping_df = pd.concat(shopping_lists).reset_index(drop=True)
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    shopping_df.to_csv(output_path, index=False)
    print(f"Shopping lists generated and saved to '{output_path}'")
    return shopping_df

def generate_alternative_products(product_df, num_alternatives=3, output_path='data/alternative_products.csv'):
    alternatives = []
    for _, product in product_df.iterrows():
        category_products = product_df[product_df['Category'] == product['Category']]
        alternative_products = category_products[category_products['ProductID'] != product['ProductID']].sample(n=min(num_alternatives, len(category_products)-1))
        for _, alt_product in alternative_products.iterrows():
            sustainability_comparison = 'Better' if alt_product['SustainabilityRating'] > product['SustainabilityRating'] else 'Worse' if alt_product['SustainabilityRating'] < product['SustainabilityRating'] else 'Same'
            alternatives.append({
                'OriginalProductID': product['ProductID'],
                'AlternativeProductID': alt_product['ProductID'],
                'PriceDifference': alt_product['Price'] - product['Price'],
                'SustainabilityComparison': sustainability_comparison
            })
    alternative_df = pd.DataFrame(alternatives)
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    alternative_df.to_csv(output_path, index=False)
    print(f"Alternative products generated and saved to '{output_path}'")
    return alternative_df

if __name__ == "__main__":
    product_df = generate_product_database()
    generate_shopping_lists(product_df)
    generate_alternative_products(product_df)

