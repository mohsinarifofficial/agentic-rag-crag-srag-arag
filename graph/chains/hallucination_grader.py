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


system = """You are an expert fact-checking grader. Your task is to evaluate whether an LLM-generated answer is factually grounded in the provided source documents and free from hallucinations.

A hallucination occurs when the answer contains:
- Information not present in the source documents
- Claims that contradict the source documents
- Fabricated facts, numbers, or details
- Inferences that go beyond what the documents support
- Claims about topics not covered in the documents

Evaluate carefully:
1. Can all claims in the answer be traced back to the provided source documents?
2. Does the answer only state information that is explicitly or reasonably inferred from the documents?
3. Are there any unsupported claims or made-up information?

Return "yes" if the answer is fully grounded in the facts from the source documents with no hallucinations.
Return "no" if the answer contains any information not supported by the source documents or contradicts them.

Be strict: only return "yes" if the entire answer is factually supported by the provided documents."""

hallucination_prompt= ChatPromptTemplate([
    ("system",system),
    ("human", "Source Documents:\n\n{document}\n\nLLM Generation: {generation}")

])

hallucination_grader:RunnableSequence = hallucination_prompt | structured_llm_grader