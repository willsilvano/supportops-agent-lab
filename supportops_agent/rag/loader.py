from __future__ import annotations

from dataclasses import dataclass

from supportops_agent.data_loader import DOCS_DIR


@dataclass(frozen=True)
class Document:
    source: str
    text: str


def load_markdown_docs() -> list[Document]:
    docs: list[Document] = []
    for path in sorted(DOCS_DIR.glob("*.md")):
        docs.append(Document(source=path.name, text=path.read_text(encoding="utf-8")))
    return docs

