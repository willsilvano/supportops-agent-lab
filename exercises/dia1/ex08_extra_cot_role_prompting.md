# Ex08 extra - Role prompting e CoT aplicado aos prompts do Dia 1

## Contexto

Este exercicio extra conversa com a parte final do Dia 1, especialmente Prompt Clinic, Chain-of-Thought em 2026 e role prompting.

A ideia nao e pedir para o modelo expor uma cadeia longa de raciocinio. Em producao, prefira pedir um plano resumido, criterios de decisao, validacoes e evidencias.

## Ponto de partida

Use os prompts produzidos nos exercicios anteriores:

- Ex04: prompt operacional com C.A.R.T.A.
- Ex07: Prompt Clinic.

## Tarefa

Crie tres variantes do prompt para o caso `TCK-4821`:

1. Prompt base
   - Usa C.A.R.T.A.
   - Nao adiciona role prompting alem do papel operacional basico.

2. Prompt com role prompting operacional
   - Define explicitamente o agente como suporte tecnico N2.
   - Explica responsabilidades, ferramentas autorizadas e limites de autonomia.

3. Prompt com plano resumido e criterios de validacao
   - Pede para o modelo produzir internamente uma analise estruturada.
   - Na resposta final, pede apenas plano resumido, criterios, evidencias e JSON.
   - Nao pede cadeia de pensamento completa.

## Teste manual com Gemini

Execute as tres variantes com a mesma entrada:

```text
Analise o ticket TCK-4821. O usuario recebe 403 no dashboard depois de alteracao de role.
```

Compare:

- a resposta usa evidencias?
- a resposta respeita os limites de autonomia?
- a resposta evita alterar role ou fechar ticket?
- a resposta fica mais verificavel?
- o JSON final continua valido?

## Entrega

Um Markdown com:

- as tres variantes do prompt;
- a resposta obtida em cada variante;
- uma tabela comparando qualidade, seguranca e aderencia ao schema;
- uma conclusao sobre qual prompt voce usaria em producao.

## Slides relacionados

- Slide 25: Prompt Clinic.
- Slide 26: Chain-of-Thought.
- Slide 27: Chain-of-Thought em 2026.
- Slide 28: Role prompting.
- Slide 29: LangChain, templates e guardrails.

