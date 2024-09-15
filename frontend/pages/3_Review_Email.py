import streamlit as st
from utils.sidebar import sidebar
import json
import requests

sidebar()

st.title("Review and Optimize Email")

if "email_template_present" not in st.session_state:
    st.session_state.email_template_present = False
# Initialize session state for optimizing email
if "additional_optimization_info" not in st.session_state:
    st.session_state.additional_optimization_info = ""

# Section for optimizing email (persist using session state)
st.session_state.additional_optimization_info = st.text_area(
    "Provide feedback to optimize the email",
    st.session_state.additional_optimization_info,
    key="optimization_info",
)

if "optimised_result" not in st.session_state:
    st.session_state.optimised_result = ""

# Button to fetch optimized email
if st.button(
    "Fetch Optimized Email",
    disabled=not (
        st.session_state.email_template_present
        and "email_draft_done" in st.session_state
        and st.session_state["email_draft_done"]
    ),
):
    try:
        url = "http://127.0.0.1:8000/review-email"
        # Prepare the JSON data for the POST request
        payload = json.dumps(
            {
                "model": st.session_state.model_choice_human,
                "additional_context": st.session_state.additional_optimization_info,
                "temperature": st.session_state.temperature,
                "streaming": st.session_state.stream_toggle,
            }
        )
        headers = {"Content-Type": "application/json"}

        response = requests.request("POST", url, headers=headers, data=payload)

        # Check if the request was successful
        if response.status_code == 200:
            st.session_state["optimized_result"] = (
                response  # Store the research results in session state (as a string)
            )
            st.session_state["email_optimized_done"] = True
        else:
            st.error(f"Error: {response.status_code} - {response.text}")
    except Exception as e:
        st.error(f"An error occurred: {e}")

# Display optimized email after button click
if (
    st.session_state.get("email_optimized_done")
    and st.session_state["optimized_result"]
):

    optimized_result = st.session_state["optimized_result"]

    # Display the string response
    st.write(optimized_result.text)  # or use st.write(research_data) if preferred
