---
id: CAL-AGENTICO-01
titulo: Como o repositório prepara e limita o trabalho de agentes
data: 2026-10-31
leitor: Issei, para revisar o que veio de cada repositório e o que ficou de fora
padrao_de_redacao: ABNT NBR ISO 24495-1 (linguagem simples) e ASD-STE100 adaptado ao PT-BR
---

# Desenvolvimento agêntico

## Para quem é e o que pede

Este documento é para você, Issei. Ele mostra quais práticas do `mauricio-site` e do `knowledge-os` entraram aqui, como foram adaptadas e quais ficaram de fora.
Nenhuma decisão é pedida. Leitura: cerca de 5 minutos.

## A ideia central

Neste projeto, o próprio agente de código é um cliente com acesso a arquivos. A ADR-ps-007 diz que o LLM não lê respostas.
Por isso, a configuração do agente aplica a barreira ao agente: ele não lê a pasta de dados, não abre a base SQLite e não grava dado de resposta sem marca de fixture.

## O que entrou

| Prática | De onde veio | Como ficou aqui |
| :-- | :-- | :-- |
| `CLAUDE.md` que só importa `AGENTS.md` | `mauricio-site` | `AGENTS.md` com invariantes, SDD, comandos, Git e mapa de pastas |
| Skill "fonte da verdade" de padrões | `mauricio-site` (`mauricio-site-patterns`) | `caliope-padroes` |
| Skill do quality gate, com limite de tentativas e *fail-closed* | `mauricio-site` (`run-quality-gate`, `.ai/`) | `verificar` e `scripts/verificar.py` |
| Hook `PreToolUse` que protege arquivos | `mauricio-site` (`guard-protected-files.mjs`) | `scripts/hooks/guarda.py`: pasta de dados, SQLite, `sqlite3`, dados D1–D5 |
| Hook `PostToolUse` que confere o arquivo gravado | `mauricio-site` (`guard-ap-tokens.mjs`) | O mesmo `guarda.py` confere D3–D5 depois de um Edit |
| Hook `Stop` que roda o gate quando o código mudou | `mauricio-site` (`stop-gate.mjs`) | `scripts/hooks/stop.py`; não entra em laço (`stop_hook_active`) |
| Permissões `allow` para os comandos de verificação | `mauricio-site` (`.claude/settings.json`) | Mais uma lista `deny` para a pasta de dados, `*.sqlite`, `.env` e `sqlite3` |
| Agentes revisores só de leitura | `mauricio-site` (`tone-reviewer`, `fde-evidence-auditor`) | `revisor-barreira`, `auditor-dados`, `revisor-redacao` |
| Mesma regra no agente e na CI | `mauricio-site` (`guard-ap-tokens` + teste) | `check_dados.py` é usado pelo hook e pelo job `dados` |
| SDD: especificação antes do código | `mauricio-site` (`docs/specs/`), `knowledge-os` (Fase 0) | `AGENTS.md` §2 e skill `nova-decisao` |
| ADRs com prefixo próprio | os dois | `ADR-ps-xxx` em `docs/especificacao/03-adrs.md` |
| CI que classifica a mudança e roda só o necessário | `knowledge-os` | `classify_changes.py` adaptado; todo arquivo de dado conta como sistema |
| Verificação de links dos `.md` | `knowledge-os` | `check_docs.py` copiado |
| Job de resumo `CI ok` e `!cancelled()` | `knowledge-os` (lição do PR #14) | Igual, com teste |
| Merge automático com `--match-head-commit` | `knowledge-os` | Só para PR só de documentação (D-08) |
| Testes dos próprios scripts de CI | `knowledge-os` (`test_ci_scripts.py`) | `tests/repositorio/test_scripts.py`, que também cobre os hooks |
| Redação em linguagem simples, ASD-STE100 e Lean | `knowledge-os` (regra de 22/10/2026) | Skill `redigir-documento` e agente `revisor-redacao` |
| Cabeçalho `id`/`titulo`/`data`/`leitor`/`padrao_de_redacao` | `knowledge-os` (retrospectiva, BL-20) | Em todo documento novo de `docs/` |
| Registro de aprendizados, só de inclusão | `mauricio-site` (`.ai/learnings.md`) | `docs/aprendizados.md`, já com as lições dos dois repositórios |
| Cópia registrada de código | `knowledge-os` → ADR-ps-008 | Skill `copiar-do-knowledge-os` e `docs/origem-do-codigo.md` |
| Runner fixo quando a ferramenta depende da imagem | `mauricio-site` (PR #125) | Registrado em `docs/aprendizados.md`; hoje não é necessário |

Acréscimos sem equivalente nos outros repositórios:

- `.gitattributes` com LF e anexos binários, para o hash do exemplo não mudar no Windows.
- Matriz de testes com Windows obrigatório (RNF-01).
- Modelo de PR com as invariantes do projeto.
- `ruff.toml` mínimo (a especificação, §16, escolhe o `ruff`).

## O que ficou de fora, e por quê

| Prática | Motivo |
| :-- | :-- |
| Memória OKF em `knowledge/` (`mauricio-site`) | O projeto ainda não tem conhecimento durável fora da especificação. `docs/aprendizados.md` basta por enquanto. |
| CodeGraph (`mauricio-site`) | É decisão local, por máquina. `.codegraph/` já está no `.gitignore`. |
| `.mcp.json` com servidores de terceiros (`mauricio-site`: context7) | Outro servidor MCP com acesso a arquivos pode contornar a barreira (limite da ADR-ps-007). O `.mcp.json` do próprio `caliope` entra na etapa E2, apontando só para a base fictícia (ADR-ps-006). |
| Gêmeo em inglês, acessibilidade de páginas, design system (`mauricio-site`) | Não há interface web neste projeto. |
| Release automático (`knowledge-os`) | Ainda não há pacote. Entra quando houver `pyproject.toml`. |
| Merge automático de código (`knowledge-os`) | Decisão D-08 do Issei: código espera por ele. |
| Benchmark e golden set (`knowledge-os`) | Não há sistema de busca para medir. A lição de revisão independente está em `docs/aprendizados.md`. |

## Limites conhecidos

- O hook procura a pasta de dados pelo nome `pesquisa-streaming`. Se a pasta mudar de nome, atualize `scripts/hooks/guarda.py` e as regras `deny`.
- Um comando de terminal com `.sqlite` no texto é bloqueado, mesmo quando só procura texto. Use a ferramenta de busca do agente (Grep), que é permitida.
- Os hooks chamam `python`. No Windows, ative a venv do projeto ou instale o Python com a opção de PATH. Sem `python`, o hook falha sem bloquear; a CI continua aplicando as regras de dados.
- O hook vale para o Claude Code. Outro agente precisa ler `AGENTS.md` e respeitar as mesmas regras; a CI é a última linha de defesa.
