import streamlit as st


def sidebar():
    # Initialize session state for model, temperature, and streaming if not set
    if "model_choice_human" not in st.session_state:
        st.session_state.model_choice_human = "Max"
    if "temperature" not in st.session_state:
        st.session_state.temperature = 0.7
    if "stream_toggle" not in st.session_state:
        st.session_state.stream_toggle = False

    with st.sidebar:
        st.header("Actions")

        # Mapping of human-readable names to actual model identifiers
        model_mapping = {
            "Max": "llama3_groq",
            "Ava": "perplexity",
            "Sophia": "claude 3.5 sonnet",
        }

        # Dropdown menu to select models (persist using session state)
        st.session_state.model_choice_human = st.selectbox(
            "Select Model",
            options=list(model_mapping.keys()),  # Display human names with icons
            index=list(model_mapping.keys()).index(
                st.session_state.model_choice_human
            ),  # Default to previously selected model
        )

        # Slider (radar-like) widget for temperature control (persist using session state)
        st.session_state.temperature = st.slider(
            "Temperature Control",
            min_value=0.0,
            max_value=1.0,
            value=st.session_state.temperature,  # Default temperature value
            step=0.01,  # Step for fine-tuning
            help="Control randomness/creativity of the model",
        )

        # Checkbox to toggle streaming
        # st.session_state.stream_toggle = st.checkbox(
        # "Streaming", value=st.session_state.stream_toggle
        # )
