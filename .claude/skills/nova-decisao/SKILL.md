---
name: nova-decisao
description: Como registrar uma decisão de arquitetura (ADR-ps-xxx) ou uma decisão que cabe ao Issei (D-xx) no meikyu-caliope. Use quando uma mudança cruza uma fronteira da especificação, exige dependência nova ou muda uma invariante.
---

# Nova decisão

## Quando é ADR e quando é D-xx

| Situação | Registro |
| :-- | :-- |
| Escolha técnica com alternativas e consequências | ADR em `docs/especificacao/03-adrs.md` |
| Escolha que muda o objetivo, o escopo, o risco aceito ou o dado tratado | D-xx em `docs/especificacao/06-decisoes-pendentes.md`, para o Issei |
| Mudança em invariante (`AGENTS.md` §1) | As duas: D-xx primeiro; a ADR só depois da resposta |

Nunca implemente uma decisão D-xx antes da resposta do Issei. Trabalhe na opção recomendada só se ela for reversível.

## ADR

Formato das ADRs existentes: **Contexto**, **Decisão**, **Motivos** ou **Alternativa recusada**, **Consequências**, **Reavaliar quando**.
Numeração contínua (`ADR-ps-010`, …). Estado inicial: proposta. Só o Issei aceita.

## D-xx

Formato do `06-decisoes-pendentes.md`: **O que é**, **Opções** numeradas com consequência, **Recomendação** e motivo.
Atualize a tabela de prioridade do topo do arquivo.

## Depois

- Atualize a especificação no mesmo PR, antes do código.
- O PR é "só documentação" e entra sozinho se a CI passar. Uma ADR aceita pelo Issei registra a data e "aceita pelo Issei em AAAA-MM-DD".
