from langchain_classic import hub
from langchain_groq import ChatGroq
from langchain_core.output_parsers import StrOutputParser
import dotenv,os

dotenv.load_dotenv()

llm = ChatGroq(
        api_key=os.getenv("api_key"),
        model="meta-llama/llama-4-scout-17b-16e-instruct"
    )

prompt=hub.pull("rlm/rag-prompt")


generation_chain = prompt | llm | StrOutputParser()


