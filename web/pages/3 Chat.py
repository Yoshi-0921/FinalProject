import sys
import streamlit as st
from openai import OpenAI

print(sys.version)

openai_api_key = None

st.markdown(
    """
    <style>
    .css-1n76uvr {
        display: flex;
        align-items: flex-end;
    }
    .css-1n76uvr > div:first-child {
        flex-grow: 1;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

if not openai_api_key:
    col1, col2 = st.columns([3, 1])
    with col1:
        openai_api_key = st.text_input(
            label="**OpenAI API Key**",
            key="chatbot_api_key",
            type="password",
        )
    with col2:
        st.button("Submit")
    st.markdown(
        "```Please add your OpenAI API key to continue. And your own key without Jerry's credit card please.```"
    )

else:
    if "messages" not in st.session_state:
        st.session_state["messages"] = [
            {
                "role": "assistant",
                "content": "Let me help you achieve Financial Indepent & Retire Early",
            }
        ]

    for msg in st.session_state.messages:
        st.chat_message(msg["role"]).write(msg["content"])

    if prompt := st.chat_input():

        client = OpenAI(api_key=openai_api_key)
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.chat_message("user").write(prompt)
        response = client.chat.completions.create(
            model="gpt-3.5-turbo", messages=st.session_state.messages
        )
        msg = response.choices[0].message.content
        st.session_state.messages.append({"role": "assistant", "content": msg})
        st.chat_message("assistant").write(msg)
