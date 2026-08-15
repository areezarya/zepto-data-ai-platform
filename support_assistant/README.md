## Example API Calls

### Policy Question

Query:

What is the refund policy?

Response:

{
  "answer": "Based on the retrieved context: ...",
  "sources": ["doc_03_chunk_0"],
  "confidence": 1.0
}

### General Question

Query:

Who won the IPL final?

Response:

{
  "answer": "I can only answer questions about Zepto policies right now.",
  "sources": [],
  "confidence": 1.0
}

2. Architecture Overview

# Zepto Policy Support Assistant

## Architecture Overview

### High-Level Pipeline

```text
                ┌─────────────────┐
                │ Zepto Documents │
                │   (8 .txt files)│
                └────────┬────────┘
                         │
                         ▼
                ┌─────────────────┐
                │   Ingestion      │
                │  Chunk Documents │
                └────────┬────────┘
                         │
                         ▼
                ┌─────────────────┐
                │   Embedding      │
                │ all-MiniLM-L6-v2│
                └────────┬────────┘
                         │
                         ▼
                ┌─────────────────┐
                │    ChromaDB      │
                │ zepto_policies   │
                └────────┬────────┘
                         │
                         ▼
                ┌─────────────────┐
                │   LangGraph      │
                │ Intent Router    │
                └────────┬────────┘
                         │
          ┌──────────────┴──────────────┐
          ▼                             ▼
 ┌─────────────────┐          ┌─────────────────┐
 │ policy_question │          │ general_question│
 └────────┬────────┘          └────────┬────────┘
          ▼                             ▼
 ┌─────────────────┐          ┌─────────────────┐
 │ Retrieve Top-3  │          │ Direct Response │
 │ Chroma Chunks   │          └────────┬────────┘
 └────────┬────────┘                   │
          ▼                             ▼
 ┌─────────────────┐          ┌─────────────────┐
 │ Generate Answer │          │ Generate Answer │
 └────────┬────────┘          └────────┬────────┘
          ▼                             ▼
          └──────────► Final Response ◄─┘

  1. Ingestion Stage

The ingestion stage loads the eight Zepto policy documents stored in the docs/ directory. The ingestion script reads each document, splits it into fixed-size chunks, and prepares those chunks for embedding.

Components

Document loading and chunking logic in the ingestion script
Source documents stored in docs/

Output

Text chunks with associated metadata such as document ID and chunk number
2. Embedding Stage

Each document chunk is converted into a vector embedding using the Sentence Transformers model:

all-MiniLM-L6-v2

The model transforms each chunk into a dense semantic vector representation.

Components

SentenceTransformer
Model: all-MiniLM-L6-v2

Output

Embedding vector for every document chunk
3. Vector Storage Stage

The generated embeddings are stored in a ChromaDB collection named:

zepto_policies

Each record contains the chunk text, embedding vector, chunk ID, and metadata. This collection acts as the vector store for retrieval.

Components

ChromaDB
Collection: zepto_policies

Output

Persistent vector database containing all document embeddings
4. Retrieval Stage

For policy-related questions, the user query is embedded using the same all-MiniLM-L6-v2 model. The query embedding is then used to retrieve the top-3 most similar chunks from the ChromaDB collection using vector similarity search.

Components

LangGraph node: retrieve_and_answer
ChromaDB collection: zepto_policies

Output

Top-3 relevant chunks returned from the vector database
5. Generation Stage

After retrieval, the system generates the final response.

For policy questions, the retrieved context is used to create the answer. For general questions, retrieval is skipped and a direct response is returned.

Components

LangGraph node: retrieve_and_answer
LangGraph node: direct_answer
Structured prompt template in prompts.py

Output

Final answer returned through the FastAPI /ask endpoint
LangGraph Workflow

The application uses a LangGraph StateGraph with three nodes:

classify_intent

Determines whether the incoming query is a:

policy_question
general_question
retrieve_and_answer

Handles policy-related questions by:

Embedding the query
Retrieving the top-3 most relevant chunks from ChromaDB
Generating a response using the retrieved context
direct_answer

Handles non-policy questions by generating a direct response without retrieval.

MOCK_LLM Behavior

The application supports two execution modes controlled by the MOCK_LLM environment variable.

Default Mode (MOCK_LLM=1)

This is the graded baseline implementation.

classify_intent

Uses keyword matching (delivery, return, refund, membership, tracking, cancel, gift card, support hours) to classify queries.

retrieve_and_answer

Does not call an LLM.
Returns a templated response:

f"Based on the retrieved context: {top_chunk_snippet}"

using the highest-ranked retrieved chunk.

direct_answer

Returns the fixed response:

I can only answer questions about Zepto policies right now.

No LLM calls are made in mock mode.

Optional Real LLM Mode (MOCK_LLM=0)

In the optional extension mode:

classify_intent may use an LLM for intent classification.
retrieve_and_answer uses the structured prompt template from prompts.py to generate grounded answers from retrieved context.
direct_answer uses the LLM to answer general questions directly.

The retrieval process remains unchanged and continues to use ChromaDB and sentence embeddings.

Data Flow Summary
User Query
    │
    ▼
classify_intent
    │
    ├── policy_question
    │       │
    │       ▼
    │ retrieve_and_answer
    │       │
    │       ▼
    │ ChromaDB Retrieval
    │       │
    │       ▼
    │ Generated Answer
    │
    └── general_question
            │
            ▼
      direct_answer
            │
            ▼
      Generated Answer
            │
            ▼
        FastAPI Response


3. Docker Instructions

## Running Locally

Build:

docker build -t zepto-support .

Run:

docker run -p 7860:7860 zepto-support


Git Commands to Submit

From your local repository root:

cd zepto-data-ai-platform

Check status:

git status

Add everything:

git add .

Commit:

git commit -m "Complete support assistant module"

Push:

git push origin main

