# app.py
from flask import jsonify, request

from common import AbstractResource

from .openai_handler import call_gpt_api


# Flask-RESTful resource to handle GPT API requests
class OpenAI(AbstractResource):
    API_PREFIX = '/openai'

    def post(self):
        data = request.get_json()
        prompt = data.get('prompt')
        if not prompt:
            return jsonify({'error': 'Prompt is required'}), 400

        gpt_response = call_gpt_api(prompt)
        return jsonify(gpt_response)
