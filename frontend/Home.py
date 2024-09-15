import streamlit as st
from utils.sidebar import sidebar
from utils.remove_existing_file import remove_existing_file
import os
import glob

# Set page configuration to wide mode
st.set_page_config(layout="wide")

# Initialize session state for prospect details if not already set
if "prospect_name" not in st.session_state:
    st.session_state.prospect_name = ""
if "company_name" not in st.session_state:
    st.session_state.company_name = ""
if "additional_info" not in st.session_state:
    st.session_state.additional_info = ""

if "product_catalog_present" not in st.session_state:
    st.session_state.product_catalog_present = False
if "email_template_present" not in st.session_state:
    st.session_state.email_template_present = False

if "sent_email" in st.session_state and st.session_state.sent_email:
    # Path to the directory
    data_dir = "../data"

    # Get a list of all .txt and .pdf files in the directory
    txt_files = glob.glob(os.path.join(data_dir, "*.txt"))
    pdf_files = glob.glob(os.path.join(data_dir, "*.pdf"))

    # Combine both lists
    files_to_remove = txt_files + pdf_files

    # Remove each file
    for file in files_to_remove:
        try:
            os.remove(file)
        except Exception as e:
            print(f"Error removing {file}: {e}")


# Title for the home page
st.title("Prospect Research and Email Personalization Tool")

# Main input section for prospect details and file uploads
st.header("Prospect Details")

# Columns to structure the layout (you can adjust the number of columns as needed)
col1, col2 = st.columns(2)

save_path = "../data"

# Ensure the directory exists
if not os.path.exists(save_path):
    os.makedirs(save_path)


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

with col2:
    st.header("File Uploads")

    # Product Catalog upload and saving
    product_catalog = st.file_uploader(
        "Upload Product Catalog (PDF/TXT)", type=["pdf", "txt"]
    )
    if product_catalog:
        # Remove any existing file with the same name (regardless of extension)
        remove_existing_file(save_path, product_catalog.name)

        # Save the uploaded file
        with open(os.path.join(save_path, product_catalog.name), "wb") as f:
            f.write(product_catalog.getbuffer())

        st.session_state.product_catalog_present = True
        st.success(
            f"Product catalog saved to {os.path.join(save_path, product_catalog.name)}"
        )

    # Email Template upload and saving
    email_template = st.file_uploader(
        "Upload Sales Email Template / Winning Emails (PDF/TXT)", type=["pdf", "txt"]
    )
    if email_template:
        # Remove any existing file with the same name (regardless of extension)
        remove_existing_file(save_path, email_template.name)

        # Save the uploaded file
        with open(os.path.join(save_path, email_template.name), "wb") as f:
            f.write(email_template.getbuffer())
        st.session_state.email_template_present = True
        st.success(
            f"Email template saved to {os.path.join(save_path, email_template.name)}"
        )

# Summary or next step instructions
st.write(
    """
After entering the prospect details and uploading the necessary files, navigate through the pages in the sidebar
to perform research, generate a personalized email, and review the optimized email.
"""
)
