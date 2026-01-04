from typing import  Any, Dict
from chains.retrieval_grader import retrieval_grader
from state import State


def grade_document(state:State) -> Dict[str, Any]:
    print("We are checking the relevence tof the doicuent")
    question = state["question"]
    doc=state["documents"]
    filtered_doc=[]
    web_search=False
    score=retrieval_grader.invoke(
        {
            "question": question,
            "document" : doc
        }
    )
    
    if score.binary_score.lower()=="no":
        web_search = True
    
    return {"web_search": web_search}




        

    
