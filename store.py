""" Store document in ChromaDB """

import os
import sys
import uuid

import tqdm
import yaml
from sentence_transformers import SentenceTransformer

import chromadb
from utils.doc_util import extract_text_from_file
from utils.text_util import nltk_chunk_text


def validate_file_path(file_path: str) -> bool:
    """Validate file path"""
    if not file_path:
        print("Document path cannot be empty.")
        return False

    if not os.path.isfile(file_path):
        print(f"File {file_path} does not exist.")
        return False

    if not file_path.endswith((".pdf", ".txt", ".md")):
        print("File must be a PDF, txt, or markdown.")

    return True


def main():
    """Main function"""
    # Load configuration
    try:
        with open("config.yml", "r", encoding="utf-8") as file:
            config = yaml.safe_load(file)
    except FileNotFoundError:
        print("Configuration file not found.")
        sys.exit(1)

    # ask document path
    pdf_path = input("Enter file path of the document [pdf, txt, markdown]: ")

    # validate document path
    pdf_path = pdf_path.strip()
    if not validate_file_path(pdf_path):
        sys.exit(1)

    # Extract text from file
    text = extract_text_from_file(pdf_path)

    # Chunk text
    chunks = nltk_chunk_text(
        text,
        chunk_size=config["text"]["chunk_text_size"],
        overlap=config["text"]["chunk_text_overlap"],
    )

    # Store in ChromaDB
    chroma_client = chromadb.PersistentClient(path=config["chromadb"]["path"])

    # Persistent storage
    collection = chroma_client.get_or_create_collection(
        name=config["chromadb"]["collection"],
        metadata={"dimentionality": config["chromadb"]["dim"]},
    )

    # Embed chunks
    embedding_model = SentenceTransformer(
        config["embedding"]["model"],
        trust_remote_code=config["embedding"]["trust_remote_code"],
    )
    for _, chunk in enumerate(tqdm.tqdm(chunks, desc="Storing chunks to ChromaDB")):
        embedding = embedding_model.encode(chunk).tolist()
        collection.add(
            documents=[chunk], embeddings=[embedding], ids=[str(uuid.uuid4())]
        )

    print(
        f"{'✅' if len(chunks) > 0 else '⚠️'} Stored {len(chunks)} chunks in ChromaDB."
    )


if __name__ == "__main__":
    main()
