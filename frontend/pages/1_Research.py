import streamlit as st
from utils.sidebar import sidebar

sidebar()

st.title("Research Prospect and Company")

# Initialize session state for additional research info if not set
if "additional_research_info" not in st.session_state:
    st.session_state.additional_research_info = ""

# Section for additional research info (persist using session state)
st.session_state.additional_research_info = st.text_area(
    "Provide additional context for research",
    st.session_state.additional_research_info,
    key="research_info",
)

# Button to fetch research data
if st.button("Fetch Research Results"):
    st.session_state["research_done"] = True

# Display research results after button click
if st.session_state.get("research_done"):
    st.write("### Research Results")
    research_results = """
    **Name**: John Doe  
    **Company**: ABC Corp  
    **Industry**: Technology  
    **Recent News**: ABC Corp recently acquired XYZ Inc.  
    **Opportunities**: ABC Corp is expanding into AI-driven solutions.
    """
    st.markdown(research_results)
