import json
import streamlit as st
from openai import OpenAI
from tools import AVAILABLE_TOOLS, OPENAI_TOOL_CALLS
from transformers import GPT2Tokenizer
import matplotlib.pyplot as plt

MESSAGE_SESSION = "message_session"
MODEL = "gpt-4"  # Ensure this is the correct model that supports 8192 tokens
TOKEN_LIMIT = 8192  # Updated token limit based on the model's context length


class ChatRole:
    ASSISTANT = "assistant"
    USER = "user"
    TOOL = "tool"


class OpenAIClientWrapper:
    def __init__(self, api_key=None) -> None:
        self.client = OpenAI(api_key=api_key)
        self.tokenizer = GPT2Tokenizer.from_pretrained(
            "gpt2"
        )  # Using GPT-2 tokenizer for token counting
        if MESSAGE_SESSION not in st.session_state:
            st.session_state[MESSAGE_SESSION] = [
                {
                    "role": ChatRole.ASSISTANT,
                    "content": "Let me help you achieve Financial Independence & Retire Early",
                }
            ]

    def start_chat_session(self):
        self._display_all_messages()
        if prompt := st.chat_input():
            st.session_state["error_message"] = None  # Clear previous error message
            self._add_message(ChatRole.USER, prompt)
            with st.spinner("Processing..."):
                try:
                    msg = self._ask_openai()
                except Exception as e:
                    st.session_state["error_message"] = str(e)
                    msg = None
            if msg:
                self._add_message(ChatRole.ASSISTANT, msg)

    # -------------------------------- handlers --------------------------------
    def _ask_openai(self):
        tool_list = OPENAI_TOOL_CALLS
        print("_ask_openai", tool_list)
        self._truncate_messages_if_needed()
        response = self.client.chat.completions.create(
            model=MODEL,
            messages=[
                msg if isinstance(msg, dict) else msg.to_dict()
                for msg in st.session_state[MESSAGE_SESSION]
            ],
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
            with st.spinner("Using tools..."):
                tool_response = self._ask_openai_to_use_tool(tool_calls)
            return tool_response.choices[0].message.content

    def _ask_openai_to_use_tool(self, tool_calls):
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
        self._truncate_messages_if_needed()
        tool_response = self.client.chat.completions.create(
            model=MODEL,
            messages=[
                msg if isinstance(msg, dict) else msg.to_dict()
                for msg in st.session_state[MESSAGE_SESSION]
            ],
        )
        print(tool_response)
        return tool_response

    def _truncate_messages_if_needed(self):
        while self._get_total_tokens() > TOKEN_LIMIT:
            # Remove the oldest user and assistant message pair
            for i, msg in enumerate(st.session_state[MESSAGE_SESSION]):
                if isinstance(msg, dict) and msg["role"] == ChatRole.USER:
                    del st.session_state[MESSAGE_SESSION][
                        i : i + 2
                    ]  # Remove both user and assistant messages
                    break

    def _get_total_tokens(self):
        total_tokens = 0
        for msg in st.session_state[MESSAGE_SESSION]:
            if isinstance(msg, dict):
                total_tokens += len(self.tokenizer.encode(msg["content"]))
        return total_tokens

    def _display_all_messages(self):
        for msg in st.session_state[MESSAGE_SESSION]:
            if isinstance(msg, dict) and (
                msg["role"] in [ChatRole.ASSISTANT, ChatRole.USER]
            ):
                self._display_message(msg["role"], msg["content"])

    def _add_message(self, role, content):
        st.session_state[MESSAGE_SESSION].append({"role": role, "content": content})
        self._display_message(role, content)

    def _display_message(self, role, content):
        if "$$" in content:
            st.chat_message(role).markdown(content)
        else:
            st.chat_message(role).write(content)

        # Check if content indicates a request to plot (for example, a specific keyword)
        if "PLOT_DIAGRAM" in content:
            self._plot_diagram()

    def _plot_diagram(self):
        # Example plot (you can customize this as needed)
        fig, ax = plt.subplots()
        ax.plot([0, 1, 2, 3], [10, 1, 4, 8])
        ax.set_title("Example Plot")
        st.pyplot(fig)
