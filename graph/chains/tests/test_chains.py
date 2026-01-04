import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(project_root))

from graph.chains.retrieval_grader import GradeDocument, retrieval_grader
from graph.chains.generation import generation_chain
from graph.chains.hallucination_grader import hallucination_grader, GradeHallucination
from ingestion import retriever
from pprint import pprint


def test_retrieval_grade_answer_yes_or_no() -> None:
    question ="agent memory"
    docs= retriever.invoke(question)
    doc_txt= docs[1].page_content
    res: GradeDocument = retrieval_grader.invoke(
        {
            "question": question,
            "document": doc_txt
        }
    )

    assert res.binary_score=="yes"


def test_retrieval_grade_answer_yes_or_no() -> None:
    question ="agen memory"
    docs= retriever.invoke(question)
    doc_txt= docs[1].page_content
    res: GradeDocument = retrieval_grader.invoke(
        {
            "question": "How to make pizza",
            "document": doc_txt
        }
    )
    
    assert res.binary_score=="No"


def test_generation_agent() -> None:
    question ="agent memory"
    docs= retriever.invoke(question)
    generation = generation_chain.invoke( {
            "question": "How to make pizza",
            "context": docs
        })
    pprint(generation)    

def test_hallucination_grader() -> None:
    question ="agent memory"
    documents= retriever.invoke(question)
    generation = hallucination_grader.invoke( {
            "generation": "What is agenet memory",
            "document": documents
        })
    pprint(generation)  
