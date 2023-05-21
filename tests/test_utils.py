# Copyright (C) 2023 Ibrahem Mouhamad
#
# SPDX-License-Identifier: MIT

import unittest

from analyzer.utils import pdf_to_text, docx_to_text, text_to_chunks

# test get_text_from_docx function
def test_get_text_from_docx():
    paragraphs = docx_to_text('tests/assets/test.docx')
    assert len(paragraphs) == 2
    assert paragraphs[0] == 'Hello, World!'
    assert paragraphs[1] == 'Hello, World!'


# test get_text_from_pdf function
def test_get_text_from_pdf():
    pages = pdf_to_text('tests/assets/test.pdf')
    assert len(pages) == 2
    assert pages[0] == 'Hello, World!'
    assert pages[1] == 'Hello, World!'

if __name__ == '__main__':
    unittest.main()

# test text_to_chunks function
def test_text_to_chunks():
    texts = ['Hello, World!', 'Hello, World!']
    chunks = text_to_chunks(texts, word_length=2)
    assert len(chunks) == 2
    assert chunks[0] == '"Hello, World!"'
    assert chunks[1] == '"Hello, World!"'
