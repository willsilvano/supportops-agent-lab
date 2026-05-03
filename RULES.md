# Regras do Laboratorio

Este repositorio e um scaffold didatico. O objetivo e praticar integracao de agentes com sistemas reais, nao criar um framework generico.

## O que preservar

- Preserve contratos publicos dos exercicios.
- Preserve formato de retorno dos schemas.
- Preserve os IDs dos dados mockados usados nos testes.
- Preserve a separacao entre codigo deterministico e comportamento de LLM.

## O que implementar

- Implemente somente o necessario para cada exercicio.
- Use Pydantic para contratos.
- Use FastAPI para a Mock API.
- Use Gemini nos exercicios com LLM real.
- Use FAISS para RAG local.
- Use DeepEval localmente no exercicio final.

## Limites de autonomia do agente

Nesta semana, o agente pode:

- consultar tickets, usuarios, roles, servicos, incidentes, audit logs e docs;
- criar nota interna controlada;
- gerar analise estruturada.

Nesta semana, o agente nao pode:

- alterar role;
- fechar ticket;
- modificar permissao;
- executar acao irreversivel sem aprovacao humana.

