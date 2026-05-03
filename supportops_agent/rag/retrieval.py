from __future__ import annotations

from supportops_agent.rag.chunking import chunk_documents
from supportops_agent.rag.faiss_store import LocalFaissStore, SearchResult
from supportops_agent.rag.loader import load_markdown_docs


def build_default_store() -> LocalFaissStore:
    docs = load_markdown_docs()
    chunks = chunk_documents(docs)
    return LocalFaissStore(chunks)


def search_runbook(query: str, top_k: int = 3) -> list[dict[str, object]]:
    store = build_default_store()
    results: list[SearchResult] = store.search(query, top_k=top_k)
    return [
        {
            "text": result.text,
            "metadata": result.metadata,
            "score": result.score,
        }
        for result in results
    ]

