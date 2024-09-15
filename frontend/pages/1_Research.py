import streamlit as st
from utils.sidebar import sidebar
import requests

if "prospect_name" not in st.session_state:
    st.session_state.prospect_name = ""
if "company_name" not in st.session_state:
    st.session_state.company_name = ""
if "additional_info" not in st.session_state:
    st.session_state.additional_info = ""
if "model_choice_human" not in st.session_state:
    st.session_state.model_choice_human = "⚡ Max"
if "temperature" not in st.session_state:
    st.session_state.temperature = 0.7
if "stream_toggle" not in st.session_state:
    st.session_state.stream_toggle = False

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
    # Set the session state to indicate research has been fetched
    st.session_state["research_done"] = True

    # Prepare the JSON data for the POST request
    payload = {
        "model": st.session_state.model_choice_human,
        "prospect_name": st.session_state.prospect_name,
        "company_name": st.session_state.company_name,
        "additional_information": st.session_state.additional_info,
        "additional_context": st.session_state.additional_info,
        "temperature": st.session_state.temperature,
        "streaming": st.session_state.stream_toggle,
    }

    # Send the POST request to the API endpoint
    try:
        response = requests.post(
            "http://localhost:8000/research-analysis", json=payload
        )

        # Check if the request was successful
        if response.status_code == 200:
            st.session_state["research_results"] = (
                response.json()
            )  # Store the research results in session state
        else:
            st.error(f"Error: {response.status_code} - {response.text}")
    except Exception as e:
        st.error(f"An error occurred: {e}")

# Display research results after button click
if st.session_state.get("research_done") and "research_results" in st.session_state:
    st.write("### Research Results")

    # Parse and display the research results from the API response
    research_data = st.session_state["research_results"]

    st.markdown(research_data)
