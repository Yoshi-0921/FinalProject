import json
import requests
from utils import add_metadata, get_server_database_schema


CLASSNAME = "DatabaseTools"
SCHEMA = get_server_database_schema()


DYNAMIC_QUERY = """
WITH
positions_data AS (
    SELECT symbol, shares
    FROM positions
    WHERE portfolio_id = ?
),
portfolio_sum AS (
    SELECT
        SUM(CASE
            WHEN stocks.symbol IN (SELECT symbol FROM positions_data) THEN stocks.open * (SELECT shares FROM positions_data WHERE positions_data.symbol = stocks.symbol)
            ELSE 0
        END) AS open,
        SUM(CASE
            WHEN stocks.symbol IN (SELECT symbol FROM positions_data) THEN stocks.close * (SELECT shares FROM positions_data WHERE positions_data.symbol = stocks.symbol)
            ELSE 0
        END) AS close
    FROM stocks
    JOIN positions_data ON stocks.symbol = positions_data.symbol
    WHERE stocks.unixtimestamp IS NOT NULL
    GROUP BY stocks.unixtimestamp
    ORDER BY stocks.unixtimestamp
),
portfolio_var AS (
    SELECT
        (portfolio_sum.close - portfolio_sum.open) / portfolio_sum.open AS var
    FROM portfolio_sum
)
SELECT
    AVG(var) AS average_variation,
    AVG(var * var) AS variance
FROM portfolio_var;

     """


class DatabaseTools:
    @staticmethod
    @add_metadata(
        {
            "type": "function",
            "function": {
                "name": f"{CLASSNAME}_query_from_database",
                "description": "Use this function to answer user questions about user's portfolio, positions, stocks, or the return of the portfolio of their own account in sqlite database. Input should be a fully formed SQL query.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "query": {
                            "type": "string",
                            "description": f"""
                                    SQL query extracting info to answer the user's question.
                                    SQL should be written using this database schema:
                                    {SCHEMA}
                                    The query should be returned in plain text, not in JSON. Give me dynamic query if necessary (when involing calculation etc).
                                    For example, calculation Geomatric Brownian Motion / Log normal distribution for the next 20 years (with 1 year interval) / Sharp Ratio etc.
                                    One example of the dynamic query is {DYNAMIC_QUERY}, for historical data needed for calculation you can retrieve from stocks table and positions table.
                                    """,
                        }
                    },
                    "required": ["query"],
                },
            },
        }
    )
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
