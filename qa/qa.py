# Copyright (C) 2023 Ibrahem Mouhamad
#
# SPDX-License-Identifier: MIT

from abc import abstractmethod
import os.path as osp
import ast

import torch
from transformers import BertForQuestionAnswering
from transformers import BertTokenizer
import pandas as pd
from scipy import spatial

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

    @abstractmethod
    def get_source_embeddings(self) -> pd.DataFrame:
        """
        Get the embeddings for the dataset.

        Returns:
            A Pandas DataFrame of embeddings.
        """

    def strings_ranked_by_relatedness(
        self,
        query: str,
        relatedness_fn=lambda x, y: 1 - spatial.distance.cosine(x, y),
        top_n: int = 100
    ) -> 'tuple[list[str], list[float]]':
        """
        Ranks a list of strings by their relatedness to a given query.

        Args:
            query: The query string.
            relatedness_fn: A function that computes the relatedness between two embeddings.
            top_n: The number of top-ranked strings to return.

        Returns:
            A tuple of two lists: the first list contains the top-ranked strings, and the second list contains their relatedness scores.
        """
        embeddings = self.get_source_embeddings()
        output = self.embedder.model.encode([query])
        query_embedding = output[0]
        strings_and_relatednesses = [
            (row["text"], relatedness_fn(query_embedding, row["embedding"]))
            for i, row in embeddings.iterrows()
        ]
        strings_and_relatednesses.sort(key=lambda x: x[1], reverse=True)
        strings, relatednesses = zip(*strings_and_relatednesses)
        return strings[:top_n], relatednesses[:top_n]

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
        self.embedder = HuggingFaceEmbedder()

    def get_source_embeddings(self) -> pd.DataFrame:
        if osp.exists(osp.join(self.dataset_embeddings_file)):
            df = pd.read_csv(self.dataset_embeddings_file, converters={'embedding': ut.from_np_array})
            return df

        df = self.embedder.embed(ut.read_dataset(self.dataset_path))
        # Save the embeddings DataFrame to a CSV file
        df.to_csv(self.dataset_embeddings_file, index=False)

        return df

    def get_correct_answer(self, answer: str) -> str:
        corrected_answer = ''
        for word in answer.split():
            # If it's a sub-word token
            if word[0:2] == '##':
                corrected_answer += word[2:]
            else:
                corrected_answer += ' ' + word
        return corrected_answer

    def answer(self, question: str) -> str:
        # search
        strings,_ = self.strings_ranked_by_relatedness(question)
        # get answer
        print(strings)
        encoding = self.tokenizer.encode_plus(text=question,text_pair=strings)
        inputs = encoding['input_ids']  # Token embeddings
        sentence_embedding = encoding['token_type_ids']  # Segment embeddings
        tokens = self.tokenizer.convert_ids_to_tokens(inputs) # input tokens
        start_scores, end_scores = self.model(input_ids=torch.tensor([inputs]), token_type_ids=torch.tensor([sentence_embedding]), return_dict=False)
        start_index = torch.argmax(start_scores)
        end_index = torch.argmax(end_scores)
        answer = ' '.join(tokens[start_index:end_index+1])
        return self.get_correct_answer(answer)
