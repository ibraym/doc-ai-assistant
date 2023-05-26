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

    Args:
        texts: A list of strings representing the text to be embedded.

    Attributes:
        texts: The original text to be embedded.

    Methods:
        embed(texts): Embeds the given text using the model.
        get_embeddings(): Returns the embedded text.
        get_texts(): Returns the original text.
        get_dataframe(): Returns a Pandas DataFrame with the embedded text and the original text.
        length(): Returns the length of the embedded text.
    """

    def __init__(self, texts: list):
        self.texts = texts

    @abstractmethod
    def embed(self, texts: list):
        """
        Embeds the given text using the model.

        Args:
            texts: A list of strings representing the text to be embedded.

        Returns:
            A list of NumPy arrays representing the embedded text.
        """

    def get_embeddings(self):
        """
        Returns the embedded text.

        Returns:
            A list of NumPy arrays representing the embedded text.
        """

        return self.embeddings

    def get_texts(self):
        """
        Returns the original text.

        Returns:
            A list of strings representing the original text.
        """

        return self.texts

    def get_dataframe(self):
        """
        Returns a Pandas DataFrame with the embedded text and the original text.

        Returns:
            A Pandas DataFrame with the embedded text and the original text.
        """

        output = []
        i=0
        for embedding in self.embeddings:
            output.append({"text": self.texts[i], 'embedding': embedding})
            i+=1
        return pd.DataFrame(output)

    def length(self):
        """
        Returns the length of the embedded text.

        Returns:
            The length of the embedded text.
        """

        return len(self.texts)


class HuggingFaceEmbedder(BaseEmbedder):
    """
    A class for embedding text using Hugging Face models.

    Args:
        texts: A list of strings representing the text to be embedded.

    Attributes:
        model: The Hugging Face model to use for embedding.
        texts: The original text to be embedded.
        embeddings: The embedded text.
    """

    def __init__(self, texts: list):
        super().__init__(texts)
        self.model = SentenceTransformer(settings.ANALYZER['huggingface']['SentenceTransformers'])
        self.embeddings = self.embed(texts=texts)

    def embed(self, texts: list):
        embeddings = self.model.encode(texts)
        return embeddings
