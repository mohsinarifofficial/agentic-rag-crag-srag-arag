from typing import Any, Dict

from langchain_classic.schema import Document
from langchain_tavily import TavilySearch

from graph.state import State


web_Search_tool= TavilySearch(max_results=3)


def web_search(state:State):
    print("Searching the web")
    question= state["question"]
    documents=state["documents"]
    tavily_results=web_Search_tool.invoke({"query": question})
    tavily_results_cleaned="".join(tavily_results["content"] for tv in tavily_results)
    results=Document(tavily_results_cleaned)
    if documents is not None:
        documents.append(results)
    else:
        documents=[results]





