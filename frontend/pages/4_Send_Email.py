import streamlit as st
import requests
import os
import glob
from utils.sidebar import sidebar

sidebar()

st.title("Send Email")

# Initialize session state for email details if not already set
if "user_email" not in st.session_state:
    st.session_state.user_email = ""
if "app_password" not in st.session_state:
    st.session_state.app_password = ""
if "recipient_email" not in st.session_state:
    st.session_state.recipient_email = ""
if "email_subject" not in st.session_state:
    st.session_state.email_subject = ""
if "sent_email" not in st.session_state:
    st.session_state.sent_email = False

# Input fields for sending email
st.session_state.user_email = st.text_input("Your Email", st.session_state.user_email)
st.session_state.app_password = st.text_input(
    "App Password", st.session_state.app_password, type="password"
)
st.session_state.recipient_email = st.text_input(
    "Recipient Email", st.session_state.recipient_email
)
st.session_state.email_subject = st.text_input(
    "Subject", st.session_state.email_subject
)

# Button to send the email with a unique key
if st.button(
    "Send Email",
    key="send_email_button",
    disabled=not (
        "email_draft_done" in st.session_state
        and st.session_state["email_draft_done"]
        and "email_optimized_done" in st.session_state
        and st.session_state["email_optimized_done"]
    ),
):
    if all(
        [
            st.session_state.user_email,
            st.session_state.app_password,
            st.session_state.recipient_email,
            st.session_state.email_subject,
        ]
    ):
        # Prepare the payload to send to the backend
        payload = {
            "to_email": st.session_state.recipient_email,
            "subject": st.session_state.email_subject,
            "gmail_user": st.session_state.user_email,
            "app_password": st.session_state.app_password,
        }

        # Send a POST request to the backend
        try:
            response = requests.post(
                "http://localhost:8000/send-email", json=payload
            )  # Update with your actual backend URL if different

            # Check if the response is successful
            if response.status_code == 200:
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
                st.success(
                    f"Email sent successfully to {st.session_state.recipient_email}!"
                )
                st.session_state.sent_email = True
            else:
                st.error(
                    f"Failed to send email. Error: {response.json().get('detail', 'Unknown error')}"
                )

        except requests.exceptions.RequestException as e:
            st.error(f"An error occurred while sending the email: {e}")
    else:
        st.error("Please fill in all fields before sending.")
