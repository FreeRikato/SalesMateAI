import streamlit as st
from utils.sidebar import sidebar

# Set page configuration to wide mode
st.set_page_config(layout="wide")

# Initialize session state for prospect details if not already set
if "prospect_name" not in st.session_state:
    st.session_state.prospect_name = ""
if "company_name" not in st.session_state:
    st.session_state.company_name = ""
if "additional_info" not in st.session_state:
    st.session_state.additional_info = ""

# Title for the home page
st.title("Prospect Research and Email Personalization Tool")

# Main input section for prospect details and file uploads
st.header("Prospect Details")

# Columns to structure the layout (you can adjust the number of columns as needed)
col1, col2 = st.columns(2)

# Prospect details input in the first column (persist using session state)
with col1:
    st.session_state.prospect_name = st.text_input(
        "Prospect Name", st.session_state.prospect_name
    )
    st.session_state.company_name = st.text_input(
        "Company Name", st.session_state.company_name
    )
    st.session_state.additional_info = st.text_area(
        "Additional Information", st.session_state.additional_info, height=150
    )

# File uploads in the second column
with col2:
    st.header("File Uploads")
    st.session_state.product_catalog = st.file_uploader(
        "Upload Product Catalog (PDF/TXT)", type=["pdf", "txt"]
    )
    st.session_state.email_template = st.file_uploader(
        "Upload Sales Email Template / Winning Emails (PDF/TXT)", type=["pdf", "txt"]
    )

# Summary or next step instructions
st.write(
    """
After entering the prospect details and uploading the necessary files, navigate through the pages in the sidebar
to perform research, generate a personalized email, and review the optimized email.
"""
)
