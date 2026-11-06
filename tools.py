"""Tools the AI assistant can use. The LLM decides when to call them."""
from datetime import datetime

import requests
from langchain_core.tools import tool

HEADERS = {"User-Agent": "ai-assistant-with-langchain/1.0 (student project)"}


@tool
def get_current_time() -> str:
    """Get the current date and time. Use when the user asks about today's date or time."""
    return datetime.now().strftime("%A, %d %B %Y, %I:%M %p")


@tool
def calculator(expression: str) -> str:
    """Evaluate a math expression such as '12 * (3 + 4)'. Use for any calculation."""
    allowed = set("0123456789+-*/(). %")
    if not expression or not set(expression) <= allowed:
        return "Only numbers and + - * / ( ) . % are allowed."
    try:
        return str(eval(expression, {"__builtins__": {}}, {}))
    except Exception as e:
        return f"Could not calculate: {e}"


@tool
def wikipedia_search(query: str) -> str:
    """Look up factual information about a person, place, concept or event on Wikipedia."""
    try:
        search = requests.get(
            "https://en.wikipedia.org/w/api.php",
            params={"action": "query", "list": "search", "srsearch": query,
                    "format": "json", "srlimit": 1},
            headers=HEADERS, timeout=10,
        ).json()
        hits = search["query"]["search"]
        if not hits:
            return "No Wikipedia article found."
        title = hits[0]["title"]
        summary = requests.get(
            f"https://en.wikipedia.org/api/rest_v1/page/summary/{title.replace(' ', '_')}",
            headers=HEADERS, timeout=10,
        ).json()
        return f"{title}: {summary.get('extract', 'No summary available.')}"
    except Exception as e:
        return f"Wikipedia lookup failed: {e}"


TOOLS = [get_current_time, calculator, wikipedia_search]
