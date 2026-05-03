# Exercicios por dia

Esta pasta acompanha a estrutura dos slides da Semana 4.

As pastas `solutions/` contem material do professor e estao ignoradas pelo `.gitignore` do repo. No scaffold inicial, alguns testes falham de proposito porque as funcoes correspondentes ainda tem `TODO` ou `NotImplementedError`; esses testes sao o contrato que os alunos devem fazer passar.

## Dia 1 - Integracao, tools e arquitetura

Foco: transformar APIs em tools seguras, definir contratos, prompts operacionais e arquitetura inicial do SupportOps Agent.

Cases dos slides cobertos diretamente:

- `dia1/ex02_tool_design_403.md`: **Case pratico: ticket 403 no dashboard**.
- `dia1/ex06_supportops_architecture.md`: **Atividade: arquitetura do SupportOps Agent**.
- `dia1/ex07_prompt_clinic.md`: **Prompt Clinic**.
- `dia1/ex08_extra_cot_role_prompting.md`: extra para Chain-of-Thought em 2026 e role prompting.

## Dia 2 - Memoria e RAG

Foco: classificar memoria, desenhar RAG para documentacao tecnica e implementar retrieval local com FAISS.

Cases dos slides cobertos diretamente:

- `dia2/ex08_memory_classification.md`: **Onde cada informacao deve viver?**
- `dia2/ex09_rag_chunking.md`: **Chat com documentacao da analytics-api**.
- `dia2/ex11_optional_query_rewriting_hyde.md`: opcional sobre query rewriting e HyDE.
- `dia2/ex12_optional_rag_eval_manual.md`: opcional sobre avaliacao manual de RAG.

## Dia 3 - Seguranca e avaliacao

Foco: guardrails, dataset de avaliacao e DeepEval local.

Cases dos slides cobertos diretamente:

- `dia3/ex12_eval_dataset.md`: **Dataset de avaliacao do projetao**.
- `dia3/ex13_deepeval.md`: **Exercicio final: avaliando com DeepEval**.
