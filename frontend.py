import streamlit as st
import base64
import pandas as pd
from logic import master

# Set page configuration
st.set_page_config(page_title="Leverage Your Sales", page_icon="🛒", layout="wide")

# Load the background image
image_path = "/Users/apple/Downloads/maxim-berg-OKjxoWaKNI0-unsplash.jpg"
with open(image_path, "rb") as image_file:
    encoded_image = base64.b64encode(image_file.read()).decode()

# Create a sample CSV file content for download
sample_csv_data = """order_id,product_id,product_title
485162XXXXXX1,6572374XXXXXX,Product A
485162XXXXXX2,6572374XXXXXX,Product B
485162XXXXXX3,6572374XXXXXX,Product C
"""

# Function to convert CSV string to a downloadable link
def generate_download_link(csv_data, filename, link_text):
    b64 = base64.b64encode(csv_data.encode()).decode()  # Convert to base64
    return f'<a href="data:file/csv;base64,{b64}" download="{filename}">{link_text}</a>'

# Apply custom CSS for the background and styling
st.markdown(f"""
    <style>
    /* Set the entire page's background image */
    .stApp {{
        background-image: url(data:image/png;base64,{encoded_image});
        background-size: cover;
        background-position: center;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }}

    /* Style for main content container */
    .content-container {{
        text-align: center;
        color: #FF6A95;
        padding: 80px 10px;
    }}

    /* Styling the header text */
    .header-title {{
        font-size: 6.5em;
        font-weight: bold;
        color: #FF6A95;
        background: linear-gradient(to right, #FF6A95, #C773FF);
        -webkit-background-clip: text;
        color: transparent;
        margin-top: -30px; 
    }}

    /* Styling the description under the title */
    .description-text {{
        font-size: 1.5em;
        font-weight: normal;  /* Make the text unbold */
        color: #36454F;       /* Make the text black */
        letter-spacing: 0.03em;  /* Increase letter spacing */
        margin-top: -18px;    /* Bring it closer to the title */
    }}

    /* Styling the description under the title */
    .description-Para {{
        font-size: 0.9em;
        font-weight: italic;  /* Make the text unbold */
        color: #36454F;       /* Make the text black */
        letter-spacing: 0.1em;  /* Increase letter spacing */
        width: 900px; 
        text-align: left;
        margin-top: 10px;
    }}

    /* Styling the file upload input */
    .stFileUploader > label {{
        display: flex;
        justify-content: center;
    }}
    
    /* Style for the upload area */
    .stFileUploader {{
        width: 380px;  /* Set a specific width for the drag-and-drop area */
    }}
    
    /* Style for file upload instructions */
    .file-upload-instructions {{
        margin-top: 120px;
        font-size: 1.3em;
        font-weight: bold;
        color: #36454F;
        opacity: 0.8;
    }}

    /* Hyperlink styling for Sample Data */
    .sample-data-link {{
        color: #FF8096;
        text-decoration: underline;
        font-size: 1em;
        cursor: pointer;
    }}
    </style>
""", unsafe_allow_html=True)

# Main Content
st.markdown("<div class='content-container'>", unsafe_allow_html=True)

# Display header title
st.markdown("<h1 class='header-title'>Basket Analysis</h1>", unsafe_allow_html=True)

# Description text under the title
st.markdown("<div class='description-text'>Identify frequently purchased product combinations from your Sales.</div>", unsafe_allow_html=True)

st.markdown('''<div class='description-Para'>Basket analysis is crucial for Direct-to-Consumer (D2C) brands because it enables them to identify
             product combinations that are frequently purchased together.This helps brands personalize product recommendations based 
            on frequently bought items, driving upselling and cross-selling strategies. According to a study, personalized product
            recommendations account for 26% of eCommerce revenue. Offering curated suggestions can significantly increase Average Order Value (AOV)
             by up to 10-30%, helping brands optimize their revenue from every customer interaction.</div>''', unsafe_allow_html=True)

# Upload CSV section
st.markdown("<div class='file-upload-instructions'>Please upload the Sales data in a CSV file</div>", unsafe_allow_html=True)

# Add a sample data download link below the file upload instructions
st.markdown(generate_download_link(sample_csv_data, "sample_data.csv", "<div class='sample-data-link'>Sample data</div>"), unsafe_allow_html=True)
uploaded_file = st.file_uploader("", type=["csv"], label_visibility="collapsed")

# Columns that must be present in the CSV
required_columns = ["order_id", "product_id", "product_title"]

# Create columns for buttons to be side by side
col1, col2 = st.columns([1, 1])

with col1:
    # Submit button
    if st.button("Submit"):
        if uploaded_file:
            # Read the CSV file into a DataFrame
            df = pd.read_csv(uploaded_file)

            # Check if required columns are in the uploaded CSV
            missing_columns = [col for col in required_columns if col not in df.columns]

            if missing_columns:
                # Display an error if any required column is missing
                st.error(f"Error: The following required columns are missing: {', '.join(missing_columns)}")
            else:
                # Display success message if all columns are present
                st.success("File uploaded successfully! All required columns are present.")
                
                st.write("Processing the file and displaying results...")  # Placeholder for further processing
                print('from test2',df)
                df = master(df)
                print(df)
                st.session_state.df = df
                st.switch_page("pages/dashboardtesting.py")
                
        else:
            st.error("Please upload a CSV file before submitting.")

# Footer note for required columns
st.markdown("<p class='footer-note'>Note: Mentioned columns must be in the data with same column name.</p>", unsafe_allow_html=True)

# End of main content container
st.markdown("</div>", unsafe_allow_html=True)
