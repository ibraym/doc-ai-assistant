# Copyright (C) 2023 Ibrahem Mouhamad
#
# SPDX-License-Identifier: MIT

import unittest

from analyzer.utils import get_text_from_pdf

# test get_text_from_pdf function
def test_get_text_from_pdf():
    pages = get_text_from_pdf('tests/assets/test.pdf')
    assert len(pages) == 2
    assert pages[0] == 'Hello, World!'
    assert pages[1] == 'Hello, World!'

if __name__ == '__main__':
    unittest.main()
