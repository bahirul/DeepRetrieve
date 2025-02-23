## Store

Extract text from documents and store them in ChromaDB using embeddings.

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