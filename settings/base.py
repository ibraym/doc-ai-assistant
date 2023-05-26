# Copyright (C) 2023 Ibrahem Mouhamad
#
# SPDX-License-Identifier: MIT

import os
from pathlib import Path

BASE_DIR = str(Path(__file__).parents[1])

ANALYZER = {
    'huggingface': {
        'SentenceTransformers': 'sentence-transformers/all-MiniLM-L6-v2',
        'BertForQuestionAnswering': 'bert-large-uncased-whole-word-masking-finetuned-squad',
        'BertTokenizer': 'bert-large-uncased-whole-word-masking-finetuned-squad'
    }
}

DATA_ROOT = os.path.join(BASE_DIR, 'data')
EMBEDDINGS_ROOT = os.path.join(DATA_ROOT, 'embeddings')

os.makedirs(DATA_ROOT, exist_ok=True)
os.makedirs(EMBEDDINGS_ROOT, exist_ok=True)
