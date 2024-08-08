import json
import requests
from utils import add_metadata

CLASSNAME = "PortfolioTools"
BASE_URL = "http://127.0.0.1:5000"  # Extracted base URL


# Utility function to handle API requests
def api_request(endpoint, method="GET", data=None):
    url = f"{BASE_URL}{endpoint}"
    headers = {"Content-Type": "application/json"}
    try:
        if method == "GET":
            response = requests.get(url, headers=headers, json=data)
        elif method == "POST":
            response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}


# Define the PortfolioTools class with metadata for each API endpoint
class PortfolioTools:

    @staticmethod
    @add_metadata(
        {
            "type": "function",
            "function": {
                "name": f"{CLASSNAME}_get_portfolio_returns",
                "description": "Fetch the portfolio returns for a given userid like weimeng.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "userid": {
                            "type": "string",
                            "description": "The user ID to fetch portfolio returns for.",
                        },
                    },
                    "required": ["userid"],
                },
            },
        }
    )
    def get_portfolio_returns(userid):
        endpoint = f"/returns/{userid}"
        return json.dumps(api_request(endpoint))

    @staticmethod
    @add_metadata(
        {
            "type": "function",
            "function": {
                "name": f"{CLASSNAME}_get_portfolio_shares",
                "description": "Fetch the shares for a given portfolio ID.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "portfolioid": {
                            "type": "string",
                            "description": "The portfolio ID to fetch shares for.",
                        },
                    },
                    "required": ["portfolioid"],
                },
            },
        }
    )
    def get_portfolio_shares(portfolioid):
        endpoint = f"/portfolios/{portfolioid}/shares"
        return json.dumps(api_request(endpoint))

    @staticmethod
    @add_metadata(
        {
            "type": "function",
            "function": {
                "name": f"{CLASSNAME}_get_gbm_parameters",
                "description": "Fetch the Geometric Brownian Motion parameters for a given portfolio ID.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "portfolioid": {
                            "type": "string",
                            "description": "The portfolio ID to fetch GBM parameters for.",
                        },
                    },
                    "required": ["portfolioid"],
                },
            },
        }
    )
    def get_gbm_parameters(portfolioid):
        endpoint = f"/portfolios/{portfolioid}/gbmparam"
        return json.dumps(api_request(endpoint))

    @staticmethod
    @add_metadata(
        {
            "type": "function",
            "function": {
                "name": f"{CLASSNAME}_get_gbm_histogram",
                "description": "Fetch the Geometric Brownian Motion histogram for a given portfolio ID.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "portfolioid": {
                            "type": "string",
                            "description": "The portfolio ID to fetch GBM histogram for.",
                        },
                    },
                    "required": ["portfolioid"],
                },
            },
        }
    )
    def get_gbm_histogram(portfolioid):
        endpoint = f"/portfolios/{portfolioid}/gbmhist"
        return json.dumps(api_request(endpoint))

    @staticmethod
    @add_metadata(
        {
            "type": "function",
            "function": {
                "name": f"{CLASSNAME}_get_portfolio",
                "description": "Fetch the portfolio for a given user ID.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "userid": {
                            "type": "string",
                            "description": "The user ID to fetch portfolio for.",
                        },
                    },
                    "required": ["userid"],
                },
            },
        }
    )
    def get_portfolio(userid):
        endpoint = f"/portfolios/{userid}"
        return json.dumps(api_request(endpoint))
