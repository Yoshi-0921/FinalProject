import json

import streamlit as st
from openai import OpenAI
from tools import AVAILABLE_TOOLS, OPENAI_TOOL_CALLS

MESSAGE_SESSION = "message_session"
MODEL = "gpt-4o"


class ChatRole:
    ASSISTANT = "assistant"
    USER = "user"
    TOOL = "tool"


class OpenAIClientWrapper:
    def __init__(self, api_key=None) -> None:
        self.client = OpenAI(api_key=api_key)
        if MESSAGE_SESSION not in st.session_state:
            st.session_state[MESSAGE_SESSION] = [
                {
                    "role": ChatRole.ASSISTANT,
                    "content": "Let me help you achieve Financial Indepent & Retire Early",
                }
            ]

    def start_chat_session(self):
        self._display_all_messages()
        if prompt := st.chat_input():
            self._add_message(ChatRole.USER, prompt)
            msg = self._ask_openai()
            self._add_message(ChatRole.ASSISTANT, msg)

    # -------------------------------- handlers --------------------------------
    def _ask_openai(self):
        tool_list = OPENAI_TOOL_CALLS
        print("_ask_openai", tool_list)
        response = self.client.chat.completions.create(
            model=MODEL,
            messages=st.session_state[MESSAGE_SESSION],
            tools=tool_list,
            tool_choice="auto",
        )

        print("response here")
        print(response)
        response_message = response.choices[0].message
        tool_calls = response_message.tool_calls
        if not tool_calls:
            print("NO TOOL CALL")
            return response_message.content
        else:
            print("USE TOOL CALL")
            st.session_state[MESSAGE_SESSION].append(response_message)
            tool_response = self._ask_openai_to_use_tool(tool_calls)
            return tool_response.choices[0].message.content

    def _ask_openai_to_use_tool(self, tool_calls):
        # TODO: 1. modify backend query
        # TODO: 2. add loading effect
        for tool_call in tool_calls:
            function_name = tool_call.function.name
            function_to_call = AVAILABLE_TOOLS[function_name]
            function_args = json.loads(tool_call.function.arguments)
            function_response = function_to_call(**function_args)
            print(
                "FUNCTION RESPONSE",
                function_response,
                isinstance(function_response, str),
            )
            st.session_state[MESSAGE_SESSION].append(
                {
                    "tool_call_id": tool_call.id,
                    "role": ChatRole.TOOL,
                    "name": function_name,
                    "content": str(function_response),
                }
            )

        print(st.session_state[MESSAGE_SESSION])
        tool_response = self.client.chat.completions.create(
            model=MODEL,
            messages=st.session_state[MESSAGE_SESSION],
        )
        print(tool_response)
        return tool_response

    def _display_all_messages(self):
        for msg in st.session_state[MESSAGE_SESSION]:
            if isinstance(msg, dict) and (
                msg["role"] in [ChatRole.ASSISTANT, ChatRole.USER]
            ):
                st.chat_message(msg["role"]).write(msg["content"])

    def _add_message(self, role, content):
        st.session_state[MESSAGE_SESSION].append({"role": role, "content": content})
        st.chat_message(role).write(content)
