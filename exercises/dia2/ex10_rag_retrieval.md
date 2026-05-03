# Ex10 - Implementar retrieval local com FAISS

## Contexto

Agora o desenho de RAG vira codigo. O objetivo e indexar documentos Markdown localmente e recuperar chunks relevantes com FAISS.

## Arquivos permitidos

```text
supportops_agent/rag/loader.py
supportops_agent/rag/chunking.py
supportops_agent/rag/embeddings.py
supportops_agent/rag/faiss_store.py
supportops_agent/rag/retrieval.py
```

## Contrato

Implemente:

```python
search_runbook(query: str, top_k: int = 3)
```

Regras:

- carregar docs Markdown locais;
- preservar metadata `source`, `section` e `service`;
- criar embeddings locais deterministicas;
- indexar com FAISS;
- retornar lista de resultados com `text`, `metadata` e `score`.

## Validacao

```bash
python run.py setup
python run.py test ex10
```

O exercicio exige `faiss-cpu==1.9.0.post1`. Se o import `faiss` falhar, o ambiente ainda nao esta pronto para este exercicio.

## Slides relacionados

- Slide 39: pipeline completo.
- Slide 40: chunking.
- Slide 41: embeddings.
- Slide 42: top-k.
- Slide 43: busca semantica.
