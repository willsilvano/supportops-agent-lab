# SupportOps Agent Lab

Laboratorio da Semana 4 para construir, em camadas, o **SupportOps Agent**: um agente de suporte tecnico que analisa tickets, consulta APIs internas mockadas, usa RAG local com FAISS, aplica guardrails e roda avaliacoes com DeepEval.

## Como rodar

Use os comandos abaixo a partir desta pasta:

```bash
python run.py doctor
python run.py setup
python run.py mock-api
python run.py test ex00
```

`python run.py test all` e esperado somente depois que os exercicios implementaveis forem concluidos pelos alunos.

Depois de subir a API:

```text
http://127.0.0.1:8000/docs
```

## LLM

Os exercicios priorizam Gemini. Configure:

```bash
cp .env.example .env
```

E preencha:

```text
GOOGLE_API_KEY=...
GEMINI_MODEL=gemini-2.5-flash
```

Os testes deterministos usam dados locais e fakes quando isso evita custo/rede. Os exercicios finais assumem acesso ao Gemini e ao DeepEval.

Importante: varias funcoes com `TODO` levantam `NotImplementedError` no scaffold inicial. Isso e intencional; elas sao o trabalho dos exercicios.

## Contratos que nao devem ser alterados

Os alunos podem implementar o corpo das funcoes indicadas nos enunciados, mas nao devem alterar:

- nomes de arquivos e modulos;
- nomes de funcoes publicas;
- parametros das funcoes;
- nomes dos endpoints mockados;
- nomes das chaves retornadas nos schemas;
- arquivos em `tests/`, exceto se o professor pedir explicitamente.

## Mock API

A mock API e um servico FastAPI real. A logica e mockada, mas os endpoints HTTP existem e leem dados locais em `supportops_agent/data/*.json`.

Endpoints principais:

- `GET /health`
- `GET /tickets`
- `GET /tickets/{ticket_id}`
- `GET /tickets/{ticket_id}/notes`
- `POST /tickets/{ticket_id}/notes`
- `GET /users`
- `GET /users/{user_id}`
- `GET /users/{user_id}/roles`
- `GET /roles/{role_id}`
- `GET /roles/{role_id}/permissions`
- `GET /access/check?user_id=...&resource=...`
- `GET /services`
- `GET /services/{service_id}/status`
- `GET /incidents`
- `GET /incidents/recent?service_id=...`
- `GET /audit-logs?user_id=...`
- `GET /deployments/recent?service_id=...`
- `GET /feature-flags?service_id=...`
- `GET /sla-policies/{tier}`
- `POST /ticket-analysis`

## Sequencia de exercicios

Os exercicios ficam separados por dia em `exercises/`.

### Dia 1 - Integracao, tools e arquitetura

- `exercises/dia1/ex00.md`: validar setup, imports e dados.
- `exercises/dia1/ex01_mock_api.md`: explorar a Mock API do SupportOps.
- `exercises/dia1/ex02_tool_design_403.md`: case dos slides sobre tool design para ticket 403.
- `exercises/dia1/ex03_schema_wrapper.md`: implementar schema e wrapper de API.
- `exercises/dia1/ex04_prompt_carta.md`: escrever prompt operacional com C.A.R.T.A.
- `exercises/dia1/ex05_agent_loop.md`: executar loop LLM -> Tool -> Result.
- `exercises/dia1/ex06_supportops_architecture.md`: atividade dos slides sobre arquitetura do SupportOps Agent.
- `exercises/dia1/ex07_prompt_clinic.md`: refatorar prompt fraco no Prompt Clinic.
- `exercises/dia1/ex08_extra_cot_role_prompting.md`: extra com role prompting e CoT/plano resumido.

### Dia 2 - Memoria e RAG

- `exercises/dia2/ex08_memory_classification.md`: classificar onde cada informacao deve viver.
- `exercises/dia2/ex09_rag_chunking.md`: desenhar RAG para documentacao da analytics-api.
- `exercises/dia2/ex10_rag_retrieval.md`: implementar retrieval local com FAISS.
- `exercises/dia2/ex11_optional_query_rewriting_hyde.md`: opcional com query rewriting e HyDE.
- `exercises/dia2/ex12_optional_rag_eval_manual.md`: opcional com avaliacao manual de RAG.

### Dia 3 - Seguranca e avaliacao

- `exercises/dia3/ex11_guardrails.md`: implementar guardrails.
- `exercises/dia3/ex12_eval_dataset.md`: criar dataset de avaliacao do projetao.
- `exercises/dia3/ex13_deepeval.md`: avaliar com DeepEval local.
