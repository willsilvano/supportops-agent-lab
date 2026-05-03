# Ex13 - Exercicio final: avaliando com DeepEval

## Contexto

O objetivo final e comparar qualidade da resposta do agente usando DeepEval localmente, integrado com a LLM configurada. Nao vamos depender de evals em cloud.

## Arquivos principais

```text
supportops_agent/evals/deepeval_runner.py
supportops_agent/evals/dataset.py
supportops_agent/data/eval_cases.json
```

## Tarefa

1. Configure `GOOGLE_API_KEY` no `.env`.
2. Garanta que Gemini esta acessivel.
3. Implemente `run_deepeval()` em `supportops_agent/evals/deepeval_runner.py`.
4. Carregue o dataset do projetao com `load_eval_cases()`.
5. Execute o agente para cada caso.
6. Monte um `LLMTestCase` por caso.
7. Use pelo menos:
   - Answer Relevancy;
   - Faithfulness.
8. Compare:
   - agente sem RAG;
   - agente com RAG;
   - agente com RAG + guardrails.

## Execucao

```bash
python -m supportops_agent.evals.deepeval_runner
```

## Entrega

Um breve relatorio com:

- casos que passaram;
- casos que falharam;
- metrica mais fraca;
- restricoes antes de producao.

## Slides relacionados

- Slide 61: ferramentas de avaliacao.
- Slide 62: avaliando com DeepEval.
- Slide 63 e 64: checklist de producao.
