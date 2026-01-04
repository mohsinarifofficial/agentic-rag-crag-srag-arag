import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from consts import RETRIEVE, GRADE_DOCUMENTS, GENERATE, WEBSEARCH, GRADE_HALLUCINATION
from nodes.generate import generate
from nodes.grade_document import grade_document
from nodes.grade_hallucination import grade_hallucination
from nodes.retrieve import retrieve
from nodes.web_search import web_search
from state import State
from langgraph.graph import StateGraph, END


def decide_to_generate(state: State):
    print("Checking document relevance")
    if state.get("web_search", False):
        print("Documents not relevant, performing web search")
        return WEBSEARCH
    else:
        print("Documents are relevant, proceeding to generation")
        return GENERATE


workflow = StateGraph(State)

workflow.add_node(RETRIEVE, retrieve)
workflow.add_node(GRADE_DOCUMENTS, grade_document)
workflow.add_node(GENERATE, generate)
workflow.add_node(WEBSEARCH, web_search)
workflow.add_node(GRADE_HALLUCINATION, grade_hallucination)

workflow.set_entry_point(RETRIEVE)
workflow.add_edge(RETRIEVE, GRADE_DOCUMENTS)
workflow.add_conditional_edges(
    GRADE_DOCUMENTS,
    decide_to_generate,
    {
        WEBSEARCH: WEBSEARCH,
        GENERATE: GENERATE,
    },
)
workflow.add_edge(WEBSEARCH, GENERATE)
workflow.add_edge(GENERATE, GRADE_HALLUCINATION)
workflow.add_edge(GRADE_HALLUCINATION, END)

app = workflow.compile()

app.get_graph().draw_mermaid_png(output_file_path="graph.png")