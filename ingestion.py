from langchain_classic.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import WebBaseLoader
from langchain_chroma import Chroma
from langchain_pinecone import PineconeEmbeddings
from langchain_groq import ChatGroq

import dotenv,os

dotenv.load_dotenv()


urls=[ "https://lilianweng.github.io/posts/2023-06-23-agent/",
    "https://lilianweng.github.io/posts/2023-03-15-prompt-engineering/",
    "https://lilianweng.github.io/posts/2023-10-25-adv-attack-llm/",]
doc =[WebBaseLoader(url).load() for url in urls]

doc_list=[item for sublist in doc for item in sublist]

text_splitter=RecursiveCharacterTextSplitter.from_tiktoken_encoder(chunk_size=250, chunk_overlap=0)
doc_split=text_splitter.split_documents(doc_list)
embeddings=PineconeEmbeddings(model="llama-text-embed-v2",pinecone_api_key=os.getenv("PINECONE_API_KEY"))

vector_store=Chroma.from_documents(documents=doc_split,embedding=embeddings,collection_name="agentic_rag",persist_directory="chroma_index")
retriever=Chroma(
    collection_name="agentic_rag",
    embedding_function=embeddings,
    persist_directory="chroma_index"
).as_retriever() 
print("Ingested")