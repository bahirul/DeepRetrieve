"""Utility functions for working with documents"""

import tqdm
from pypdf import PdfReader


def extract_text_pdf(pdf_path: str) -> str:
    """Extract text from a PDF file"""
    reader = PdfReader(pdf_path)
    pdf_texts = []

    for _, page in enumerate(
        tqdm.tqdm(reader.pages, desc="Extracting text from pages")
    ):
        pdf_texts.append(page.extract_text().strip())

    # filter out empty strings
    pdf_texts = [text for text in pdf_texts if text]
    return "\n\n".join(pdf_texts)


def extract_text_markdown(markdown_path: str) -> str:
    """Extract text from a markdown file"""
    with open(markdown_path, "r", encoding="utf-8") as file:
        return file.read()


def extract_text_txt(txt_path: str) -> str:
    """Extract text from a txt file"""
    with open(txt_path, "r", encoding="utf-8") as file:
        return file.read()


def extract_text_from_file(file_path: str) -> str:
    """Extract text from a file"""
    if file_path.endswith(".pdf"):
        return extract_text_pdf(file_path)
    elif file_path.endswith(".md"):
        return extract_text_markdown(file_path)
    elif file_path.endswith(".txt"):
        return extract_text_txt(file_path)
    else:
        raise ValueError("Unsupported file format")
