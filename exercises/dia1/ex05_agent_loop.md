# Ex05 - Executar loop LLM -> Tool -> Result

## Contexto

O modelo pode decidir que precisa de uma tool, mas quem valida e executa a chamada e o runtime da aplicacao.

Neste exercicio, o fluxo ainda e estreito e deterministico para facilitar teste.

## Arquivos permitidos

```text
supportops_agent/tools/ticket_tools.py
supportops_agent/agent/output_schemas.py
supportops_agent/agent/state.py
supportops_agent/agent/nodes.py
supportops_agent/agent/graph.py
```

## Contrato

Implemente os contratos e o fluxo:

1. `TicketContextInput` e `TicketContextResult`;
2. `get_ticket_context(payload, client=None)`;
3. `Evidence` e `TicketAnalysis`;
4. `fetch_ticket_node`;
5. `check_access_node`;
6. `analyze_node`;
7. `run_supportops_flow`.

O fluxo deve:

1. recebe `Analise o ticket TCK-4821`;
2. busca contexto do ticket;
3. checa acesso do usuario ao recurso;
4. monta evidencias;
5. retorna JSON validado por `TicketAnalysis`.

Observacao:

- O Ex03 ja implementou `check_user_access`.
- Neste exercicio, voce conecta essa capability ao fluxo do agente.

## Validacao

```bash
python run.py test ex05
```

## Slides relacionados

- Slide 14: executar loop LLM -> Tool -> Result.
- Slide 15: validar resposta final.
- Slide 19: o que cada no garante.
