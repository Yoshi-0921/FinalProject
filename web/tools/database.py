import json

import requests


class DatabaseTools:
    @staticmethod
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
