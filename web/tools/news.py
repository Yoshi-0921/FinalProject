import json
import requests


def get_news(company):
    api_key = "YOUR_NEWS_API_KEY"
    url = f"https://newsapi.org/v2/everything?q={company}&apiKey={api_key}"
    response = requests.get(url)
    news_data = response.json()
    return {company: news_data["articles"]}


class NewsTools:
    @staticmethod
    def get_news_all(companies):
        news_data_list = [get_news(company) for company in companies]
        return json.dumps({"results": news_data_list})

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
