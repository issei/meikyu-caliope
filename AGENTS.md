# meikyu-caliope — protocolo do agente

Este arquivo é a diretiva principal para qualquer agente que trabalha neste repositório.
O `CLAUDE.md` só importa este arquivo.

O produto é um backend local para pesquisa qualitativa: importa respostas de entrevistas em JSON, guarda tudo em SQLite e oferece um servidor MCP por stdio.
Pacote e comando: `caliope`. Primeiro estudo: acessibilidade em streaming (Liga Web Para Todos).
Especificação completa: [`docs/especificacao/`](docs/especificacao/README.md).

---

## 1. Invariantes (não negociáveis)

Estas regras valem para você, agente, e não só para o código que você escreve.

1. **O LLM não lê respostas** ([ADR-ps-007](docs/especificacao/03-adrs.md)). Isso inclui você.
   Não abra a pasta de dados nem a base SQLite. Não use `sqlite3`. Não peça à pessoa que cole uma resposta no chat.
   O hook `scripts/hooks/guarda.py` bloqueia essas ações. Se ele bloquear, não procure outro caminho: pare e diga o que precisa.
2. **Nenhum dado real no repositório.** Só fixtures fictícias, marcadas com `"_fixture": true` ou com hash em `scripts/ci/ficticios.sha256`.
   `scripts/ci/check_dados.py` aplica isso no hook e na CI.
3. **Nenhuma saída do MCP contém texto** de resposta, situação, trecho ou identificação. Toda ferramenta nova tem teste de vazamento (RF-24).
4. **A natureza da base é fixa** (`ficticio` ou `real`, ADR-ps-006). Nenhum código muda a natureza. Saída fictícia leva o aviso de demonstração.
5. **Decisão de interpretação é humana e passa pela CLI** (ADR-ps-004). Nenhuma ferramenta MCP aceita, rejeita, retira, restaura ou expurga.
6. **Só biblioteca padrão em execução.** `pytest`, `ruff` e `jsonschema` são só de desenvolvimento.
7. **Núcleo genérico** (ADR-ps-009). `src/caliope/` não cita o estudo de streaming. O estudo vive em `estudos/`.

## 2. Desenvolvimento guiado por especificação

- A especificação vem antes do código. Se o requisito mudar, atualize `docs/especificacao/` **antes** do código, no mesmo PR.
- Todo código aponta para o requisito que atende (RF-xx, RNF-xx, AN-xx, ADR-ps-xxx) no docstring do módulo ou do teste.
- Decisão nova de arquitetura vira ADR em `docs/especificacao/03-adrs.md`. Decisão que é do Issei vira item D-xx em `06-decisoes-pendentes.md`. Use a skill `nova-decisao`.
- Siga o roteiro (§18 da especificação): E1 → E2 → E3 → I2 → I3. Não adiante itens de etapa futura.
- Teste primeiro: escreva o teste que falha, depois o código.

## 3. Skills, agentes e hooks

Leia a skill antes da tarefa que ela cobre. Mapa completo: [`docs/desenvolvimento-agentico.md`](docs/desenvolvimento-agentico.md).

| Tarefa | Use |
| :-- | :-- |
| Qualquer mudança de código | skill `caliope-padroes` (fonte da verdade das convenções) |
| Antes de commit ou push | skill `verificar` |
| Copiar arquivo do `knowledge-os` | skill `copiar-do-knowledge-os` (ADR-ps-008) |
| Escrever ou revisar documento | skill `redigir-documento` |
| Nova ADR ou decisão para o Issei | skill `nova-decisao` |
| PR que toca `src/caliope/mcp/` | agente `revisor-barreira` |
| PR que toca fixtures, importação, exportação ou identificação | agente `auditor-dados` |
| PR com documento novo | agente `revisor-redacao` |

## 4. Comandos

```bash
python scripts/verificar.py            # tudo: dados, links, compilação, testes, ruff
python scripts/verificar.py --rapido   # sem ruff (é o que o hook Stop roda)
python scripts/ci/check_dados.py       # só o guarda de dados
```

No Windows, use a venv do projeto (`py -m venv .venv` e `.venv\Scripts\activate`). Os hooks chamam `python`, que precisa estar no PATH.

## 5. Git, PR e CI

- Commits convencionais em português: `feat(importacao): …`, `fix(mcp): …`, `docs: …`, `test: …`, `ci: …`.
- Use o modelo de PR (`.github/pull_request_template.md`). Marque as invariantes.
- **Merge automático só para PR só de documentação** (decisão D-08 do Issei). PR de código, testes, CI, `.claude/` ou qualquer `.json`, `.ipynb`, `.csv` espera o Issei. Regra em [`docs/ci-cd.md`](docs/ci-cd.md).
- A CI roda os testes no Windows (obrigatório) e no Linux (informativo).
- Nunca pule, desligue ou marque como ignorado um teste para a CI passar.
- No máximo três tentativas de deixar a verificação verde. Depois, pare e relate o bloqueio com a saída do erro.

## 6. Documentação

- Português do Brasil, linguagem simples: ABNT NBR ISO 24495-1 e ASD-STE100 adaptado ao PT-BR. Detalhe na skill `redigir-documento`.
- Pensamento enxuto: escreva o que alguém vai ler ou usar agora. Especificação de etapa futura é estoque e perde valor.
- Documento novo em `docs/` tem cabeçalho com `id`, `titulo`, `data`, `leitor` e `padrao_de_redacao`.
- Não refatore documentos existentes só para mudar o estilo.

## 7. Aprendizados

Antes de uma tarefa grande, leia [`docs/aprendizados.md`](docs/aprendizados.md).
Ao fim, acrescente o que aprendeu (só inclusão; uma lição por item: contexto → lição).

## 8. Mapa de pastas

| Pasta | Conteúdo |
| :-- | :-- |
| `docs/especificacao/` | Especificação, contratos MCP, ADRs, decisões |
| `docs/` | CI/CD, desenvolvimento agêntico, origem do código, aprendizados |
| `src/caliope/` | Núcleo genérico (a partir da etapa E1) |
| `estudos/` | Pacotes de estudo (instrumento, normalização, análises) |
| `tests/` | Testes; `tests/repositorio/` cobre CI, hooks e guarda de dados |
| `scripts/ci/`, `scripts/hooks/` | Verificações da CI e hooks do agente |
| `.claude/` | Configuração do Claude Code: permissões, hooks, skills, agentes |
