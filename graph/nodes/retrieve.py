from typing import Any, Dict
import sys
from pathlib import Path

# Add parent directories to path to find ingestion.py
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from state import State
from ingestion import retriever
def retrieve(state: State) -> Dict[str, Any]:
    """
    Retrieve the documents from the vector store
    """
    question=state["question"]
    documents=retriever.invoke(question)
    return {"documents": documents}
    


