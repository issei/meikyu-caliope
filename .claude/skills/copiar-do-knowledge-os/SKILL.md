---
name: copiar-do-knowledge-os
description: Procedimento da ADR-ps-008 para copiar um arquivo do repositório issei/knowledge-os para o meikyu-caliope — leitura integral, cabeçalho de origem, registro e teste no Windows. Use sempre que for reaproveitar código do knowledge-os.
---

# Copiar do `knowledge-os` (ADR-ps-008)

O reaproveitamento é por **cópia registrada**, não por biblioteca comum.

## Lista aprovada

Só estes arquivos, do commit `feefe4d`:

- `src/kos/store/schema.py` → base de `src/caliope/base/`
- `src/kos/errors.py` e o teste que compara o catálogo com o contrato → `src/caliope/erros.py`
- `src/kos/mcp/__init__.py` → base de `src/caliope/mcp/servidor.py`

Como ideia, sem cópia: `store/dump.py` (digest lógico) e `audit` (evento antes do resultado).
**Proibido:** `search`, `cite`, `answer`. Eles devolvem texto e violam a barreira (ADR-ps-007).

Outro arquivo fora da lista precisa de mudança na ADR-ps-008 antes da cópia.

## Passos

1. **Leia o arquivo inteiro** no commit de origem (`git show feefe4d:<caminho>`). A especificação registra duas afirmações erradas feitas de memória (`05-metacognicao.md` §1). Não repita.
2. Copie e adapte. Retire tudo o que devolve texto de fragmento.
3. Primeira linha do docstring do módulo, depois do resumo:
   `Origem: issei/knowledge-os@<commit>, <caminho> (cópia registrada, ADR-ps-008). Mudanças: <lista curta>.`
4. Acrescente uma linha em `docs/origem-do-codigo.md`.
5. Rode a verificação. O código copiado nunca rodou no Windows no projeto de origem: confira o job Windows da CI.
6. No PR, marque a invariante de código copiado.

## Quando o `knowledge-os` mudar

A cada release do `knowledge-os`, compare os arquivos da tabela de origem com a versão nova e registre a decisão (atualizar ou manter).
