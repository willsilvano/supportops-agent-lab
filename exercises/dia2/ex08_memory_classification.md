# Ex08 - Onde cada informacao deve viver?

## Contexto

Nem toda memoria longa e RAG. Nem todo dado deve ser salvo. O objetivo e classificar informacoes do SupportOps conforme uso, risco e forma de consulta.

## Cenario

O ticket 403 voltou a acontecer. O usuario pertence ao grupo `sales_manager`. Ha um runbook de roles, um incidente antigo resolvido e audit logs recentes.

## Tarefa

Classifique cada item:

- estado da sessao;
- memoria operacional persistente;
- memoria semantica/RAG;
- nao armazenar.

Itens:

1. Ticket atual.
2. Resultado de `check_user_access`.
3. Runbook de autenticacao.
4. Historico de incidente resolvido.
5. Feedback humano sobre a analise.
6. Token secreto colado no ticket.
7. Status do workflow de aprovacao.
8. Prompt injection encontrado em documento recuperado.

## Entrega

Uma tabela com classificacao e justificativa.

## Slides relacionados

- Slide 32: tipos praticos de memoria.
- Slide 33: memoria de sessao.
- Slide 34: memoria operacional persistente.
- Slide 35: memoria semantica vs RAG.
- Slide 37: exercicio de classificacao.

