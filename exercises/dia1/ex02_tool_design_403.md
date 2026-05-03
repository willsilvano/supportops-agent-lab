# Ex02 - Case pratico: ticket 403 no dashboard

## Contexto

Este exercicio corresponde diretamente ao case dos slides: **Case pratico: ticket 403 no dashboard**.

O ticket `TCK-4821` relata erro 403 no dashboard logo apos alteracao de role. O objetivo deste exercicio nao e implementar codigo ainda. O objetivo e transformar endpoints crus em capabilities seguras para um agente.

## Colinha - etapas de tool design

Use esta sequencia como checklist resumido dos slides 8 a 15:

1. Mapear necessidade
   - Antes de pensar em endpoint, pergunte: que decisao do agente exige dado externo?
   - No ticket 403: o agente precisa saber ticket, usuario, role, permissao, status do servico, incidentes e documentacao.

2. Desenhar capability
   - Uma tool boa expressa uma intencao de negocio, nao detalhes internos da API.
   - Prefira `check_user_access(user_id, resource)` a expor varias chamadas cruas de role, permissao e audit log.

3. Definir schema da tool
   - O schema e o contrato entre LLM e runtime.
   - Defina campos obrigatorios, tipos, descricoes, exemplos e rejeite propriedades extras quando possivel.

4. Implementar wrapper da API
   - O wrapper valida entrada, chama a API real e normaliza erros.
   - O LLM deve receber payload pequeno e limpo, nao a resposta crua do servico interno.

5. Escrever prompt operacional
   - O prompt define comportamento, autonomia, regras, tarefa e formato de saida.
   - Para esta semana, use C.A.R.T.A.: Contexto, Autonomia, Regras, Tarefa e Artefato/evidencia.

6. Executar loop LLM -> Tool -> Result
   - O modelo solicita a tool; o runtime valida, executa e devolve resultado.
   - O modelo nao executa HTTP, nao burla schema e nao chama tools fora da allowlist.

7. Validar resposta final
   - A resposta final precisa ser estruturada e validada por codigo.
   - Verifique schema, evidencias obrigatorias, risco, acoes proibidas e necessidade de aprovacao humana.

## Tarefa

Desenhe a integracao do agente para esse caso:

1. Escolha quais tools expor.
2. Defina o schema de entrada de cada tool.
3. Defina limites de autonomia.
4. Defina o JSON final esperado.
5. Separe o que fica em codigo/policy e o que fica em prompt.

## APIs disponiveis

```text
GET /tickets/{ticket_id}
GET /users/{user_id}
GET /users/{user_id}/roles
GET /access/check?user_id=...&resource=...
GET /services/{service_id}/status
GET /incidents/recent?service_id=...
GET /audit-logs?user_id=...
POST /tickets/{ticket_id}/notes
POST /ticket-analysis
```

## Entrega

Um Markdown com:

- lista de tools;
- schema resumido;
- limites de autonomia;
- output JSON;
- validacoes deterministicas.

## Slides relacionados

- Slide 10: desenhar capability.
- Slide 11: schema da tool.
- Slide 12: wrapper da API.
- Slide 17: codigo vs prompt.
- Slide 18: case pratico.
