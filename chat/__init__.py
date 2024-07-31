# app.py
from flask import Flask, request, jsonify
from flask_restful import Resource
from .openai_handler import call_gpt_api

app = Flask(__name__)



# Flask-RESTful resource to handle GPT API requests
class OpenAI(Resource):
    def post(self):
        data = request.get_json()
        prompt = data.get('prompt')
        if not prompt:
            return jsonify({'error': 'Prompt is required'}), 400

        gpt_response = call_gpt_api(prompt)
        return jsonify(gpt_response)
