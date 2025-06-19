from langchain_core.tools import tool
from langchain_ollama import ChatOllama
from langchain_tavily import TavilySearch


@tool
def triple(number: float) -> float:
    """
    Use when you need to triple a number.
    """
    return float(number) * 3


tools = [TavilySearch(max_results=1), triple]

llm = ChatOllama(model="llama3.1:8b", temperature=0).bind_tools(tools)
