# Agentic RAG - Code Structure

## Directory Tree Structure

```
agentic_RAG/
│
├── __pycache__/                          # Python bytecode cache (auto-generated)
│
├── chroma_index/                         # ChromaDB vector store persistence directory
│   ├── a47ba61e-dd09-4097-8d7f-024ccb7b11c1/
│   │   ├── data_level0.bin
│   │   ├── header.bin
│   │   ├── index_metadata.pickle
│   │   ├── length.bin
│   │   └── link_lists.bin
│   └── chroma.sqlite3
│
├── main.py                               # Main entry point (currently imports node functions)
│
├── ingestion.py                          # Document ingestion script - loads web docs, splits, creates vector store
│                                          # Creates ChromaDB retriever and exports 'retriever' object
│
└── graph/                                # Main graph package
    │
    ├── __init__.py                       # Package initializer (currently empty comment)
    ├── __pycache__/                      # Python bytecode cache
    │
    ├── consts.py                         # Constants: RETRIEVE, GRADE_DOCUMENTS, GENERATE, WEBSEARCH
    │
    ├── state.py                          # State definition: State TypedDict class
    │                                     # Fields: question, generation, web_search, documents
    │
    ├── graph_work_flow.py                # Main graph workflow definition
    │                                     # - Defines StateGraph with nodes and edges
    │                                     # - Contains decide_to_generate routing function
    │                                     # - Compiles and exports 'app'
    │
    ├── chains/                           # LangChain chains package
    │   │
    │   ├── __init__.py                   # Package initializer (currently empty comment)
    │   ├── __pycache__/                  # Python bytecode cache
    │   │
    │   ├── generation.py                 # Generation chain: prompt | llm | StrOutputParser
    │   │                                 # - Uses langchain_classic.hub.pull("rlm/rag-prompt")
    │   │                                 # - Exports 'generation_chain'
    │   │
    │   ├── retrieval_grader.py           # Retrieval grader chain
    │   │                                 # - Defines GradeDocument Pydantic model
    │   │                                 # - Creates structured LLM grader
    │   │                                 # - Exports 'retrieval_grader' chain
    │   │
    │   └── tests/                        # Tests package
    │       │
    │       ├── __init__.py               # Package initializer
    │       ├── __pycache__/              # Python bytecode cache
    │       │
    │       └── test_chains.py            # Unit tests for chains
    │                                     # - test_retrieval_grade_answer_yes_or_no
    │                                     # - test_generation_agent
    │
    └── nodes/                            # Graph nodes package
        │
        ├── __pycache__/                  # Python bytecode cache
        │
        ├── retrieve.py                   # Retrieve node: fetches documents from vector store
        │                                 # - Uses 'retriever' from ingestion module
        │                                 # - Function: retrieve(state) -> Dict[str, Any]
        │                                 # - Returns: {"documents": documents}
        │
        ├── grade_document.py             # Grade document node: evaluates document relevance
        │                                 # - Uses retrieval_grader chain
        │                                 # - Function: grade_document(state)
        │                                 # - Sets web_search flag based on score
        │
        ├── generate.py                   # Generate node: creates final answer
        │                                 # - Uses generation_chain
        │                                 # - Function: generate(state) -> Dict[str, Any]
        │                                 # - Returns: {"document", "generation", "question"}
        │
        └── web_search.py                 # Web search node: searches web if docs insufficient
        │                                 # - Uses TavilySearch tool
        │                                 # - Function: web_search(state)
        │                                 # - Appends web results to documents
        │
        └── [NOTE: No __init__.py in nodes/ - imports are direct from module files]
```

## Import Relationships

### External Dependencies
- **langgraph**: Graph workflow framework
- **langchain_classic**: LangChain classic chains and prompts
- **langchain_groq**: Groq LLM provider
- **langchain_chroma**: ChromaDB vector store
- **langchain_pinecone**: Pinecone embeddings
- **langchain_tavily**: Tavily web search tool
- **pydantic**: Data validation (for GradeDocument model)

### Internal Import Patterns

#### Absolute Imports (from graph package root)
```python
from graph.consts import ...
from graph.state import State
from graph.nodes.xxx import ...
from graph.chains.xxx import ...
```

#### Module-level Imports (sibling modules)
```python
from ingestion import retriever  # From agentic_RAG root
```

## Graph Workflow Flow

```
START
  │
  ▼
RETRIEVE (retrieve node)
  │
  ▼
GRADE_DOCUMENTS (grade_document node)
  │
  ├─[web_search == True]──► WEBSEARCH (web_search node) ──► GENERATE (generate node) ──► END
  │
  └─[web_search == False]──► GENERATE (generate node) ──► END
```

## Key Files Description

### Root Level
- **main.py**: Entry point (currently just imports - may need implementation)
- **ingestion.py**: Data ingestion pipeline - loads documents, creates embeddings, stores in ChromaDB

### Graph Package
- **consts.py**: Node name constants
- **state.py**: State schema definition (TypedDict)
- **graph_work_flow.py**: Main workflow orchestration

### Chains Package
- **generation.py**: LLM chain for answer generation
- **retrieval_grader.py**: LLM chain for document relevance grading

### Nodes Package
- **retrieve.py**: Retrieval from vector store
- **grade_document.py**: Document relevance evaluation
- **generate.py**: Final answer generation
- **web_search.py**: Web search fallback

### Tests
- **test_chains.py**: Unit tests for chain functionality

## Data Flow

1. **Ingestion**: Documents → Split → Embed → Store in ChromaDB
2. **Retrieve**: Question → Vector Search → Documents
3. **Grade**: Question + Documents → LLM Grader → Relevance Score
4. **Route**: Score → Decision → WebSearch (if needed) or Generate
5. **Generate**: Question + Documents → LLM → Final Answer

