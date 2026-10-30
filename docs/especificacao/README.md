# Backend local da pesquisa sobre acessibilidade em streaming — especificação

Pedido do Issei em 30/10/2026. Só especificação; nada foi implementado.

## Recomendação em sete linhas

1. **SQLite, não base de grafos.** O problema é integridade e procedência, não consulta de grafo. O Minigraf 2.0.11 tem um defeito que perde valores em relações múltiplas (reproduzido aqui) e bloqueia leitura por outro processo.
2. **Python com biblioteca padrão**, servidor MCP por stdio no mesmo padrão do `knowledge-os`.
3. **O LLM orquestra e não lê respostas** (decisão do Issei, 30/10/2026). O MCP só devolve estrutura, ids, metadados e agregados; a codificação assistida usa regras determinísticas que o LLM propõe. A pessoa lê, recorta e decide pela CLI.
4. **Instrumento versionado.** O JSON da página traz só ids de campo; o texto das perguntas vem do HTML de um commit fixo.
5. **Natureza da base travada** (fictícia ou real), com aviso em toda saída fictícia.
6. **Núcleo genérico, estudo como pacote de dados.** Outra pesquisa com formulário entra como um pacote novo, sem mudar o núcleo.
7. **Reaproveitamento do `knowledge-os` por cópia registrada** de três arquivos de infraestrutura; nada que devolva texto.

## Documentos

| Arquivo | Conteúdo | Entregáveis do pedido |
| :-- | :-- | :-- |
| [`01-especificacao.md`](01-especificacao.md) | Especificação técnica completa | 1–6, 8, 9, 11–19 |
| [`02-contratos-mcp.md`](02-contratos-mcp.md) | Envelope, erros, idempotência, contrato de cada ferramenta, comandos da CLI | 9, 10 |
| [`03-adrs.md`](03-adrs.md) | Nove decisões de arquitetura propostas | 3, 6, 8 |
| [`04-avaliacao-minigraf.md`](04-avaliacao-minigraf.md) | Avaliação do Minigraf com fatos verificados | 7 |
| [`05-metacognicao.md`](05-metacognicao.md) | Metacognição sobre repositório, abstração e reaproveitamento do `knowledge-os` | 3, 15, 16, 19 |
| [`anexos/`](anexos/) | JSON fictício de exemplo e scripts de sondagem do Minigraf | — |

## Decisões

Tomadas pelo Issei em 30/10/2026: D-01, D-02, D-07, D-03, D-04, D-06 (ADRs aceitas), D-08 e D-09. Repositório: `issei/meikyu-caliope` (D-07). Em aberto, com a Liga antes da primeira importação real, D-05 e V-06. Guia: [`06-decisoes-pendentes.md`](06-decisoes-pendentes.md).
