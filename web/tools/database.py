import json
import requests
from utils import add_metadata, get_server_database_schema


CLASSNAME = "DatabaseTools"
SCHEMA = get_server_database_schema()


class DatabaseTools:
    @staticmethod
    @add_metadata(
        {
            "type": "function",
            "function": {
                "name": f"{CLASSNAME}_query_from_database",
                "description": "Use this function to answer user questions about user's portfolio, positions, stocks, or the return of the portfolio of their own account in sqlite database. Input should be a fully formed SQL query.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "query": {
                            "type": "string",
                            "description": f"""
                                    SQL query extracting info to answer the user's question.
                                    SQL should be written using this database schema:
                                    {SCHEMA}
                                    The query should be returned in plain text, not in JSON.
                                    """,
                        }
                    },
                    "required": ["query"],
                },
            },
        }
    )
    def query_from_database(query):
        url = "http://127.0.0.1:5000/openai/database/query"
        headers = {"Content-Type": "application/json"}
        data = {"query": query}
        try:
            response = requests.get(url, headers=headers, json=data)
            response.raise_for_status()
            return json.dumps(response.json())
        except requests.exceptions.RequestException as e:
            return {"error": str(e)}
