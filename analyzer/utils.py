# Copyright (C) 2023 Ibrahem Mouhamad
#
# SPDX-License-Identifier: MIT

import re

import pdftotext
import docx

def reprocess(text):
    """
    Reprocesses a text by removing newlines, tabs, and extra spaces.

    Args:
        text: The text to be preprocessed.

    Returns:
        The preprocessed text.
    """

    text = text.replace('\n', ' ')
    text = text.replace('\t', '')
    text = re.sub('\s+', ' ', text)
    return text

# get a list of paragraphs from docx file
def docx_to_text(filename: str) -> list:
    """Reads a Word docx file and returns a list of pages.

    Args:
        filename: The path to the Word file.

    Returns:
        A list of paragraphs, where each paragraph is a string.
    """

    with open(filename, "rb") as f:
        doc = docx.Document(f)
    paragraphs = []

    for page in doc.paragraphs:
        if (page.text == ''):
            continue
        paragraphs.append(reprocess(page.text))
    return paragraphs

# get a list of pages from PDF file
def pdf_to_text(filename: str) -> list:
    """Reads a PDF file and returns a list of pages.

    Args:
        filename: The path to the PDF file.

    Returns:
        A list of pages, where each page is a string.
    """

    pages = []
    with open(filename, 'rb') as f:
        pdf = pdftotext.PDF(f)
    # Iterate over all the pages
    for page in pdf:
        pages.append(reprocess(page))
    return pages

def text_to_chunks(texts: list, word_length: int = 256, start_page: int = 1) -> list:
    """
    Splits a list of texts into chunks of the given word length.

    Args:
        texts: A list of strings representing the text to be split.
        word_length: The desired length of each chunk.
        start_page: The page number to start splitting from.

    Returns:
        A list of strings representing the chunks.
    """

    text_tokens = [t.split(' ') for t in texts]
    chunks = []

    for idx, words in enumerate(text_tokens):
        for i in range(0, len(words), word_length):
            chunk = words[i : i + word_length]
            if (
                (i + word_length) > len(words)
                and (len(chunk) < word_length)
                and (len(text_tokens) != (idx + 1))
            ):
                text_tokens[idx + 1] = chunk + text_tokens[idx + 1]
                continue
            chunk = ' '.join(chunk).strip()
            chunk = f'"' + chunk + '"'
            chunks.append(chunk)
    return chunks
