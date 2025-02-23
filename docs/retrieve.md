# Retrieve

Retrieve information from the documents using embeddings and send them to the LLM model for further processing.

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