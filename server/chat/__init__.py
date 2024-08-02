# app.py
import sqlite3
from flask import jsonify, request

from config import SQLITE_PATH
from common import AbstractResource
from .openai_handler import call_gpt_api
from .database_handler import *


class OpenAI(AbstractResource):
    END_POINTS = ["/openai"]

    def post(self):
        data = request.get_json()
        prompt = data.get("prompt")
        if not prompt:
            return jsonify({"error": "Prompt is required"}), 400
        gpt_response = call_gpt_api(prompt)
        return jsonify(gpt_response)


class OpenAIDatabaseSchema(AbstractResource):
    END_POINTS = ["/openai/database/schema"]

    def get(self):
        return jsonify({"schema": database_schema_dict})


class OpenAIDatabaseQuery(AbstractResource):
    END_POINTS = ["/openai/database/query"]

    def get(self):
        data = request.get_json()
        query = data.get("query")
        if not query:
            return jsonify({"error": "query is required"}), 400
        try:
            results = str(sqlite3.connect(SQLITE_PATH).execute(query).fetchall())
        except Exception as e:
            results = f"query failed with error: {e}"
        return jsonify({"results": results})
