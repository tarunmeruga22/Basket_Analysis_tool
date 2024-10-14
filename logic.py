import pandas as pd
import numpy as np
from itertools import combinations_with_replacement

# Step 0: Clean the data, create product inventory, and assign TEMP_Product_IDs
def preprocess_input_data(df):
    # Step 1: Load the CSV file

    # Step 2: Drop rows where Product ID is NULL or '0'
    df_cleaned = df.dropna()  # Remove NULL product IDs
    df_cleaned = df_cleaned[df_cleaned['product_id'] != 0]  # Remove rows where product_id is '0'

    # Step 3: Create a DataFrame with unique product titles and product IDs from the cleaned data
    product_inventory = df_cleaned[['product_id', 'product_title']].drop_duplicates().reset_index(drop=True)
    product_inventory['TEMP_Product_ID'] = range(1, len(product_inventory) + 1)

    # Step 4: Merge the TEMP_Product_ID back into the cleaned data
    df_cleaned = df_cleaned.merge(product_inventory[['product_id', 'TEMP_Product_ID']], on='product_id', how='left')
    # display(df_cleaned)
    
    Max_product = df_cleaned.TEMP_Product_ID.max()
    return df_cleaned, product_inventory, Max_product

# Step 1: Read cleaned data and create the order-product dictionary
def process_excel_to_dict(df):
    Matrix_order = df.TEMP_Product_ID.max()  # Get the maximum TEMP_Product_ID to determine the matrix size
    print(f"Matrix order: {Matrix_order}")

    # Create dictionary where each order_id is a key and product IDs are in a list as the value
    order_dict = df.groupby('order_id')['TEMP_Product_ID'].apply(list).to_dict()

    # Sort product_ids for each order_id
    for order_id in order_dict:
        order_dict[order_id] = sorted(order_dict[order_id])

    return order_dict, Matrix_order

# Step 2: Generate unique combinations of product_ids for each order_id
def generate_combinations(order_product_dict):
    result = []
    for order_id, product_ids in order_product_dict.items():
        combinations_list = list(combinations_with_replacement(product_ids, 2))
        result.append((order_id, combinations_list))
    return result

# Step 3: Create the N*N matrix and fill it with the frequency of each combination
def create_frequency_matrix(combinations_list, matrix_order):
    matrix = np.zeros((matrix_order + 1, matrix_order + 1), dtype=int)  # Initialize an N+1 x N+1 matrix

    for _, comb_list in combinations_list:
        for (i, j) in comb_list:
            matrix[i][j] += 1
            if i != j:
                matrix[j][i] += 1  # Ensure symmetric increment for (j, i)
    return matrix

# Step 4: Extract top combinations based on frequency matrix for all products, and add product titles
def extract_top_combinations(matrix, top_n, product_inventory):
    diag_values = np.diag(matrix)  # Get the diagonal values
    top_products = np.argsort(diag_values)[-top_n:][::-1]  # Top N products with highest self-combinations

    result_table = []

    # Create a dictionary from TEMP_Product_ID to product_title
    product_title_dict = product_inventory.set_index('TEMP_Product_ID')['product_title'].to_dict()

    for prod_id in top_products:
        row = matrix[prod_id]  # Get the corresponding row for the product

        # Exclude the diagonal element (self-combination) and get top combinations
        top_combinations = np.argsort(row)[::-1]  # Sorted indices of combinations (descending)
        top_combinations = [idx for idx in top_combinations if idx != prod_id][:10]  # Exclude self and take top 10

        total_count = matrix[prod_id, prod_id]  # Total count of the product itself

        # Create a dictionary for the top combinations with their counts, percentages, and product titles
        combination_data = {
            'TOP_TEMP_PRODUCT_ID': prod_id,
            'TOP_PRODUCT_TITLE': product_title_dict.get(prod_id, "Unknown"),  # Add product title
            'TOTAL': total_count,
        }

        for i, combo_id in enumerate(top_combinations):
            count = row[combo_id]
            percentage = (count / total_count) * 100 if total_count > 0 else 0
            combination_data[f'COMBO {i + 1}'] = f"{prod_id},{combo_id}"
            combination_data[f'COMBO {i + 1} PRODUCT_TITLE'] = product_title_dict.get(combo_id, "Unknown")  # Add combo product title
            combination_data[f'COMBO {i + 1} COUNT'] = count
            combination_data[f'COMBO {i + 1} PERCENTAGE'] = percentage

        result_table.append(combination_data)

    return result_table

# # Step 5: Save result to Excel
# def save_result_to_excel(result_table, file_name='output_combinations_with_titles.xlsx'):
#     df = pd.DataFrame(result_table)
#     df.to_excel(file_name, index=False)
#     print(f"Result saved to {file_name}")

# def save_matrix_to_excel(matrix, file_name='frequency_matrix.xlsx'):
#     df = pd.DataFrame(matrix)
#     df.to_excel(file_name, index=False, header=False)
#     print(f"Matrix saved to {file_name}")

def master(df):
        # # Example usage:
        # file_path = '/Users/apple/Desktop/Basket_analysis/Testing/TBOF/TBOF_sales_2024-04-01_2024-09-29.csv'  # Replace with your actual file path

        # Step 0: Preprocess input data to clean and create TEMP_Product_IDs from the cleaned data
        cleaned_df, product_inventory, Max_product = preprocess_input_data(df)

        # Step 1: Process the cleaned data and create the dictionary
        order_product_dict, Matrix_order = process_excel_to_dict(cleaned_df)

        # Step 2: Generate combinations and store the result
        combinations_list = generate_combinations(order_product_dict)

        # Step 3: Create the frequency matrix
        frequency_matrix = create_frequency_matrix(combinations_list, Matrix_order)

        # Step 4: Extract top products and their combinations along with counts and product titles
        result_table = extract_top_combinations(frequency_matrix, Max_product, product_inventory)

        df = pd.DataFrame(result_table)

        return df

  
