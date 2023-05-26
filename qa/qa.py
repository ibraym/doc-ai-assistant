# Copyright (C) 2023 Ibrahem Mouhamad
#
# SPDX-License-Identifier: MIT

import os.path as osp

import torch
from transformers import BertForQuestionAnswering
from transformers import BertTokenizer
import pandas as pd

import settings
from .embedder import HuggingFaceEmbedder
from . import utils as ut

class BaseQA:
    """
    Base class for question answering models.

    Args:
    dataset_path: The path to the dataset.
    """

    def __init__(self, dataset_path: str):
        self.dataset_path = dataset_path
        self.dataset_checksum = ut.get_dataset_hash(dataset_path)
        self.dataset_embeddings_file = osp.join(settings.EMBEDDINGS_ROOT, '{}.csv'.format(self.dataset_checksum))

class HuggingFaceQA(BaseQA):
    """
    Hugging Face question answering model.

    Args:
    dataset_path: The path to the dataset.
    """

    def __init__(self, dataset_path: str):
        super().__init__(dataset_path)
        self.model = BertForQuestionAnswering.from_pretrained(settings.ANALYZER['huggingface']['BertForQuestionAnswering'])
        self.tokenizer = BertTokenizer.from_pretrained(settings.ANALYZER['huggingface']['BertTokenizer'])

    def get_embeddings(self) -> pd.DataFrame:
        """
        Get the embeddings for the dataset.

        Returns:
            A Pandas DataFrame of embeddings.
        """

        if osp.exists(osp.join(self.dataset_embeddings_file)):
            embeddings = pd.read_csv(self.dataset_embeddings_file)
            return embeddings

        embedder = HuggingFaceEmbedder(ut.read_dataset(self.dataset_path))
        df = embedder.embed()
        # Save the embeddings DataFrame to a CSV file
        df.to_csv("my_file.csv")

        return df
