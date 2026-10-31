---
id: CAL-CICD-01
titulo: Como a CI decide o que roda e o que entra sozinho na main
data: 2026-10-31
leitor: Issei e qualquer agente que abre PR neste repositório
padrao_de_redacao: ABNT NBR ISO 24495-1 (linguagem simples) e ASD-STE100 adaptado ao PT-BR
---

# CI/CD

A CI é uma adaptação da CI do `knowledge-os` (`feefe4d`, `docs/ci-cd.md` de lá).
Há três diferenças. O guarda de dados roda em todo PR. Os testes rodam no Windows. O merge automático vale só para documentação (decisão D-08 do Issei, 30/10/2026).

## Fluxo

```text
PR aberto ou atualizado
  ├─ changes ── classifica os arquivos (scripts/ci/classify_changes.py)
  ├─ dados  ── guarda de dados D1–D5 (scripts/ci/check_dados.py)            [sempre]
  ├─ docs   ── links relativos dos .md (scripts/ci/check_docs.py)           [se mudou documento]
  ├─ tests  ── Windows e Linux × Python 3.12 e 3.13 (scripts/verificar.py)  [se mudou sistema]
  ├─ lint   ── ruff check                                                   [se mudou sistema]
  └─ ci-ok  ── passa se todo job necessário passou ou foi pulado
       └─ automerge ── squash na main, só se o PR não tem nada de sistema
```

Os jobs rodam em paralelo. Um push novo no mesmo PR cancela a execução anterior.

## O que é "sistema" e o que é "só documentação"

| Sistema: roda testes e **espera o Issei** | Só documentação: entra sozinho se a CI passar |
| :-- | :-- |
| `src/`, `tests/`, `scripts/`, `estudos/`, `notebooks/`, `.github/`, `.claude/`, `pyproject.toml` | demais `*.md` e `docs/**` |
| `docs/especificacao/anexos/` (os testes leem o exemplo fictício) | |
| qualquer `.json`, `.ipynb`, `.csv` ou `.sqlite*`, em qualquer pasta | |
| qualquer arquivo fora das duas listas | |

`AGENTS.md` e `CLAUDE.md` contam como documentação. Mudança neles muda o comportamento do agente, mas não o produto nem o dado.

A regra está em `scripts/ci/classify_changes.py` e é coberta por `tests/repositorio/test_scripts.py`.

## Guarda de dados (D1–D5)

| Regra | Bloqueia |
| :-- | :-- |
| D1 | Base SQLite e arquivos dela (`*.sqlite`, `*-wal`, `*-shm`, `*-journal`) |
| D2 | `.env` |
| D3 | JSON no formato da página (objeto com `campos`) sem `"_fixture": true` e sem hash em `scripts/ci/ficticios.sha256` |
| D4 | Exportação da base com natureza diferente de `ficticio` ou com identificação |
| D5 | Notebook com saída gravada |

O mesmo código roda no hook de guarda do agente (`docs/desenvolvimento-agentico.md`). O agente e a CI aplicam a mesma regra.

## Windows

RNF-01 pede Windows. O job no Windows é obrigatório. O job no Linux usa `continue-on-error` e só informa.
O `.gitattributes` fixa LF e marca anexos e fixtures como binários. Assim o checkout no Windows não muda o SHA-256 do exemplo.

## Entrega

Ainda não há release: o pacote nasce na etapa E1. Quando houver `pyproject.toml`, o modelo é o do `knowledge-os`: release só quando a versão não tem tag `v<versão>`.

## Salvaguardas

- O merge automático usa `--match-head-commit`. Um commit novo depois do início da execução impede o merge.
- PR de fork e PR em rascunho nunca entram sozinhos.
- Permissão padrão `contents: read`. Escrita só no job `automerge`.

## Configuração recomendada no GitHub

- Proteção da `main` com o check obrigatório **CI ok**.
- Se a proteção exigir aprovação, o merge automático de documentação também vai esperar a aprovação.
