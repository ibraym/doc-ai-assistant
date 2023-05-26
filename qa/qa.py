# Copyright (C) 2023 Ibrahem Mouhamad
#
# SPDX-License-Identifier: MIT

import torch
from transformers import BertForQuestionAnswering
from transformers import BertTokenizer

import settings

class BaseQA:
    def __init__(self, dataset_path: str):
        self.dataset_path = dataset_path

class HuggingFaceQA(BaseQA):
    def __init__(self, dataset_path: str):
        super().__init__(dataset_path)
        self.model = BertForQuestionAnswering.from_pretrained(settings.ANALYZER['huggingface']['BertForQuestionAnswering'])
        self.tokenizer = BertTokenizer.from_pretrained(settings.ANALYZER['huggingface']['BertTokenizer'])
        # self.embedder = self.embed(texts=texts)
