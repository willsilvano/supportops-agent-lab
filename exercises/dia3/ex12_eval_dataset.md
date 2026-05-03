# Ex12 - Dataset de avaliacao do projetao

## Contexto

Antes de rodar DeepEval, LangSmith, Ragas ou qualquer judge, voce precisa de casos esperados. Sem dataset, avaliacao vira opiniao.

## Arquivo principal

```text
supportops_agent/data/eval_cases.json
supportops_agent/evals/dataset.py
```

## Tarefa

Crie ou revise um dataset com casos que cubram:

- caso normal;
- API falhando;
- prompt injection;
- RAG sem resposta;
- permissao ausente;
- caso ambiguo.

Campos obrigatorios:

```json
{
  "id": "EVAL-001",
  "input": "Analise o ticket TCK-4821",
  "expected_tools": [],
  "expected_risk": "medium",
  "must_include_evidence": [],
  "forbidden_actions": [],
  "reference_answer": "..."
}
```

## Validacao

```bash
python run.py test ex12
```

## Slides relacionados

- Slide 56: T.R.A.C.E.
- Slide 57: metricas para agents com tools.
- Slide 58: metricas para RAG.
- Slide 60: dataset de avaliacao.

