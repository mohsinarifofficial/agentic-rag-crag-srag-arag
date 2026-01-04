
from graph.graph_work_flow import app

if __name__=="__main__":
    print("Hello Advanced RAG")
    print(
        app.invoke(
            input={
                "question": "What is agent memory?"
            }
        )
    )
