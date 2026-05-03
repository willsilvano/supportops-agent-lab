from __future__ import annotations

import hashlib
import re

import numpy as np


TOKEN_RE = re.compile(r"[a-zA-Z0-9_:-]+")


class HashingEmbedder:
    """Embedder local deterministico para aula.

    Ele nao substitui embeddings de producao. Serve para manter o RAG local,
    barato e reprodutivel enquanto a aula foca em chunking, FAISS e payload.
    """

    def __init__(self, dimensions: int = 128):
        self.dimensions = dimensions

    def embed(self, text: str) -> np.ndarray:
        vector = np.zeros(self.dimensions, dtype="float32")
        for token in TOKEN_RE.findall(text.lower()):
            digest = hashlib.sha256(token.encode("utf-8")).digest()
            index = int.from_bytes(digest[:4], "little") % self.dimensions
            vector[index] += 1.0
        norm = np.linalg.norm(vector)
        if norm:
            vector /= norm
        return vector

    def embed_many(self, texts: list[str]) -> np.ndarray:
        return np.vstack([self.embed(text) for text in texts]).astype("float32")

