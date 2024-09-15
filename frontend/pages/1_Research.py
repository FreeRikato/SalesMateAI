import streamlit as st
from utils.sidebar import sidebar
import json
import requests

# Sidebar to select model, input, etc.
sidebar()

# Set default session state values
if "prospect_name" not in st.session_state:
    st.session_state.prospect_name = ""
if "company_name" not in st.session_state:
    st.session_state.company_name = ""
if "additional_info" not in st.session_state:
    st.session_state.additional_info = ""
if "model_choice_human" not in st.session_state:
    st.session_state.model_choice_human = "Max"
if "temperature" not in st.session_state:
    st.session_state.temperature = 0.7
if "stream_toggle" not in st.session_state:
    st.session_state.stream_toggle = False
if "research_results" not in st.session_state:
    st.session_state["research_results"] = (
        None  # Initialize session state for research results
    )
if "additional_research_info" not in st.session_state:
    st.session_state["additional_research_info"] = "Proceed with human message"
# Title of the app
st.title("Research Prospect and Company")

# Section for additional research info (persist using session state)
st.session_state.additional_research_info = st.text_area(
    "Provide additional context for research",
    st.session_state.additional_research_info,
    key="research_info",
)

# Button to fetch research data
if st.button(
    "Fetch Research Results",
    disabled=(
        st.session_state.prospect_name == "" or st.session_state.company_name == ""
    ),
):
    # Send the POST request to the API endpoint
    try:

        url = "http://127.0.0.1:8000/research-analysis"
        payload = json.dumps(
            {
                "model": st.session_state.model_choice_human,
                "prospect_name": st.session_state.prospect_name,
                "company_name": st.session_state.company_name,
                "additional_information": st.session_state.additional_info,
                "additional_context": st.session_state.additional_research_info,
                "temperature": st.session_state.temperature,
                "streaming": st.session_state.stream_toggle,
            }
        )
        headers = {"Content-Type": "application/json"}

        response = requests.request("POST", url, headers=headers, data=payload)

        # Check if the request was successful
        if response.status_code == 200:
            st.session_state["research_results"] = (
                response  # Store the research results in session state (as a string)
            )
            st.session_state["research_done"] = True  # Indicate that research is done
        else:
            st.error(f"Error: {response.status_code} - {response.text}")
    except Exception as e:
        st.error(f"An error occurred: {e}")

# Display research results after button click
if st.session_state.get("research_done") and st.session_state["research_results"]:
    st.write("### Research Results")

    # Parse and display the research results from the API response
    research_data = st.session_state["research_results"]

    # Display the string response
    st.markdown(research_data.text)  # or use st.write(research_data) if preferred
