import yfinance as yf
import json
from utils import add_metadata


CLASSNAME = "YahooFinanceTools"


class YahooFinanceTools:
    @staticmethod
    @add_metadata(
        {
            "type": "function",
            "function": {
                "name": f"{CLASSNAME}_get_income_statement",
                "description": "Get the income statement for a given ticker symbol.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "ticker": {
                            "type": "string",
                            "description": "The ticker symbol of the company (e.g., 'AAPL' for Apple).",
                        }
                    },
                    "required": ["ticker"],
                },
            },
        }
    )
    def get_income_statement(ticker: str) -> dict:
        stock = yf.Ticker(ticker)
        return stock.financials.to_dict()

    @staticmethod
    @add_metadata(
        {
            "type": "function",
            "function": {
                "name": f"{CLASSNAME}_get_cash_flow",
                "description": "Get the cash flow statement for a given ticker symbol.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "ticker": {
                            "type": "string",
                            "description": "The ticker symbol of the company (e.g., 'AAPL' for Apple).",
                        }
                    },
                    "required": ["ticker"],
                },
            },
        }
    )
    def get_cash_flow(ticker: str) -> dict:
        stock = yf.Ticker(ticker)
        return stock.cashflow.to_dict()

    @staticmethod
    @add_metadata(
        {
            "type": "function",
            "function": {
                "name": f"{CLASSNAME}_get_balance_sheet",
                "description": "Get the balance sheet for a given ticker symbol.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "ticker": {
                            "type": "string",
                            "description": "The ticker symbol of the company (e.g., 'AAPL' for Apple).",
                        }
                    },
                    "required": ["ticker"],
                },
            },
        }
    )
    def get_balance_sheet(ticker: str) -> dict:
        stock = yf.Ticker(ticker)
        return stock.balance_sheet.to_dict()

    @staticmethod
    @add_metadata(
        {
            "type": "function",
            "function": {
                "name": f"{CLASSNAME}_get_financial_summary",
                "description": "Get a summary of financial data for a given ticker symbol.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "ticker": {
                            "type": "string",
                            "description": "The ticker symbol of the company (e.g., 'AAPL' for Apple).",
                        }
                    },
                    "required": ["ticker"],
                },
            },
        }
    )
    def get_financial_summary(ticker: str) -> dict:
        stock = yf.Ticker(ticker)
        return stock.info

    @staticmethod
    @add_metadata(
        {
            "type": "function",
            "function": {
                "name": f"{CLASSNAME}_get_all_financial_data",
                "description": "Get all financial data for a given ticker symbol, including the income statement, cash flow statement, balance sheet, and financial summary.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "ticker": {
                            "type": "string",
                            "description": "The ticker symbol of the company (e.g., 'AAPL' for Apple).",
                        }
                    },
                    "required": ["ticker"],
                },
            },
        }
    )
    def get_all_financial_data(ticker: str) -> dict:
        financial_data = {
            "income_statement": YahooFinanceTools.get_income_statement(ticker),
            "cash_flow": YahooFinanceTools.get_cash_flow(ticker),
            "balance_sheet": YahooFinanceTools.get_balance_sheet(ticker),
            "financial_summary": YahooFinanceTools.get_financial_summary(ticker),
        }
        return financial_data
