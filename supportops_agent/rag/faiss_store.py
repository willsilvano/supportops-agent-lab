from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from supportops_agent.rag.chunking import Chunk
from supportops_agent.rag.embeddings import HashingEmbedder


@dataclass
class SearchResult:
    text: str
    metadata: dict[str, str]
    score: float


class LocalFaissStore:
    def __init__(self, chunks: list[Chunk], embedder: HashingEmbedder | None = None):
        try:
            import faiss
        except ImportError as exc:
            raise RuntimeError("faiss-cpu nao esta instalado. Rode `python run.py setup`.") from exc

        self.faiss = faiss
        self.chunks = chunks
        self.embedder = embedder or HashingEmbedder()
        vectors = self.embedder.embed_many([chunk.text for chunk in chunks])
        self.index = faiss.IndexFlatIP(vectors.shape[1])
        self.index.add(vectors)

    def search(self, query: str, top_k: int = 3) -> list[SearchResult]:
        query_vector = self.embedder.embed(query).reshape(1, -1).astype("float32")
        scores, indices = self.index.search(query_vector, top_k)
        results: list[SearchResult] = []
        for score, index in zip(scores[0], indices[0]):
            if index < 0:
                continue
            chunk = self.chunks[int(index)]
            results.append(SearchResult(text=chunk.text, metadata=chunk.metadata, score=float(score)))
        return results

