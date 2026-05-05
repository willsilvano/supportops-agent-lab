# Ex02 - Entrega: Tool Design para Ticket 403 no Dashboard

## Cenário

Ticket `TCK-4821`: usuário reporta erro 403 no dashboard logo após alteração de role.
O agente precisa diagnosticar a causa raiz e propor resolução.

---

## 1. Lista de Tools

| # | Tool | Intenção de negócio | APIs internas consumidas |
|---|------|---------------------|--------------------------|
| 1 | `get_ticket_context` | Obter contexto completo do ticket (dados do ticket + usuário + notas) | `GET /tickets/{id}`, `GET /users/{id}`, `GET /tickets/{id}/notes` |
| 2 | `check_user_access` | Verificar se o usuário tem acesso ao recurso reportado | `GET /access/check`, `GET /users/{id}/roles`, `GET /audit-logs` |
| 3 | `get_service_health` | Verificar se o serviço está saudável e se há incidentes recentes | `GET /services/{id}/status`, `GET /incidents/recent` |
| 4 | `search_docs` | Buscar documentação relevante (runbooks, permissões) | `GET /docs`, `GET /docs/{slug}` |
| 5 | `submit_analysis` | Registrar a análise final estruturada do agente | `POST /ticket-analysis` |
| 6 | `add_ticket_note` | Adicionar nota interna ao ticket com achados | `POST /tickets/{id}/notes` |

---

## 2. Schema Resumido de Cada Tool

### get_ticket_context

```json
{
  "name": "get_ticket_context",
  "description": "Recupera contexto enriquecido do ticket: dados do ticket, informações do usuário afetado e notas existentes.",
  "parameters": {
    "type": "object",
    "properties": {
      "ticket_id": {
        "type": "string",
        "description": "ID do ticket (ex: TCK-4821)",
        "pattern": "^TCK-\\d+$"
      }
    },
    "required": ["ticket_id"],
    "additionalProperties": false
  }
}
```

### check_user_access

```json
{
  "name": "check_user_access",
  "description": "Verifica se um usuário possui acesso a um recurso específico. Retorna status de acesso, roles atuais e últimas alterações de permissão no audit log.",
  "parameters": {
    "type": "object",
    "properties": {
      "user_id": {
        "type": "string",
        "description": "ID do usuário a verificar (ex: USR-001)"
      },
      "resource": {
        "type": "string",
        "description": "Recurso alvo (ex: dashboard, admin-panel, billing)"
      }
    },
    "required": ["user_id", "resource"],
    "additionalProperties": false
  }
}
```

### get_service_health

```json
{
  "name": "get_service_health",
  "description": "Verifica status operacional do serviço e incidentes recentes que possam explicar o erro.",
  "parameters": {
    "type": "object",
    "properties": {
      "service_id": {
        "type": "string",
        "description": "ID do serviço (ex: SVC-AUTH, SVC-DASHBOARD)"
      }
    },
    "required": ["service_id"],
    "additionalProperties": false
  }
}
```

### search_docs

```json
{
  "name": "search_docs",
  "description": "Busca documentação interna relevante para o diagnóstico (runbooks, guias de permissões).",
  "parameters": {
    "type": "object",
    "properties": {
      "query": {
        "type": "string",
        "description": "Termo de busca (ex: 'role change 403', 'auth permissions')",
        "maxLength": 200
      }
    },
    "required": ["query"],
    "additionalProperties": false
  }
}
```

### submit_analysis

```json
{
  "name": "submit_analysis",
  "description": "Submete a análise final estruturada do ticket. Requer evidências coletadas nas etapas anteriores.",
  "parameters": {
    "type": "object",
    "properties": {
      "ticket_id": {
        "type": "string",
        "description": "ID do ticket analisado"
      },
      "risk": {
        "type": "string",
        "enum": ["low", "medium", "high", "critical"],
        "description": "Nível de risco da situação"
      },
      "summary": {
        "type": "string",
        "description": "Resumo da análise e causa raiz identificada",
        "maxLength": 2000
      },
      "evidence": {
        "type": "array",
        "items": { "type": "string" },
        "description": "Lista de evidências que suportam a conclusão"
      }
    },
    "required": ["ticket_id", "risk", "summary", "evidence"],
    "additionalProperties": false
  }
}
```

### add_ticket_note

```json
{
  "name": "add_ticket_note",
  "description": "Adiciona nota interna ao ticket com os achados do agente.",
  "parameters": {
    "type": "object",
    "properties": {
      "ticket_id": {
        "type": "string",
        "description": "ID do ticket"
      },
      "author": {
        "type": "string",
        "description": "Identificador do autor (ex: supportops-agent)",
        "maxLength": 80
      },
      "body": {
        "type": "string",
        "description": "Conteúdo da nota",
        "maxLength": 1000
      }
    },
    "required": ["ticket_id", "author", "body"],
    "additionalProperties": false
  }
}
```

---

## 3. Limites de Autonomia

| Ação | Autonomia | Justificativa |
|------|-----------|---------------|
| Ler dados (tickets, users, roles, logs) | ✅ Autônomo | Somente leitura, sem efeito colateral |
| Verificar acesso e saúde do serviço | ✅ Autônomo | Consulta diagnóstica |
| Buscar documentação | ✅ Autônomo | Somente leitura |
| Adicionar nota interna ao ticket | ✅ Autônomo | Baixo risco, rastreável |
| Submeter análise final | ✅ Autônomo | Registro estruturado, não altera estado do usuário |
| Alterar role/permissão do usuário | ❌ Requer aprovação humana | Ação destrutiva, impacto em acesso |
| Escalar para engenharia | ❌ Requer aprovação humana | Envolve outro time |
| Fechar/resolver ticket | ❌ Requer aprovação humana | Decisão final de negócio |
| Contatar o usuário diretamente | ❌ Requer aprovação humana | Comunicação externa |

