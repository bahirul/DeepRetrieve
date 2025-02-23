"""Utility functions for text processing"""

import nltk
import tqdm
from langchain.text_splitter import RecursiveCharacterTextSplitter, TokenTextSplitter


def text_chunk(text: str, chunk_size: int = 500, chunk_overlap: int = 0) -> list[str]:
    """Chunk text into smaller pieces using RecursiveCharacterTextSplitter"""
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size, chunk_overlap=chunk_overlap
    )
    chunks = text_splitter.split_text(text)
    return chunks


def token_text_chunk(
    text: str, chunk_size: int = 500, chunk_overlap: int = 0
) -> list[str]:
    """Chunk text into smaller pieces using TokenTextSplitter"""
    text_splitter = TokenTextSplitter(
        chunk_size=chunk_size, chunk_overlap=chunk_overlap
    )
    chunks = text_splitter.split_text(text)
    return chunks


def nltk_chunk_text(text, chunk_size=512, overlap=50):
    """Chunk text into smaller pieces using NLTK"""
    sentences = nltk.sent_tokenize(text)
    chunks = []
    current_chunk = []
    current_length = 0

    for _, sentence in enumerate(tqdm.tqdm(sentences, desc="Chunking text")):
        sentence_length = len(sentence.split())
        if current_length + sentence_length > chunk_size:
            chunks.append(" ".join(current_chunk))
            current_chunk = current_chunk[-overlap:]  # Preserve overlap
            current_length = sum(len(str(sent).split()) for sent in current_chunk)

        current_chunk.append(sentence)
        current_length += sentence_length

    if current_chunk:
        chunks.append(" ".join(current_chunk))

    return chunks
