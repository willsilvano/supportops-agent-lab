# Analytics API: catalogo de erros operacionais

## Objetivo

Este documento descreve erros comuns da `analytics-api`, como interpreta-los e quais evidencias coletar antes de recomendar uma acao.

O foco e evitar respostas plausiveis sem sustentacao. Todo diagnostico deve estar conectado a status do servico, logs, permissao efetiva, deploy recente ou runbook.

## HTTP 401

HTTP 401 indica falha de autenticacao.

Causas comuns:

- token expirado;
- token ausente;
- clock skew entre cliente e provedor de identidade;
- sessao invalida;
- ambiente errado.

Evidencias uteis:

- horario do erro;
- endpoint chamado;
- issuer do token;
- usuario autenticado;
- codigo de erro do identity provider.

Acao recomendada:

- orientar renovacao de sessao;
- validar ambiente;
- escalar para Identity Platform se houver muitos usuarios afetados.

## HTTP 403

HTTP 403 indica que a identidade foi reconhecida, mas a autorizacao efetiva negou o recurso.

Causas comuns:

- role sem permissao para o recurso;
- recurso fora do escopo do cliente;
- cache de permissoes atrasado apos alteracao de role;
- feature flag ativou novo caminho de autorizacao;
- politica de tenant bloqueou o acesso.

Evidencias uteis:

- role atual do usuario;
- permissoes associadas a role;
- recurso solicitado;
- audit logs recentes;
- incidentes recentes sobre cache de permissoes;
- feature flags relacionadas ao servico.

## Diferenca entre 403 por permissao e 403 por cache

403 por permissao:

- a role atual nao contem permissao para o recurso;
- nao ha alteracao de role recente;
- a checagem de acesso efetivo retorna `allowed=false`;
- a acao correta e solicitar revisao humana de permissao.

403 por cache:

- a role atual contem permissao;
- houve alteracao de role recente;
- audit logs mostram `role_updated`;
- incidente historico ou runbook menciona TTL de cache;
- a acao correta e invalidacao controlada ou aguardar propagacao.

## HTTP 404

HTTP 404 indica recurso inexistente ou nao visivel para aquele escopo.

Causas comuns:

- dashboard removido;
- slug errado;
- tenant errado;
- recurso ainda nao replicado.

Antes de responder, confirme se o usuario esta no tenant correto.

## HTTP 409

HTTP 409 indica conflito de estado.

Causas comuns:

- job de exportacao ja em andamento;
- dashboard sendo recalculado;
- alteracao concorrente de configuracao.

Acao recomendada:

- nao repetir operacao indefinidamente;
- verificar idempotencia;
- orientar aguardar job anterior ou cancelar com aprovacao.

## HTTP 429

HTTP 429 indica rate limit.

Evidencias uteis:

- cliente;
- usuario;
- endpoint;
- janela de tempo;
- correlation id.

Acao recomendada:

- reduzir frequencia;
- usar backoff;
- escalar se o cliente tiver SLA enterprise e impacto amplo.

## HTTP 500

HTTP 500 indica falha interna.

Nao conclua que e erro do usuario. Consulte status do servico, incidentes e deploys recentes.

## HTTP 504

HTTP 504 indica timeout.

Timeouts em exportacao costumam estar ligados a fila de relatorios, consulta pesada ou deploy recente.

Evidencias uteis:

- tamanho do relatorio;
- periodo consultado;
- status da fila;
- deploy recente;
- feature flag de exportacao assincrona.

## Politica para agentes

O agente pode recomendar diagnostico e proximos passos.

O agente nao pode:

- executar retry agressivo;
- alterar permissao;
- desligar feature flag;
- fechar ticket sem confirmacao;
- prometer resolucao sem evidencia.

## Resposta esperada para erro 403 no dashboard

Uma resposta madura deve dizer:

- qual hipotese e mais provavel;
- quais evidencias sustentam a hipotese;
- que acao segura deve ser tomada;
- qual acao nao deve ser automatizada;
- se e necessaria aprovacao humana.

