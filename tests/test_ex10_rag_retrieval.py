import unittest

from supportops_agent.rag.chunking import chunk_documents
from supportops_agent.rag.loader import load_markdown_docs


class Ex10RagRetrievalTest(unittest.TestCase):
    def test_chunking_preserves_source_and_section(self):
        chunks = chunk_documents(load_markdown_docs())
        self.assertGreaterEqual(len(chunks), 4)
        self.assertIn("source", chunks[0].metadata)
        self.assertIn("section", chunks[0].metadata)

    def test_retrieval_finds_403_runbook(self):
        from supportops_agent.rag.retrieval import search_runbook

        results = search_runbook("403 apos troca de role no dashboard", top_k=3)
        joined = "\n".join(result["text"] for result in results)
        self.assertIn("403", joined)
        self.assertIn("role", joined)


if __name__ == "__main__":
    unittest.main()
