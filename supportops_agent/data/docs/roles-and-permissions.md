# Roles e permissoes da analytics-api

## Objetivo

Este documento descreve roles, permissoes e recursos usados pela `analytics-api`. Ele deve ser usado pelo agente para entender se a role atual de um usuario deveria permitir determinado acesso.

Ele nao autoriza mudancas. Qualquer alteracao de role ou permissao exige aprovacao humana e workflow auditavel.

## Modelo de permissao

Uma role contem uma ou mais permissoes.

Uma permissao combina:

- recurso;
- acao;
- escopo de tenant;
- restricoes opcionais.

Exemplo:

```json
{
  "resource": "dashboard:revenue",
  "action": "view"
}
```

## Recursos principais

### `dashboard:revenue`

Dashboard de receita comercial.

Requer permissao de visualizacao gerencial ou comercial.

### `dashboard:risk`

Dashboard de risco.

Requer role especifica de risco.

### `report:*`

Familia de relatorios.

Pode incluir visualizacao, exportacao e agendamento.

### `report:export`

Exportacao de relatorios.

Pode ter limites de volume, rate limit e fila assincrona.

## Role `sales_manager`

A role `sales_manager` deve permitir visualizar:

- `dashboard:revenue`;
- relatorios comerciais;
- metricas agregadas de vendas.

Permissoes esperadas:

- `PERM-DASHBOARD-REVENUE`;
- `PERM-REPORT-VIEW`.

Nao permite:

- `dashboard:risk`;
- administracao de usuarios;
- alteracao de role;
- configuracao global de tenant.

## Role `analyst`

A role `analyst` permite:

- visualizar relatorios;
- exportar relatorios dentro dos limites;
- acessar paineis operacionais nao gerenciais.

Pode nao permitir:

- `dashboard:revenue`;
- dashboards executivos;
- dashboard de risco;
- configuracoes administrativas.

## Role `risk_viewer`

A role `risk_viewer` permite visualizar:

- `dashboard:risk`;
- indicadores de risco;
- relatorios de compliance de leitura.

Nao permite:

- exportar relatorios sensiveis sem politica adicional;
- alterar configuracoes de risco;
- acessar dashboard comercial por padrao.

## Como diagnosticar permissao ausente

Sinais de permissao ausente:

- role atual nao contem permissao para o recurso;
- nao houve alteracao recente de role;
- `check_user_access` retorna `allowed=false`;
- nao ha incidente ou degradacao relacionada;
- outros usuarios com a role correta acessam normalmente.

Acao recomendada:

- nao conceder permissao automaticamente;
- recomendar revisao humana da role;
- anexar evidencias ao ticket.

## Como diagnosticar cache de permissao

Sinais de cache:

- role atual deveria permitir o recurso;
- houve alteracao recente de role;
- o erro comecou apos a alteracao;
- incidente historico menciona atraso de cache;
- status da `analytics-api` esta degradado ou houve atraso no consumidor de eventos.

Acao recomendada:

- solicitar invalidacao controlada do cache;
- pedir reteste;
- monitorar recurrence;
- registrar nota interna.

## Matriz resumida

| Role | Recurso permitido | Acao | Observacao |
|---|---|---|---|
| sales_manager | dashboard:revenue | view | Caso comum de gerentes comerciais |
| sales_manager | report:* | view | Relatorios comerciais |
| analyst | report:export | execute | Sujeito a rate limit |
| risk_viewer | dashboard:risk | view | Escopo de risco |

## Politica para agentes

O agente pode:

- explicar permissao esperada;
- comparar role atual com recurso solicitado;
- recomendar revisao humana.

O agente nao pode:

- alterar role;
- adicionar permissao;
- remover permissao;
- inferir permissao a partir de cargo textual sem consultar dados.

