# DeepRetrieve

DeepRetrieve is a Retrieval-Augmented Generation (RAG)-based system designed to efficiently retrieve, analyze, and compare information from various documents. Leveraging vector search technology and Large Language Models (LLMs).

## Demo Preview
[![asciicast](https://asciinema.org/a/704910.svg)](https://asciinema.org/a/704910)


## Setup Instructions

- Clone the repository
- Setup virtual environment (Python 3.12+)
    ```bash
    python3.12 -m venv venv
    source venv/bin/activate
    ```
- Install dependencies
    ```bash
    pip install -r requirements.txt
    ```

## Usage

- Setup the configuration file
    ```bash
    cp config.yml.example config.yml
    ```
- Update the configuration file with the required information
    - Note: The `ollama` section is optional and can be left empty if you don't want to use the LLM model for processing the documents.
- Store the documents in ChromaDB
    ```bash
    python3.12 store.py
    ```
- Retrieve information from the documents
    ```bash
    python3.12 retrieve.py
    ```

## Flowchart

1. store.py (Store the documents in ChromaDB using embeddings)
    ```mermaid
    flowchart TD
        A[Start] --> B[Setup nltk resources]
        B --> C[Load configuration from config.yml]
        C --> D{Configuration file found?}
        D -->|No| E[Print error and exit]
        D -->|Yes| F[Ask for document path]
        F --> G[Validate document path]
        G --> H{Is path valid?}
        H -->|No| I[Print error and exit]
        H -->|Yes| J[Extract text from file]
        J --> K[Chunk text]
        K --> L[Setup ChromaDB client]
        L --> M[Get or create collection]
        M --> N[Initialize embedding model]
        N --> O[Iterate over text chunks]
        O --> P[Generate embeddings for chunk]
        P --> Q[Add chunk to collection]
        Q --> R{More chunks?}
        R -->|Yes| O
        R -->|No| S[Print success message]
        S --> T[End]
    ```
2. retrieve.py (Retrieve information from the documents using embeddings)
    ```mermaid
    flowchart TD
    A[Start] --> B[Load configuration from config.yml]
    B --> C{Configuration file found?}
    C -->|No| D[Print error and exit]
    C -->|Yes| E[Ask for query]
    E --> F[Validate query]
    F --> G{Is query valid?}
    G -->|No| H[Print error and exit]
    G -->|Yes| I[Setup ChromaDB client]
    I --> J[Get or create collection]
    J --> K[Initialize embedding model]
    K --> L[Search for the query]
    L --> M{Documents found?}
    M -->|No| N[Print no documents found and exit]
    M -->|Yes| O[Retrieve the documents]
    O --> P{Ollama API URL and model configured?}
    P -->|No| Q[Print documents manually]
    P -->|Yes| R[Process documents to LLM model]
    R --> S[Chat with the LLM model]
    S --> T[End]
    Q --> T
    N --> T
    D --> T
    ```