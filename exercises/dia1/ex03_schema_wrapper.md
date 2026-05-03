# Ex03 - Implementar schema e wrapper de API

## Contexto

Uma capability segura nao deve entregar a resposta crua da API ao LLM. O wrapper valida entrada, chama a API e normaliza a saida.

## Arquivos permitidos

```text
supportops_agent/tools/access_tools.py
```

## Contrato

Implemente ou revise:

```python
CheckUserAccessInput
CheckUserAccessResult
check_user_access(payload, client=None)
```

Regras:

- `user_id` e `resource` sao obrigatorios.
- entradas vazias devem falhar em validacao Pydantic;
- `CheckUserAccessResult` deve ser o contrato normalizado retornado ao agente;
- a funcao deve chamar `client.check_access`;
- o retorno deve conter `user_id`, `resource`, `allowed`, `roles`, `matched_permissions` e `error`;
- a resposta crua da API nao deve ser repassada integralmente ao LLM.

## Validacao

```bash
python run.py test ex03
```

## Slides relacionados

- Slide 11: schema da tool.
- Slide 12: wrapper da API.
- Slide 15: validar resposta final.
