import inspect
import itertools
from types import FunctionType

from .database import DatabaseTools
from .news import NewsTools
from .yahoo import YahooFinanceTools
from .portfolio import PortfolioTools

TOOL_CATEGORIES = [NewsTools, DatabaseTools, YahooFinanceTools, PortfolioTools]


def get_static_methods(cls):
    static_methods = []
    for name, member in inspect.getmembers(cls):
        if isinstance(member, FunctionType) and member.tool_call_metadata:
            print("HERE", member.tool_call_metadata["function"]["name"], member)
            static_methods.append(
                {member.tool_call_metadata["function"]["name"]: member}
            )
    return static_methods


AVAILABLE_TOOLS = {}
for l in [get_static_methods(c) for c in TOOL_CATEGORIES]:
    for d in l:
        AVAILABLE_TOOLS.update(d)

OPENAI_TOOL_CALLS = [tool.tool_call_metadata for tool in AVAILABLE_TOOLS.values()]
