# Copyright (C) 2023 Ibrahem Mouhamad
#
# SPDX-License-Identifier: MIT

import unittest
import hashlib

import qa.utils as ut

class TestFile(unittest.TestCase):
    def get_actual_hash(self):
        hash_digest = hashlib.new('md5')
        ut.get_file_hash(self.file, hash_digest)
        actual_hash = hash_digest.hexdigest()
        return actual_hash

    # test text_to_chunks function
    def test_text_to_chunks(self):
        texts = ['Hello, World!', 'Hello, World!']
        chunks = ut.text_to_chunks(texts, word_length=2)
        assert len(chunks) == 2
        assert chunks[0] == '"Hello, World!"'
        assert chunks[1] == '"Hello, World!"'

class TestTxtFile(TestFile):
    def setUp(self) -> None:
        self.file = 'tests/assets/test_dataset/test_txt.txt'

    # test txt_to_lines function
    def test_get_text_from_txt(self):
        lines = ut.txt_to_lines(self.file)
        assert len(lines) == 2
        assert lines[0] == 'Hello, World! '
        assert lines[1] == 'Hello, World!'

    def test_get_file_hash_with_md5(self):
        expected_hash = '5757414141a63cf1c315a22bd84da6ef'
        actual_hash = self.get_actual_hash()
        self.assertEqual(expected_hash, actual_hash)

class TestDocxFile(TestFile):
    def setUp(self) -> None:
        self.file = 'tests/assets/test_dataset/docx/test.docx'

    # test get_text_from_docx function
    def test_get_text_from_docx(self):
        paragraphs = ut.docx_to_text(self.file)
        assert len(paragraphs) == 2
        assert paragraphs[0] == 'Hello, World!'
        assert paragraphs[1] == 'Hello, World!'

    def test_get_file_hash_with_md5(self):
        expected_hash = '127587764a5b3b198c3e6f6bfeb67cca'
        actual_hash = self.get_actual_hash()
        self.assertEqual(expected_hash, actual_hash)

class TestPdfFile(TestFile):
    def setUp(self) -> None:
        self.file = 'tests/assets/test_dataset/pdf/test.pdf'

    # test get_text_from_pdf function
    def test_get_text_from_pdf(self):
        pages = ut.pdf_to_text('tests/assets/test_dataset/pdf/test.pdf')
        assert len(pages) == 2
        assert pages[0] == 'Hello, World!'
        assert pages[1] == 'Hello, World!'

    def test_get_file_hash_with_md5(self):
        expected_hash = '236415fa7ee746f99d053d7207e77e4d'
        actual_hash = self.get_actual_hash()
        self.assertEqual(expected_hash, actual_hash)

class TestGetFolderHash(unittest.TestCase):
    def setUp(self) -> None:
        self.docx_folder = 'tests/assets/test_dataset/docx'
        self.pdf_folder = 'tests/assets/test_dataset/pdf'

    def test_get_folder_hash_with_md5_docx(self):
        expected_hash = "127587764a5b3b198c3e6f6bfeb67cca"
        hash_digest = hashlib.new('md5')
        ut.get_folder_hash(self.docx_folder, hash_digest)
        actual_hash = hash_digest.hexdigest()
        self.assertEqual(expected_hash, actual_hash)

    def test_get_folder_hash_with_md5_pdf(self):
        expected_hash = "236415fa7ee746f99d053d7207e77e4d"
        hash_digest = hashlib.new('md5')
        ut.get_folder_hash(self.pdf_folder, hash_digest)
        actual_hash = hash_digest.hexdigest()
        self.assertEqual(expected_hash, actual_hash)

class TestGetDatasetHash(unittest.TestCase):

    def setUp(self) -> None:
        self.dataset_path = 'tests/assets/test_dataset'

    def test_get_dataset_hash_with_md5(self):
        expected_hash = "2dd51a6cce74b1f94c8af8f2ed5a5c6a"
        actual_hash = ut.get_dataset_hash(self.dataset_path)
        self.assertEqual(expected_hash, actual_hash)

if __name__ == '__main__':
    unittest.main()
