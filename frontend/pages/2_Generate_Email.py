import streamlit as st
from utils.sidebar import sidebar

sidebar()

st.title("Generate Personalized Email")

# Initialize session state for email draft info
if "additional_email_info" not in st.session_state:
    st.session_state.additional_email_info = ""

# Section for email drafting (persist using session state)
st.session_state.additional_email_info = st.text_area(
    "Provide additional context to personalize the email draft",
    st.session_state.additional_email_info,
    key="email_info",
)

# Button to draft personalized email
if st.button("Generate Email"):
    st.session_state["email_draft_done"] = True

# Display email draft after button click
if st.session_state.get("email_draft_done"):
    st.write("### Personalized Email Draft")
    personalized_draft = """
    Dear John Doe,

    I hope this email finds you well. I noticed that ABC Corp recently acquired XYZ Inc., 
    and I believe our AI-driven product catalog could help streamline your upcoming projects. 

    Best regards,  
    [Your Name]
    """
    st.markdown(personalized_draft)
