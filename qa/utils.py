# Copyright (C) 2023 Ibrahem Mouhamad
#
# SPDX-License-Identifier: MIT

import re
import hashlib
import os

from scipy import spatial
import pandas as pd
import pdftotext
import docx

from .embedder import BaseEmbedder

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
    text = re.sub(r'\s+', ' ', text)
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

def txt_to_lines(file_path):
    """
    Read a text file and return a list of lines.

    Args:
        file_path: The path to the text file.

    Returns:
        A list of lines in the text file.
    """

    with open(file_path, "r") as f:
        lines = f.readlines()
    processed_lines = []
    for line in lines:
        processed_lines.append(reprocess(line))
    return processed_lines

def read_file(file_path: str, filename: str) -> list:
    """
    Read the contents of a file and return a list of text chunks.

    Args:
        file_path: The path to the file.
        filename: The name of the file.

    Returns:
        A list of text chunks.
    """

    file_extension = os.path.splitext(file_path)[1].lower()
    if file_extension in ['.pdf', '.docx', '.txt']:
        if file_extension == '.pdf':
            pages = pdf_to_text(file_path)
            return text_to_chunks(pages, filename)
        elif file_extension == '.docx':
            paragraphs = docx_to_text(file_path)
            return text_to_chunks(paragraphs, filename)
        else:
            lines = txt_to_lines(file_path)
            return text_to_chunks(lines, filename)
    else:
        return None

def read_folder(folder_path: str, texts: list) -> list:
    """
    Read the contents of all files in a folder and add them to a list.

    Args:
        folder_path: The path to the folder.
        texts: A list to store the text chunks.

    Returns:
        The list of text chunks.
    """

    for root, _, files in os.walk(folder_path):
        for file in files:
            print(file)
            file_path = os.path.join(root, file)
            texts += read_file(file_path, file)

def read_dataset(dataset_path: str) -> list:
    """
    Read the contents of a dataset and return a list of text chunks.

    Args:
        dataset_path: The path to the dataset.

    Returns:
        A list of text chunks.
    """

    dataset_texts = []
    read_folder(dataset_path, dataset_texts)
    return dataset_texts

def text_to_chunks(texts: list, filename, word_length: int = 256) -> list:
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
            chunk = '{} "{}"'.format(filename, chunk)
            chunks.append(chunk)
    return chunks

def strings_ranked_by_relatedness(
    query: str,
    source_embeddings: pd.DataFrame,
    embedder: BaseEmbedder,
    relatedness_fn=lambda x, y: 1 - spatial.distance.cosine(x, y),
    top_n: int = 100
) -> 'tuple[list[str], list[float]]':
    """
    Ranks a list of strings by their relatedness to a given query.

    Args:
        query: The query string.
        source_embeddings: A Pandas DataFrame of source embeddings.
        embedder: An embedding model.
        relatedness_fn: A function that computes the relatedness between two embeddings.
        top_n: The number of top-ranked strings to return.

    Returns:
        A tuple of two lists: the first list contains the top-ranked strings, and the second list contains their relatedness scores.
    """

    output = embedder.embed([query])
    query_embedding = output[0]
    strings_and_relatednesses = [
        (row["text"], relatedness_fn(query_embedding, row["embedding"]))
        for i, row in source_embeddings.iterrows()
    ]
    strings_and_relatednesses.sort(key=lambda x: x[1], reverse=True)
    strings, relatednesses = zip(*strings_and_relatednesses)
    return strings[:top_n], relatednesses[:top_n]

def get_dataset_hash(dataset_path, hash_algorithm='md5'):
    """
    Get the hash of a dataset.

    Args:
        dataset_path: The path to the dataset.
        hash_algorithm: The hash algorithm to use.

    Returns:
        The hash of the dataset.
    """

    hash_digest = hashlib.new(hash_algorithm)
    get_folder_hash(dataset_path, hash_digest)
    return hash_digest.hexdigest()

def get_folder_hash(folder_path, hash_digest):
    """
    Get the hash of a folder.

    Args:
        folder_path: The path to the folder.
        hash_digest: The hash object to update.

    Returns:
        None.
    """

    for root, _, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)
            get_file_hash(file_path, hash_digest)

def get_file_hash(file_path, hash_digest):
    """
    Get the hash of a file.

    Args:
        file_path: The path to the file.
        hash_digest: The hash object to update.

    Returns:
        None.
    """

    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_digest.update(chunk)
