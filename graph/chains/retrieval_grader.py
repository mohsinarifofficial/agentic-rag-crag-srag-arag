from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel,Field
from langchain_groq import ChatGroq
import dotenv, os

dotenv.load_dotenv()

llm = ChatGroq(
        api_key=os.getenv("api_key"),
        model="meta-llama/llama-4-scout-17b-16e-instruct"
    )


class GradeDocument(BaseModel):
    """Binary score on relevance. Check for the relevant data  in the reponse """
    binary_score: str =Field(description="Documents are relevant to question, 'yes' or 'no'")

structured_llm_grader = llm.with_structured_output(GradeDocument)

system = """You are an expert document relevance grader. Your task is to evaluate whether a retrieved document is relevant to answering a user's question.

Evaluate the document based on:
1. Does the document contain information that directly relates to the question?
2. Does the document provide useful context or background that helps answer the question?
3. Is the document's topic and content aligned with what the user is asking about?

Return "yes" if the document is relevant and useful for answering the question.
Return "no" if the document is not relevant, off-topic, or doesn't contain information related to the question.

Be precise and objective in your evaluation."""

grade_prompt= ChatPromptTemplate(
    [
        ("system", system),
        ("human", "Retrieved document:\n\n{document}\n\nUser question: {question}")
    ]
)

retrieval_grader=grade_prompt | structured_llm_grader