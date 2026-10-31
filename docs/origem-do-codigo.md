---
id: CAL-ORIGEM-01
titulo: Registro do código copiado de outros repositórios
data: 2026-10-31
leitor: quem revisa um PR com código copiado, ou atualiza uma cópia
padrao_de_redacao: ABNT NBR ISO 24495-1 (linguagem simples) e ASD-STE100 adaptado ao PT-BR
---

# Origem do código

Regra: ADR-ps-008. Procedimento: skill `copiar-do-knowledge-os`.
Cada arquivo copiado tem cabeçalho de origem e uma linha nesta tabela.

| Arquivo aqui | Origem | Commit | Mudanças | Data |
| :-- | :-- | :-- | :-- | :-- |
| `scripts/ci/classify_changes.py` | `issei/knowledge-os`, `scripts/ci/classify_changes.py` | `feefe4d` | Padrões deste projeto; todo arquivo de dado conta como sistema | 2026-10-31 |
| `scripts/ci/check_docs.py` | `issei/knowledge-os`, `scripts/ci/check_docs.py` | `feefe4d` | `SKIP_DIRS` | 2026-10-31 |
| `.github/workflows/ci.yml` (estrutura) | `issei/knowledge-os`, `.github/workflows/ci.yml` | `feefe4d` | Job `dados`, matriz Windows, `lint`, merge automático só para documentação, sem release | 2026-10-31 |

Os três arquivos de produto da ADR-ps-008 (`schema.py`, `errors.py`, `mcp/__init__.py`) entram na etapa E1 e E2.
