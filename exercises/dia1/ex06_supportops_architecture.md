# Ex06 - Arquitetura do SupportOps Agent com D.E.C.I.D.E.

## Contexto

Este exercicio corresponde diretamente ao case dos slides: **Atividade: arquitetura do SupportOps Agent**.

A entrega nao e codigo. A entrega e um plano tecnico para um agente que analisa tickets de erro 403 no dashboard com tools, RAG, limites e avaliacao.

O Ex02 tratou o case menor de **tool design**. Agora o escopo aumenta: voce deve desenhar a arquitetura completa do agente, conectando integracao, prompt, RAG, guardrails e avaliacao.

## Tarefa

Use D.E.C.I.D.E.:

- Definir objetivo verificavel;
- Enumerar fontes de dados;
- Criar capabilities;
- Impor limites;
- Desenhar outputs;
- Evaluar comportamento.

## Escopo fechado

O agente deve:

- analisar tickets de erro 403 no dashboard;
- consultar usuario, role, permissao, servico, incidentes e audit logs;
- consultar documentacao tecnica via RAG;
- retornar recomendacao com evidencias.

O agente nao pode:

- alterar role;
- conceder permissao;
- fechar ticket.

## Entrega

Um plano em Markdown com:

- objetivo verificavel;
- fontes;
- tools;
- limites;
- output JSON;
- dataset minimo de avaliacao.

## Slides relacionados

- Slide 20: D.E.C.I.D.E.
- Slide 21: D.E.C.I.D.E. em detalhes.
- Slide 22: aplicando D.E.C.I.D.E.
- Slide 23: atividade de arquitetura.
