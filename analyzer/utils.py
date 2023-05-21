# Copyright (C) 2023 Ibrahem Mouhamad
#
# SPDX-License-Identifier: MIT

import pdftotext

# get a list pf pages from PDF file
def get_text_from_pdf(pdf_file):
    pages = []
    with open(pdf_file, 'rb') as f:
        pdf = pdftotext.PDF(f)
    # Iterate over all the pages
    for page in pdf:
        pages.append(page)
    return pages
