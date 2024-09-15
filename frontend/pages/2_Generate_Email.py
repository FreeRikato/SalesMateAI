import streamlit as st
from utils.sidebar import sidebar
import json
import requests

sidebar()

st.title("Generate Personalized Email")

# Initialize session state for email draft info
if "additional_email_info" not in st.session_state:
    st.session_state.additional_email_info = ""

if "product_catalog_present" not in st.session_state:
    st.session_state.product_catalog_present = False
if "generated_result" not in st.session_state:
    st.session_state.generated_result = ""

# Section for email drafting (persist using session state)
st.session_state.additional_email_info = st.text_area(
    "Provide additional context to personalize the email draft",
    st.session_state.additional_email_info,
    key="email_info",
)

# Button to draft personalized email
if st.button(
    "Generate Email",
    disabled=not (
        st.session_state.product_catalog_present
        and "research_done" in st.session_state
        and st.session_state["research_done"]
    ),
):
    try:
        url = "http://127.0.0.1:8000/generate-email"
        # Prepare the JSON data for the POST request
        payload = json.dumps(
            {
                "model": st.session_state.model_choice_human,
                "additional_context": st.session_state.additional_research_info,
                "temperature": st.session_state.temperature,
                "streaming": st.session_state.stream_toggle,
            }
        )
        headers = {"Content-Type": "application/json"}

        response = requests.request("POST", url, headers=headers, data=payload)

        # Check if the request was successful
        if response.status_code == 200:
            st.session_state["generated_result"] = (
                response  # Store the research results in session state (as a string)
            )
            st.session_state["email_draft_done"] = (
                True  # Indicate that research is done
            )
        else:
            st.error(f"Error: {response.status_code} - {response.text}")
    except Exception as e:
        st.error(f"An error occurred: {e}")
if st.session_state.get("email_draft_done") and st.session_state["generated_result"]:
    # Display research results after button click
    st.write("### Generation Results")

    # Parse and display the research results from the API response
    generated_data = st.session_state["generated_result"]

    # Display the string response
    st.markdown(generated_data.text)  # or use st.write(research_data) if preferred
