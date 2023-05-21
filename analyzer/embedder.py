# Copyright (C) 2023 Ibrahem Mouhamad
#
# SPDX-License-Identifier: MIT

from sentence_transformers import SentenceTransformer
import pandas as pd

import settings

class HuggingFaceEmbedder:
    def __init__(self, texts: list):
        self.model = SentenceTransformer(settings.ANALYZER['huggingface']['SentenceTransformers'])
        self.texts = texts
        self.embeddings = self.embed(texts=texts)

    def embed(self, texts: list):
        embeddings = self.model.encode(texts)
        return embeddings

    def get_embeddings(self):
        return self.embeddings

    def get_texts(self):
        return self.texts

    def get_dataframe(self):
        output = []
        i=0
        for embedding in self.embeddings:
            output.append({"text": self.texts[i], 'embedding': embedding})
            i+=1
        return pd.DataFrame(output)

    def length(self):
        return len(self.texts)
