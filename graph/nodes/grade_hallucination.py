from typing import Any, Dict

from chains.hallucination_grader import hallucination_grader
from state import State


def grade_hallucination(state: State) -> Dict[str, Any]:
    print("Checking for hallucinations in the generated answer")
    question = state["question"]
    documents = state["documents"]
    generation = state["generation"]
    
    documents_text = "\n\n".join([str(doc) for doc in documents]) if documents else ""
    
    score = hallucination_grader.invoke(
        {
            "document": documents_text,
            "generation": generation
        }
    )
    
    is_grounded = score.binary_Score
    
    print(f"Hallucination check: {'Grounded (no hallucinations)' if is_grounded else 'Hallucinations detected'}")
    
    return {"is_grounded": is_grounded}

