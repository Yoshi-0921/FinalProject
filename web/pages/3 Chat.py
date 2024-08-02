import sys

import streamlit as st
from chat import OpenAIClientWrapper
from config import OPENAI_API_KEY

# # Initialize session state if not already done
if "OPENAI_API_KEY" not in st.session_state:
    st.session_state["OPENAI_API_KEY"] = None


openai_api_key = OPENAI_API_KEY
if openai_api_key:
    st.session_state["OPENAI_API_KEY"] = openai_api_key


def set_api_key():
    st.session_state["OPENAI_API_KEY"] = openai_api_key


# TODO: DELETE DURIAN PLEASE
card_number = None
if "card_number" not in st.session_state:
    st.session_state["card_number"] = ""


def set_durian():
    st.session_state["card_number"] = card_number


# TODO: DELETE DURIAN PLEASE


# Input field and button for the API key
if not st.session_state["OPENAI_API_KEY"]:
    openai_api_key = st.text_input(
        label="**OpenAI API Key**",
        key="chatbot_api_key",
        type="password",
    )
    st.button("Submit", type="primary", on_click=set_api_key)
    st.markdown(
        "> Please add your OpenAI API key to continue. And your own key without Jerry's credit card please."
    )

# TODO: DELETE DURIAN PLEASE
elif not "DURIAN" in st.session_state["card_number"]:
    card_number = st.text_input(
        "Any card number that does not belong to Jerry", max_chars=20
    )
    st.button("PAY", type="primary", on_click=set_durian)
# TODO: DELETE DURIAN PLEASE
else:
    client = OpenAIClientWrapper(api_key=st.session_state["OPENAI_API_KEY"])
    client.start_chat_session()
