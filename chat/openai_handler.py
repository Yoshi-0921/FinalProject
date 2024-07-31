import requests


GPT_API_KEY = 'your_gpt_api_key_here'

# Function to connect to GPT API
def call_gpt_api(prompt):
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {GPT_API_KEY}',
    }

    data = {
        'model': 'gpt-4',  # Replace with the appropriate model name if necessary
        'messages': [
            {'role': 'system', 'content': 'You are a helpful assistant.'},
            {'role': 'user', 'content': prompt},
        ],
        'max_tokens': 1000,  # Adjust the max tokens as needed
    }

    response = requests.post('https://api.openai.com/v1/chat/completions', headers=headers, json=data)
    return response.json()