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

1. [Store](docs/store.md)
2. [Retrieve](docs/retrieve.md)