import streamlit as st
from utils.sidebar import sidebar

sidebar()

st.title("Review and Optimize Email")

# Initialize session state for optimizing email
if "additional_optimization_info" not in st.session_state:
    st.session_state.additional_optimization_info = ""

# Section for optimizing email (persist using session state)
st.session_state.additional_optimization_info = st.text_area(
    "Provide feedback to optimize the email",
    st.session_state.additional_optimization_info,
    key="optimization_info",
)

# Button to fetch optimized email
if st.button("Fetch Optimized Email"):
    st.session_state["email_optimized_done"] = True

# Display optimized email after button click
if st.session_state.get("email_optimized_done"):
    st.write("### Optimized Email")
    optimized_email = """
    Dear John Doe,

    I would like to follow up on our previous conversation and provide more details 
    about our AI-driven solutions, which I believe would align perfectly with ABC Corp's 
    recent expansion into AI-driven products...

    Best regards,  
    [Your Name]
    """
    st.markdown(optimized_email)
