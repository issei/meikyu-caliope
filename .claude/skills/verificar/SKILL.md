---
name: verificar
description: Como rodar a verificação local do meikyu-caliope (dados, links, compilação, testes, ruff) e interpretar falhas. Use antes de todo commit e push, e quando o hook Stop bloquear o encerramento.
---

# Verificação local

Uma chamada só, offline e determinística. **Verde obrigatório antes de qualquer push.**

```bash
python scripts/verificar.py            # completo
python scripts/verificar.py --rapido   # sem ruff; é o que o hook Stop roda
```

## O que roda

| Passo | Script | Falha quer dizer |
| :-- | :-- | :-- |
| Dados (D1–D5) | `scripts/ci/check_dados.py` | Base SQLite, `.env`, JSON de resposta sem marca de fixture, exportação real ou com identificação, notebook com saída |
| Links | `scripts/ci/check_docs.py` | Link relativo quebrado em algum `.md` |
| Compilação | `python -m compileall` | Erro de sintaxe |
| Testes | `python -m unittest discover -s tests -t .` | Ver a mensagem do teste |
| Ruff | `ruff check .` (se instalado) | Estilo ou erro estático; `ruff check --fix .` resolve parte |

A CI roda os mesmos passos, com os testes no Windows e no Linux (`docs/ci-cd.md`).

## Como agir numa falha

- **Dados:** não "conserte" marcando um dado real como fixture. Se o arquivo é real, ele sai do repositório. Se é fictício e precisa manter os bytes, registre o SHA-256 em `scripts/ci/ficticios.sha256` e diga isso no PR.
- **Teste de vazamento ou de contrato MCP:** a saída ganhou texto. Corrija a projeção, não o teste.
- **Só falha no Windows:** veja caminho, fim de linha (`.gitattributes`) e codificação do console.

## Regra

No máximo **três** tentativas por tarefa. Continua vermelho: pare num ponto seguro e relate o bloqueio com a saída do erro. Nunca pule, desligue ou ignore um teste.
