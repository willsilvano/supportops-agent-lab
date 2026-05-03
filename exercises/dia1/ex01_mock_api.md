# Ex01 - Explorar a Mock API do SupportOps

## Contexto

O SupportOps Agent nao deve responder apenas com prompt. Ele precisa consultar sistemas externos. Neste laboratorio, esses sistemas sao representados por uma API FastAPI mockada, mas com endpoints HTTP reais.

## Tarefa

1. Suba a API mockada.
2. Abra a documentacao interativa.
3. Consulte o ticket `TCK-4821`.
4. A partir do ticket, consulte:
   - usuario;
   - roles;
   - permissao efetiva;
   - status do servico;
   - incidentes recentes.
5. Explique quais dados mudariam a resposta do agente.

## Comandos

```bash
python run.py mock-api
```

Em outro terminal:

```bash
python run.py test ex01
```

Docs:

```text
http://127.0.0.1:8000/docs
```

## Entrega

Um pequeno resumo com:

- ticket analisado;
- usuario afetado;
- recurso solicitado;
- status da permissao;
- status do servico;
- incidente recente mais relevante.

## Slides relacionados

- Slide 3: O cenario central: SupportOps Agent.
- Slide 8: Workflow de integracao LLM + API.
- Slide 9: Etapa 1 - Mapear necessidade.

