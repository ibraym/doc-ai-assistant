# Copyright (C) 2023 Ibrahem Mouhamad
#
# SPDX-License-Identifier: MIT

from abc import abstractmethod
from sentence_transformers import SentenceTransformer
import pandas as pd

import settings

class BaseEmbedder:
    """
    A class for embedding text using a model.

    Methods:
        embed(texts): Embeds the given text using the model.
        get_texts(): Returns the original text.
        get_dataframe(embeddings): Returns a Pandas DataFrame with the embedded text and the original text.
        length(): Returns the length of the embedded text.
    """

    @abstractmethod
    def embed(self, texts) -> pd.DataFrame:
        """
        Embeds the given text using the model.

        Args:
            texts: A list of strings representing the text to be embedded.

        Returns:
            A panada DataFrame contains the embeddings with the original text.
        """

    def get_dataframe(self, embeddings, texts: list) -> pd.DataFrame:
        """
        Returns a Pandas DataFrame with the embedded text and the original text.

        Returns:
            A Pandas DataFrame with the embedded text and the original text.
        """

        output = []
        i=0
        for embedding in embeddings:
            output.append({"text": texts[i], 'embedding': embedding})
            i+=1
        return pd.DataFrame(output)

class HuggingFaceEmbedder(BaseEmbedder):
    """
    A class for embedding text using Hugging Face models.

    Attributes:
        model: The Hugging Face model to use for embedding.
    """

    def __init__(self):
        self.model = SentenceTransformer(settings.ANALYZER['huggingface']['SentenceTransformers'])

    def embed(self, texts):
        embeddings = self.model.encode(texts)
        df = self.get_dataframe(embeddings, texts)
        return df
