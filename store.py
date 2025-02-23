""" Store document in ChromaDB """

import os
import sys
import uuid

import chromadb
import nltk
import tqdm
import yaml
from sentence_transformers import SentenceTransformer

from utils.doc_util import extract_text_from_file
from utils.text_util import chunk_text


def nltk_download():
    """Download NLTK resources"""
    try:
        nltk.data.find("tokenizers/punkt")
        nltk.data.find("tokenizers/punkt_tab")
    except LookupError:
        nltk.download("punkt")
        nltk.download("punkt_tab")


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

    # setup nltk resources and load configuration
    nltk_download()

    try:
        with open("config.yml", "r", encoding="utf-8") as file:
            config = yaml.safe_load(file)
    except FileNotFoundError:
        print("Configuration file not found.")
        sys.exit(1)

    # ask document path
    pdf_path = input("Enter file path of the document [pdf, txt, markdown]: ")

    # validate document path
    if not validate_file_path(pdf_path):
        sys.exit(1)

    # Extract text from file
    text = extract_text_from_file(pdf_path)

    # Tokenize and Chunk text
    chunks = chunk_text(text, chunk_size=config["text"]["chunk_size"])

    # Store in ChromaDB
    chroma_client = chromadb.PersistentClient(
        path=config["chromadb"]["path"]
    )  # Persistent storage
    collection = chroma_client.get_or_create_collection(
        name=config["chromadb"]["collection"],
        metadata={"dimentionality": config["chromadb"]["dim"]},
    )

    embedding_model = SentenceTransformer(config["embedding"]["model"])
    for _, chunk in enumerate(tqdm.tqdm(chunks, desc="Storing chunks to ChromaDB")):
        embedding = embedding_model.encode(chunk).tolist()
        collection.add(
            documents=[chunk], embeddings=[embedding], ids=[str(uuid.uuid4())]
        )

    print(f"✅ Stored {len(chunks)} chunks in ChromaDB.")


if __name__ == "__main__":
    main()
