import itertools
import inspect
from types import FunctionType

from utils import get_server_database_schema
from .news import NewsTools
from .database import DatabaseTools

TOOL_CATEGORIES = [NewsTools, DatabaseTools]


def get_static_methods(cls):
    static_methods = []
    for name, member in inspect.getmembers(cls):
        if isinstance(member, FunctionType):
            static_methods.append((cls.__name__ + "_" + name, member))
    return static_methods


AVAILABLE_TOOLS = dict(
    itertools.chain(*[get_static_methods(c) for c in TOOL_CATEGORIES])
)


def get_tool_list():
    tool_list = [
        {
            "type": "function",
            "function": {
                "name": "NewsTools_get_current_weather",
                "description": "Get the current weather in a given location",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "location": {
                            "type": "string",
                            "description": "The city and state, e.g. San Francisco, CA",
                        },
                        "unit": {
                            "type": "string",
                            "enum": ["celsius", "fahrenheit"],
                        },
                    },
                    "required": ["location"],
                },
            },
        },
        # {
        #     "type": "function",
        #     "function": {
        #         "name": "DatabaseTools_query_from_database",
        #         "description": "Get information regarding user's portfolio, positions, stocks, or the return of the portfolio of their own account.",
        #         "parameters": {
        #             "type": "object",
        #             "properties": {
        #                 "prompt": {
        #                     "type": "string",
        #                     "description": "The entire original prompt sent by the user.",
        #                 }
        #             },
        #             "required": ["prompt"],
        #         },
        #     },
        # },
        {
            "type": "function",
            "function": {
                "name": "DatabaseTools_query_from_database",
                "description": "Use this function to answer user questions about user's portfolio, positions, stocks, or the return of the portfolio of their own account in sqlite database. Input should be a fully formed SQL query.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "query": {
                            "type": "string",
                            "description": f"""
                                    SQL query extracting info to answer the user's question.
                                    SQL should be written using this database schema:
                                    {get_server_database_schema()}
                                    The query should be returned in plain text, not in JSON.
                                    """,
                        }
                    },
                    "required": ["query"],
                },
            },
        },
    ]
    return tool_list
