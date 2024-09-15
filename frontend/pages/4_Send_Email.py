import streamlit as st
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
if st.button("Send Email", key="send_email_button"):
    if all(
        [
            st.session_state.user_email,
            st.session_state.app_password,
            st.session_state.recipient_email,
            st.session_state.email_subject,
        ]
    ):
        # Example of sending email logic (add your email logic here)
        st.success(f"Email sent successfully to {st.session_state.recipient_email}!")
    else:
        st.error("Please fill in all fields before sending.")
