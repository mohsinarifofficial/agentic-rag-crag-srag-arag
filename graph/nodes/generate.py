from typing import Any, Dict

from chains.generation import generation_chain

from state import State

def generate(state:State) -> Dict[str, Any]:
    print("Genearting")
    question=state["question"]
    content =state["documents"]
    generation = generation_chain.invoke({
        "context": content,
        "question": question 
    })

    return {
        "document": content, "generation": generation,
        "question": question
    }

