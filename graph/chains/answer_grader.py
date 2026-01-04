from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableSequence
from langchain_groq import ChatGroq
from pydantic import BaseModel, Field
import dotenv, os

dotenv.load_dotenv()


llm = ChatGroq(
        api_key=os.getenv("api_key"),
        model="meta-llama/llama-4-scout-17b-16e-instruct"
    )

class GradeHallucination(BaseModel):
    binary_Score: bool = Field(description="Answer is grounded to the fact, yes or no"
    )

structured_llm_grader=llm.with_structured_output(GradeHallucination)


system = """You are an expert answer quality grader. Your task is to evaluate whether an LLM-generated answer adequately addresses and satisfies a user's question.

Evaluate the answer based on:
1. Does the answer directly address what the user asked?
2. Is the answer complete and comprehensive enough to satisfy the question?
3. Does the answer provide useful information that helps the user understand the topic?
4. Is the answer clear and well-structured?

Return "yes" if the answer fully meets the question's requirements and provides a satisfactory response.
Return "no" if the answer is incomplete, off-topic, doesn't address the question, or fails to meet the user's needs.

Be objective and focus on whether the answer fulfills what the question is asking for."""

hallucination_prompt= ChatPromptTemplate([
    ("system",system),
    ("human", "Question: {question}\n\nLLM Generation: {generation}")

])

hallucination_grader:RunnableSequence = hallucination_prompt | structured_llm_grader