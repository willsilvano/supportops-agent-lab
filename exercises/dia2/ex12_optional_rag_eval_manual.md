# Ex12 opcional - Avaliacao manual de RAG

## Contexto

Antes de usar DeepEval no Dia 3, vale praticar avaliacao manual do retrieval. O objetivo e separar falha de busca de falha de resposta final.

Este exercicio e opcional para o Dia 2 caso sobre tempo.

## Dataset pequeno

Use estas perguntas:

1. O que fazer com 403 apos troca de role?
2. Qual role permite `dashboard:revenue`?
3. O que indica erro 429?
4. Quando feature flag pode causar 403?
5. O que fazer se o RAG nao tiver informacao sobre `dashboard:new-beta`?

## Tarefa

Para cada pergunta:

1. Rode ou simule top-3 do retriever.
2. Marque quais chunks sao relevantes.
3. Calcule:
   - recall@3;
   - precision@3;
   - citation coverage.
4. Identifique se a falha esta em:
   - chunking;
   - query;
   - embedding;
   - documento ausente;
   - geracao final.

## Entrega

Uma tabela com:

- pergunta;
- chunks esperados;
- chunks recuperados;
- recall@3;
- precision@3;
- diagnostico da falha;
- ajuste recomendado.

## Slides relacionados

- Slide 42: top-k e reranking.
- Slide 45: case de documentacao.
- Slide 58: metricas para RAG.

