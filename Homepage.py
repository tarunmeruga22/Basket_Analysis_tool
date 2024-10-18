import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
import base64
import pandas as pd
from logic import master
import json

# Load credentials from Streamlit secrets
credentials_info = json.loads(st.secrets["google_credentials"]["GOOGLE_SHEET_CREDENTIALS_JSON"])

# Authenticate using the credentials
creds = Credentials.from_service_account_info(credentials_info, scopes=['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive'])

# Authorize and open the Google Sheet
client = gspread.authorize(creds)
sheet = client.open('Basket_Analysis_leads').sheet1

# Set page configuration with the sidebar collapsed by default
st.set_page_config(page_title="Leverage Your Sales", page_icon="🛒", layout="wide", initial_sidebar_state="collapsed")

# Load the background image
image_path = "256013152_06ded2be-68c1-4023-ab8c-0783ccfb952c.jpg"
with open(image_path, "rb") as image_file:
    encoded_image = base64.b64encode(image_file.read()).decode()

# Sample CSV data for download
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
    .stApp {{
        background-image: url(data:image/png;base64,{encoded_image});
        background-size: cover;
        background-position: center;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }}
    .stAppHeader {{
        background-color: transparent !important;
    }}
    .content-container {{
        text-align: center;
        color: #aed6f1;
        padding: 80px 10px;
    }}
    .header-title {{
        font-size: 6.5em;
        font-weight: bold;
        color: #aed6f1;
        background: linear-gradient(to right,#5dade2, #d2b4de );
        -webkit-background-clip: text;
        color: transparent;
        margin-top:-20px; 
    }}
    .description-text {{
        font-size: 1.5em;
        font-weight: normal;
        color: #36454F;
        letter-spacing: 0.03em;
        margin-top: -18px;
    }}
    .description-Para {{
        font-size: 1em;
        font-weight: italic;
        color: #36454F;
        letter-spacing: 0.1em;
        width: 950px; 
        text-align: left;
        margin-top: 20px;
    }}
    .stFileUploader > label {{
        display: flex;
        justify-content: center;
        margin-top: -20px;
    }}
    .stFileUploader {{
        width: 380px;
    }}
    .file-upload-instructions {{
        margin-top: 25px;
        font-size: 1.3em;
        font-weight: bold;
        color: #36454F;
        opacity: 0.8;
    }}
    .sample-data-link {{
        color: #FF8096;
        text-decoration: underline;
        font-size: 1em;
        cursor: pointer;
    }}

    .email-input-label {{
        font-size: 1.3em;
        color: #36454F;
        font-weight: bold;
        margin-top : 40px;
        opacity: 0.8;
    }}
    .stTextInput {{
        width: 480px; /* Set the width for the email input field */
        margin-top : -20px;
        
    }}
    .sttext_input > label {{ 
        display: flex;
        justify-content: center;
        width: 480px;
        color: #36454F;
    }}


    </style>
""", unsafe_allow_html=True)

# Main Content
st.markdown("<div class='content-container'>", unsafe_allow_html=True)

# Display header title
st.markdown("<h1 class='header-title'>Basket Analysis</h1>", unsafe_allow_html=True)

# Description text under the title
st.markdown("<div class='description-text'>Identify frequently purchased product combinations from your Sales.</div>", unsafe_allow_html=True)

st.markdown('''<div class='description-Para'>Basket analysis is crucial for Direct-to-Consumer (D2C)
             brands because it identifies product combinations that are frequently purchased together. 
            By analyzing these patterns, brands can uncover valuable insights into customer behavior, 
            leading to more effective cross-selling, upselling, and personalized shopping experiences.</div>''', unsafe_allow_html=True)

# Email Input Field
st.markdown("<div class='email-input-label'>Enter your email address</div>", unsafe_allow_html=True)
email = st.text_input("", key="email_input", placeholder="your.email@example.com")


# Save email if entered
if email:
    # Save the email to the Google Sheet
    sheet.append_row([email])
    st.success("Success")

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
                df = master(df)
            
                st.session_state.df = df
                st.switch_page("pages/Dashboard.py")
                
        else:
            st.error("Please upload a CSV file before submitting.")

# Footer note for required columns
st.markdown("<p class='footer-note'>Note : All columns mentioned in the sample data must be present with the same name.</p>", unsafe_allow_html=True)

# End of main content container
st.markdown("</div>", unsafe_allow_html=True)
