# Ex11 opcional - Query rewriting e HyDE para RAG

## Contexto

Perguntas de usuario raramente chegam no formato ideal para busca vetorial. Em RAG, uma etapa simples de reescrita de query pode melhorar muito a recuperacao.

Este exercicio e opcional para o Dia 2 caso sobre tempo.

## Cenario

Pergunta original:

```text
O dashboard parou depois que mudaram meu perfil. O que faco?
```

Essa pergunta e humana, mas pouco precisa para retrieval. Ela nao menciona `403`, `role`, `analytics-api`, `permissao` nem `cache`.

## Tarefa

Crie tres estrategias de busca:

1. Query original
   - Use exatamente a pergunta do usuario.

2. Query rewriting
   - Reescreva a pergunta para termos mais tecnicos.
   - Exemplo: `erro 403 dashboard apos alteracao de role analytics-api cache permissoes`.

3. HyDE simplificado
   - Escreva uma resposta hipotetica curta.
   - Use essa resposta hipotetica como texto de busca.

## Entrega

Um Markdown com:

- query original;
- query reescrita;
- resposta hipotetica HyDE;
- top-3 documentos/chunks esperados;
- comparacao de qual estrategia parece melhor.

## Discussao

Responda:

- a query original recupera o runbook certo?
- a query reescrita aumenta precisao?
- HyDE ajudou ou trouxe ruido?
- em que caso voce automatizaria query rewriting com LLM?

## Slides relacionados

- Slide 39: pipeline completo.
- Slide 41: embeddings.
- Slide 42: top-k e reranking.
- Slide 45: chat com documentacao da analytics-api.