**Regra geral:** O agente pode investigar e registrar, mas NÃO pode remediar (alterar permissões, roles, status de serviço) sem aprovação humana.

---

## 4. Output JSON Esperado (Resposta Final do Agente)

```json
{
  "ticket_id": "TCK-4821",
  "status": "analyzed",
  "risk": "medium",
  "root_cause": "Role alterada de 'editor' para 'viewer' removeu permissão 'dashboard:read' necessária para acessar o painel.",
  "summary": "Usuário USR-042 perdeu acesso ao dashboard após alteração de role realizada em 2025-01-15T10:30:00Z. O audit log confirma a mudança de role. O serviço de auth está operacional, sem incidentes ativos.",
  "evidence": [
    "audit_log: role_change USR-042 editor -> viewer em 2025-01-15T10:30:00Z",
    "access_check: USR-042 denied para resource 'dashboard'",
    "service_status: SVC-AUTH operational",
    "incidents_recent: nenhum incidente ativo para SVC-AUTH"
  ],
  "recommended_actions": [
    {
      "action": "restore_role",
      "description": "Restaurar role 'editor' para USR-042",
      "requires_approval": true
    }
  ],
  "confidence": 0.92,
  "requires_human_approval": true
}
```

---

## 5. Separação: Código/Policy vs. Prompt

### Fica em CÓDIGO / POLICY (determinístico)

| Responsabilidade | Implementação |
|------------------|---------------|
| Validação de schema de entrada | Pydantic `BaseModel` com `Field` constraints |
| Validação de schema de saída | Pydantic model para o JSON final |
| Allowlist de tools | Lista fixa no runtime; LLM não pode chamar tool fora dela |
| Rate limiting | Middleware no runtime (max 10 tool calls por execução) |
| Bloqueio de ações destrutivas | Código verifica `requires_approval` antes de executar |
| Normalização de respostas da API | Wrapper retorna payload limpo, sem dados internos |
| Timeout de execução | Configuração no runtime (ex: 30s por tool call) |
| Auditoria | Log de toda tool call com timestamp, input e output |
| Campos obrigatórios na análise final | Validação Pydantic: `ticket_id`, `risk`, `summary`, `evidence` não-vazia |
| Sanitização de dados sensíveis | Wrapper remove campos como tokens, senhas, PII desnecessária |

### Fica em PROMPT (flexível, ajustável)

| Responsabilidade | Onde no prompt (C.A.R.T.A.) |
|------------------|------------------------------|
| Persona e tom | **C**ontexto: "Você é um agente de suporte L2..." |
| Limites de autonomia em linguagem natural | **A**utonomia: "Você pode investigar mas não remediar" |
| Ordem de investigação sugerida | **T**arefa: "1. Obtenha contexto do ticket, 2. Verifique acesso..." |
| Regras de negócio interpretativas | **R**egras: "Se risco >= high, sempre recomende aprovação humana" |
| Formato de saída desejado | **A**rtefato: "Responda no JSON especificado" |
| Quando escalar | **R**egras: "Se não encontrar causa raiz em 3 iterações, escale" |
| Critérios de confiança | **R**egras: "confidence < 0.7 → marque requires_human_approval = true" |

---

## Validações Determinísticas (executadas por código após resposta do LLM)

```python
def validate_agent_output(output: dict) -> list[str]:
    """Retorna lista de erros. Lista vazia = output válido."""
    errors = []

    # 1. Campos obrigatórios
    required = ["ticket_id", "risk", "summary", "evidence", "requires_human_approval"]
    for field in required:
        if field not in output:
            errors.append(f"Campo obrigatório ausente: {field}")

    # 2. Risk deve ser valor válido
    if output.get("risk") not in ("low", "medium", "high", "critical"):
        errors.append(f"risk inválido: {output.get('risk')}")

    # 3. Evidence não pode ser vazia
    if not output.get("evidence"):
        errors.append("evidence não pode ser vazia - agente deve citar fontes")

    # 4. Se risk >= high, requires_human_approval deve ser True
    if output.get("risk") in ("high", "critical"):
        if not output.get("requires_human_approval"):
            errors.append("risk alto/crítico exige requires_human_approval=true")

    # 5. Ações recomendadas destrutivas devem ter requires_approval=True
    for action in output.get("recommended_actions", []):
        destructive_keywords = ["restore", "change", "delete", "revoke", "grant"]
        if any(kw in action.get("action", "") for kw in destructive_keywords):
            if not action.get("requires_approval"):
                errors.append(f"Ação destrutiva '{action['action']}' sem requires_approval")

    # 6. Summary não pode exceder 2000 chars
    if len(output.get("summary", "")) > 2000:
        errors.append("summary excede 2000 caracteres")

    return errors
```

---

## Fluxo Resumido do Agente

```
┌─────────────┐
│   Ticket    │
│  TCK-4821   │
└──────┬──────┘
       │
       ▼
┌──────────────────┐
│ get_ticket_context│  → Contexto: ticket + user + notas
└──────┬───────────┘
       │
       ▼
┌──────────────────┐
│ check_user_access │  → Acesso negado? Roles? Audit log?
└──────┬───────────┘
       │
       ▼
┌──────────────────┐
│ get_service_health│  → Serviço OK? Incidentes?
└──────┬───────────┘
       │
       ▼
┌──────────────────┐
│   search_docs    │  → Runbook relevante?
└──────┬───────────┘
       │
       ▼
┌──────────────────┐
│  submit_analysis │  → JSON final validado
└──────┬───────────┘
       │
       ▼
┌──────────────────┐
│  add_ticket_note │  → Nota interna com achados
└──────────────────┘
```
