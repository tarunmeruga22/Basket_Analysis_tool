        
import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# Load the data from the Excel file
# file_path = '/Users/apple/Desktop/Basket_analysis/output_combinations_with_titles.xlsx'
# df = pd.read_excel(file_path, sheet_name='Sheet1')
if 'df' not in st.session_state:
    st.write("No data available. Please upload a CSV file first.")
else:
    df = st.session_state.df  # Retrieve the DataFrame
# Calculate the top 10 selling products based on the 'TOTAL' column
    top_10_selling_products = df[['TOP_PRODUCT_TITLE', 'TOTAL']].drop_duplicates().sort_values(by='TOTAL', ascending=False).head(10)

    # Set page configuration
    st.set_page_config(page_title="Basket Analysis Dashboard", page_icon="🛒", layout="wide")

    # Sidebar for product selection with search bar
    st.sidebar.title("Basket Analysis")

    # Add a search bar to the sidebar to filter the dropdown options
    search_query = st.sidebar.text_input("Search Products", "")

    # Filter products based on the search query
    filtered_products = df['TOP_PRODUCT_TITLE'].unique()
    if search_query:
        filtered_products = [product for product in filtered_products if search_query.lower() in product.lower()]

    # Dropdown for selecting the product
    selected_product = st.sidebar.selectbox("Select Product Title", filtered_products)

    # Filter data for selected product
    filtered_data = df[df['TOP_PRODUCT_TITLE'] == selected_product]

    # Main Dashboard
    st.header(f"Product Title: {selected_product}")
    st.subheader("Product Summary")   
    st.metric("Total Orders", filtered_data['TOTAL'].sum())

    # Top Selling Products
    st.subheader("Top Selling Combo")
    st.markdown(f"1. **{filtered_data['COMBO 1 PRODUCT_TITLE'].values[0]}** + {selected_product}")
    st.markdown(f"2. **{filtered_data['COMBO 2 PRODUCT_TITLE'].values[0]}** + {selected_product}")
    st.markdown(f"3. **{filtered_data['COMBO 3 PRODUCT_TITLE'].values[0]}** + {selected_product}")
    st.markdown(f"4. **{filtered_data['COMBO 4 PRODUCT_TITLE'].values[0]}** + {selected_product}")
    st.markdown(f"5. **{filtered_data['COMBO 5 PRODUCT_TITLE'].values[0]}** + {selected_product}")


    # Generate the horizontal bar chart for cross-sold items with a red gradient
    st.subheader("Main Item and Cross-sold Items")

    # Data for Main Item and Cross-Sold Items
    main_item = filtered_data['TOP_PRODUCT_TITLE'].values[0]
    main_item_count = filtered_data['TOTAL'].values[0]
    cross_sold_items = filtered_data[['COMBO 1 PRODUCT_TITLE', 'COMBO 2 PRODUCT_TITLE', 'COMBO 3 PRODUCT_TITLE', 'COMBO 4 PRODUCT_TITLE', 'COMBO 5 PRODUCT_TITLE', 'COMBO 6 PRODUCT_TITLE', 'COMBO 7 PRODUCT_TITLE', 'COMBO 8 PRODUCT_TITLE', 'COMBO 9 PRODUCT_TITLE', 'COMBO 10 PRODUCT_TITLE']].values[0]
    cross_sold_counts = filtered_data[['COMBO 1 COUNT', 'COMBO 2 COUNT', 'COMBO 3 COUNT', 'COMBO 4 COUNT', 'COMBO 5 COUNT', 'COMBO 6 COUNT', 'COMBO 7 COUNT', 'COMBO 8 COUNT', 'COMBO 9 COUNT', 'COMBO 10 COUNT']].values[0]

    # Combine main item and cross-sold counts for a consistent gradient
    all_items = [main_item] + list(cross_sold_items)
    all_counts = [main_item_count] + list(cross_sold_counts)

    # Create a grouped horizontal bar chart with the same red gradient for all items
    fig = go.Figure()

    # Add bars for both main item and cross-sold items
    fig.add_trace(go.Bar(
        y=all_items,  # Main and cross-sold items
        x=all_counts,  # Counts for main and cross-sold items
        orientation='h',
        marker=dict(
            color=all_counts,  # Apply gradient based on total counts
            colorscale='Reds'  # Red color gradient for all items
        ),
        text=[f'{count}' for count in all_counts],  # Display count as text
        textposition='auto'
    ))

    # Update layout
    fig.update_layout(
        barmode='stack',
        title="Main Item and Cross-sold Items",
        xaxis_title="Count",
        yaxis_title="Items",
        height=600,
        width=900,
        plot_bgcolor='rgba(0,0,0,0)',  # Transparent background
        showlegend=False
    )

    st.plotly_chart(fig)

    # Top 10 Selling Products
    st.subheader("Top 10 Selling Products")

    # Create a bar chart for the top 10 selling products with blue gradient
    fig_top_10 = go.Figure(go.Bar(
        x=top_10_selling_products['TOTAL'].values,
        y=top_10_selling_products['TOP_PRODUCT_TITLE'].values,
        orientation='h',
        marker=dict(
            color=top_10_selling_products['TOTAL'].values,  # Apply blue gradient based on counts
            colorscale='Blues'
        ),
        text=top_10_selling_products['TOTAL'].values,  # Display counts as text
        textposition='auto'
    ))

    # Update layout for top 10 products chart
    fig_top_10.update_layout(
        title="Top 10 Selling Products by Total Orders",
        xaxis_title="Total Orders",
        yaxis_title="Product Title",
        height=500,
        plot_bgcolor='rgba(0,0,0,0)'  # Transparent background
    )

    # Display top 10 selling products chart
    st.plotly_chart(fig_top_10)

    # Top 10 Combo Percentages
    st.subheader("Top 5 Combo Percentages")

    # Calculate combo percentages for each combo relative to the total
    combo_titles = ['COMBO 1 PRODUCT_TITLE', 'COMBO 2 PRODUCT_TITLE', 'COMBO 3 PRODUCT_TITLE', 'COMBO 4 PRODUCT_TITLE', 'COMBO 5 PRODUCT_TITLE']
    combo_counts = ['COMBO 1 COUNT', 'COMBO 2 COUNT', 'COMBO 3 COUNT', 'COMBO 4 COUNT', 'COMBO 5 COUNT']

    combo_percentages = []
    total_count = filtered_data['TOTAL'].values[0]

    for combo_count in combo_counts:
        combo_percentage = (filtered_data[combo_count].values[0] / total_count) * 100
        combo_percentages.append(combo_percentage)

    # Define reversed colorscale for heatmap (reversed gradient from green to red)
    colorscale = ['#7FFF00', '#ADFF2F', '#FFD700', '#FFA500', '#FF6347']  # Reversed: green to red

    # Display top combos and their percentages with reversed gradient heatmap
    for i, (combo, percentage) in enumerate(zip(combo_titles, combo_percentages)):
        combo_product = filtered_data[combo].values[0]
        
        # Use the index to determine the color from the reversed colorscale
        color = colorscale[i % len(colorscale)]
        
        st.write(f'{i+1}. {combo_product} + {selected_product}')
        st.write(f'   Percentage of total orders: {percentage:.2f}%')
        
        # Display the heatmap bar with reversed gradient color
        st.markdown(f"<div style='background-color:{color};padding:10px;border-radius:5px;width:{percentage}%;'></div>", unsafe_allow_html=True)

    # Feedback Section at the bottom of the sidebar
    st.sidebar.markdown("<br><br><br><br><br><br><br><br><br><br><br>", unsafe_allow_html=True)  # Add some space
    st.sidebar.markdown("For any queries:")
    Linkedin_link = "www.linkedin.com/in/tarun-meruga-0b687822b"
    st.sidebar.markdown(f"[Tarun Meruga]({Linkedin_link})")
    st.sidebar.markdown("[tarunmeruga22@gmail.com](mailto:tarunmeruga22@gmail.com)")

    # Google Form Link
    google_form_link = "https://forms.gle/pAd3mjjms6zfpZDj9"  # Replace with your actual Google Form link
    st.sidebar.markdown(f"[Feedback Please]( {google_form_link})")
