"""Utility functions for text processing"""

import nltk
from tqdm import tqdm


def chunk_text(text: str, chunk_size: int = 5) -> list[str]:
    """Chunk text into smaller pieces using nltk with sentence tokenization"""
    sentences = nltk.sent_tokenize(text)

    chunks = []
    current_chunk = []
    for _, chunk in enumerate(tqdm(sentences, desc="Chunking text")):
        if len(current_chunk) < chunk_size:
            current_chunk.append(chunk)
        else:
            chunks.append(" ".join(current_chunk))
            current_chunk = []

    return chunks


def truncate_text(text: str, max_length: int) -> str:
    """Truncate text to a maximum length"""
    return text[:max_length] + "..." if len(text) > max_length else text
