# app.py
from flask import jsonify, request

from config import RESOUCE

from .openai_handler import call_gpt_api


# Flask-RESTful resource to handle GPT API requests
class OpenAI(RESOUCE):
    OPENAI_API_PREFIX = '/openai'
    def post(self):
        data = request.get_json()
        prompt = data.get('prompt')
        if not prompt:
            return jsonify({'error': 'Prompt is required'}), 400

        gpt_response = call_gpt_api(prompt)
        return jsonify(gpt_response)
