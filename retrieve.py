""" Retrive document from the Chroma database based on the query"""

import asyncio
import sys

import yaml
from ollama import AsyncClient
from sentence_transformers import SentenceTransformer

import chromadb


def validate_query(query: str) -> bool:
    """Validate query"""
    if not query:
        print("Query cannot be empty.")
        return False
    return True


async def main():
    """Main"""

    # load configuration
    try:
        with open("config.yml", "r", encoding="utf-8") as file:
            config = yaml.safe_load(file)
    except FileNotFoundError:
        print("Configuration file not found.")
        sys.exit(1)

    # ask query
    query = input("Enter the query to search for: ")

    # check if the query is empty
    if not validate_query(query):
        sys.exit(1)

    # chromadb setup
    chroma_client = chromadb.PersistentClient(config["chromadb"]["path"])
    collection = chroma_client.get_or_create_collection(
        name=config["chromadb"]["collection"],
        metadata={"dimentionality": config["chromadb"]["dim"]},
    )

    # search for the query
    embedding_model = SentenceTransformer(config["embedding"]["model"])
    results = collection.query(
        query_embeddings=[embedding_model.encode(query)],
        n_results=config["chromadb"]["n_results"],  # get the top 5 results
    )

    # check if no documents found
    if len(results["documents"]) == 0:
        print("No documents found.")
        sys.exit(1)

    # retrieve the documents
    document_results = results["documents"][0]

    # process to ollama
    if len(document_results) > 0:
        if config["ollama"]["api_url"] and config["ollama"]["model"]:
            print(f"Processing documents to LLM model {config["ollama"]["model"]}...")

            # chat with the LLM model
            await chat(
                config["ollama"]["api_url"],
                config["ollama"]["model"],
                document_results,
                query,
            )
        else:
            print(
                "Ollama API URL and model not configured, query manually from the documents."
            )
            for i, doc in enumerate(document_results):
                print(f"Document {i+1}:")
                print(doc)
                print("\n\n")


async def chat(host: str, model: str, documents: list[str], query: str):
    """Chat with the LLM model"""
    client = AsyncClient(host=host)

    prompt = f"""
    Based on the following retrieved context: 

    {"\n".join(documents) if documents else "No context available."}



    Answer the following question: 

    {query}"""

    # Send to the LLM model
    messages = [
        {"role": "user", "content": prompt},
    ]

    # Realtime chat with the LLM model
    async for part in await client.chat(
        model=model,
        messages=messages,
        stream=True,
    ):
        print(part["message"]["content"], end="", flush=True)


if __name__ == "__main__":
    asyncio.run(main())
