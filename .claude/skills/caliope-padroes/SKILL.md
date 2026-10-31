---
name: caliope-padroes
description: Fonte da verdade das convenções de código do meikyu-caliope — organização do pacote caliope, erros, eventos, MCP, testes e fixtures. Use antes de criar ou alterar qualquer arquivo em src/, tests/ ou estudos/.
---

# Padrões do `caliope`

Leia `AGENTS.md` §1 (invariantes) antes desta skill. Aqui estão as convenções que tornam as invariantes verificáveis.

## Onde cada coisa mora

A estrutura está em `docs/especificacao/01-especificacao.md` §15. Resumo:

- `src/caliope/leitores/pagina_v1.py` é o **único** lugar que conhece o JSON da página. O resto do núcleo vê o modelo normalizado.
- `src/caliope/mcp/` é a única porta para o LLM. Nada fora dela fala MCP.
- `src/caliope/cli/` contém as ações humanas: aceitar, rejeitar, expurgar, restaurar, ler texto e identificação.
- `estudos/<estudo>/` contém dados do estudo (instrumento, normalização, análises). O núcleo não importa nada de lá pelo nome.

## Regras de código

1. **Só biblioteca padrão** em `src/`. Uma dependência nova de execução precisa de ADR.
2. **Erros com código do catálogo** (`erros.py`, modelo do `knowledge-os`). O catálogo é igual ao de `02-contratos-mcp.md`; um teste compara os dois. Mensagem de erro nunca repete o valor recebido quando ele pode ser texto de resposta.
3. **Evento antes do resultado.** Toda escrita grava o evento (`eventos/registrar.py`) na mesma transação. O registro de eventos é só de inclusão (ADR-ps-003).
4. **Determinismo.** Ordene tudo que sai (chaves, listas por id). Não use hora local, locale nem `hash()` do Python em resultado. Hash é SHA-256 sobre forma canônica.
5. **Caminhos.** Use `pathlib`. Recuse `..`, caminho absoluto e unidade (`C:`) onde a especificação pede só nome de arquivo (RNF-05). Teste com espaço e acento no caminho.
6. **Texto.** Leia e grave com `encoding="utf-8"` explícito. Normalize para NFC na camada normalizada; o bruto fica como chegou (ADR-ps-002).
7. **Docstring do módulo** diz o que ele faz e a quais RF, RNF ou ADR atende.

## Regras do MCP (ADR-ps-005, ADR-ps-007)

- Toda ferramenta declara `inputSchema` e `outputSchema`, e todo resultado traz `natureza`.
- A projeção SQL de uma ferramenta MCP **lista colunas**. Nunca `SELECT *`. Nenhuma coluna de texto de resposta, situação, trecho ou identificação.
- A importação pelo MCP recebe só nome de arquivo dentro de `entrada/`.
- Ferramenta nova = teste de contrato (subprocesso, entrada válida e inválida, saída valida no `outputSchema`) + entrada no teste de vazamento (RF-24).
- Peça revisão ao agente `revisor-barreira` antes do PR.

## Testes

- Camadas e pastas: `01-especificacao.md` §17.2. Testes de CI e hooks ficam em `tests/repositorio/`.
- Fixtures em `tests/fixtures/ficticio/`, com `"_fixture": true` em cada arquivo. Não altere bytes de fixture com hash registrado.
- Teste verifica estrutura e invariantes (contagens, hashes, estados). Nunca uma "descoberta" de pesquisa (§17.3).
- Base de teste em pasta temporária (`tempfile.TemporaryDirectory`). Nunca na pasta de dados do usuário.

## Antes de terminar

Rode a skill `verificar`. Se copiou algo do `knowledge-os`, siga a skill `copiar-do-knowledge-os`.
