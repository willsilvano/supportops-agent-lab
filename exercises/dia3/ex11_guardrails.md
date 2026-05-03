# Ex11 - Guardrails de input, tool call e output

## Contexto

No Dia 3, o agente ja consulta APIs e RAG. Agora ele pode causar dano se aceitar instrucoes maliciosas ou chamar tools proibidas.

## Arquivo permitido

```text
supportops_agent/tools/guardrail_tools.py
```

## Tarefa

Implemente guardrails deterministicas para:

1. detectar prompt injection simples;
2. validar allowlist de tools;
3. bloquear tools proibidas;
4. rejeitar output final que recomenda acao proibida.

## Validacao

```bash
python run.py test ex11
```

## Slides relacionados

- Slide 48: riscos em agentes reais.
- Slide 49: defesas deterministicas.
- Slide 51: prompt injection.
- Slide 52: guardrails.
- Slide 53: controle de acesso e autonomia.

