import json

import requests


class NewsTools:
    def _get_news(company):
        api_key = "YOUR_NEWS_API_KEY"
        url = f"https://newsapi.org/v2/everything?q={company}&apiKey={api_key}"
        response = requests.get(url)
        news_data = response.json()
        return {company: news_data["articles"]}

    # @staticmethod
    # def get_news(companies):
    #     news_data_list =
    #     return json.dumps({"results": location, "temperature": "unknown"})

    @staticmethod
    def get_current_weather(location, unit="fahrenheit"):
        """Get the current weather in a given location"""
        if "tokyo" in location.lower():
            return json.dumps({"location": "Tokyo", "temperature": "10", "unit": unit})
        elif "san francisco" in location.lower():
            return json.dumps(
                {"location": "San Francisco", "temperature": "72", "unit": unit}
            )
        elif "paris" in location.lower():
            return json.dumps({"location": "Paris", "temperature": "22", "unit": unit})
        else:
            return json.dumps({"location": location, "temperature": "unknown"})
