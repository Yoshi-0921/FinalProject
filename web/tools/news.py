import json
import requests
from config import NEWS_API_KEY
from utils import get_last_month_date, add_metadata


def get_news(company):
    url = f"https://newsapi.org/v2/everything?q={company}&from={get_last_month_date()}&sortBy=popularity&apiKey={NEWS_API_KEY}"
    response = requests.get(url)
    news_data = response.json()
    return {company: news_data["articles"][:5]}


CLASSNAME = "NewsTools"


class NewsTools:
    @staticmethod
    @add_metadata(
        {
            "type": "function",
            "function": {
                "name": f"{CLASSNAME}_get_news_all",
                "description": "Fetch news data for a list of companies.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "companies": {
                            "type": "array",
                            "items": {
                                "type": "string",
                                "description": "The name of a company",
                            },
                            "description": "A list of company names to fetch news for",
                        }
                    },
                    "required": ["companies"],
                },
            },
        }
    )
    def get_news_all(companies):
        news_data_list = [get_news(company) for company in companies]
        return json.dumps({"results": news_data_list})
