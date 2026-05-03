from __future__ import annotations

from dataclasses import dataclass

from supportops_agent.rag.loader import Document


@dataclass(frozen=True)
class Chunk:
    text: str
    metadata: dict[str, str]


def chunk_markdown_by_section(doc: Document) -> list[Chunk]:
    chunks: list[Chunk] = []
    current_title = "intro"
    current_lines: list[str] = []

    def flush() -> None:
        if not current_lines:
            return
        text = "\n".join(current_lines).strip()
        if text:
            chunks.append(
                Chunk(
                    text=text,
                    metadata={
                        "source": doc.source,
                        "section": current_title,
                        "service": "analytics-api",
                    },
                )
            )

    for line in doc.text.splitlines():
        if line.startswith("#"):
            flush()
            current_title = line.lstrip("#").strip()
            current_lines = [line]
        else:
            current_lines.append(line)
    flush()
    return chunks


def chunk_documents(docs: list[Document]) -> list[Chunk]:
    chunks: list[Chunk] = []
    for doc in docs:
        chunks.extend(chunk_markdown_by_section(doc))
    return chunks

