#!/usr/bin/env python3
"""Classifica os arquivos alterados num PR para a CI decidir o que rodar.

Origem: issei/knowledge-os@feefe4d, scripts/ci/classify_changes.py (cópia
registrada, ADR-ps-008). Mudanças: padrões deste projeto e a regra de dados.

Uso: classify_changes.py <base_sha> <head_sha>  (ou lista de caminhos em stdin com "-")

Escreve em $GITHUB_OUTPUT (ou stdout) as chaves:
  system=true|false  algo que muda o comportamento do sistema, dos testes ou do agente
  docs=true|false    algum documento alterado

Regra (docs/ci-cd.md): um arquivo é "system" se casar com SYSTEM_PATTERNS. Os
anexos da especificação que os testes leem também contam como "system". Um PR
só com documentos que não são "system" é "docs-only": não roda a suíte e entra
sozinho na main (decisão D-08 do Issei). Todo o resto espera o Issei.
"""

from __future__ import annotations

import fnmatch
import os
import subprocess
import sys

SYSTEM_PATTERNS = (
    "src/*",
    "tests/*",
    "scripts/*",
    "estudos/*",
    "notebooks/*",
    ".github/*",
    ".claude/*",
    "pyproject.toml",
    # Lidos pelos testes (exemplo fictício com hash registrado).
    "docs/especificacao/anexos/*",
    # Qualquer dado, em qualquer pasta, nunca entra sem revisão humana.
    "*.json",
    "*.ipynb",
    "*.sqlite*",
    "*.csv",
)
DOC_PATTERNS = ("*.md", "docs/*")


def classify(paths: list[str]) -> dict[str, bool]:
    system = any(fnmatch.fnmatch(p, pat) for p in paths for pat in SYSTEM_PATTERNS)
    docs = any(fnmatch.fnmatch(p, pat) for p in paths for pat in DOC_PATTERNS)
    # Sem arquivos (não deveria acontecer) ou com algo não classificado: roda tudo.
    unknown = [p for p in paths
               if not any(fnmatch.fnmatch(p, pat) for pat in SYSTEM_PATTERNS + DOC_PATTERNS)]
    if not paths or unknown:
        system = True
    return {"system": system, "docs": docs}


def changed_paths(base: str, head: str) -> list[str]:
    out = subprocess.run(
        ["git", "diff", "--name-only", "-z", f"{base}...{head}"],
        check=True, capture_output=True,
    ).stdout
    return [p.decode("utf-8", "surrogateescape") for p in out.split(b"\0") if p]


def main(argv: list[str]) -> int:
    if argv[1:] == ["-"]:
        paths = [line.strip() for line in sys.stdin if line.strip()]
    elif len(argv) == 3:
        paths = changed_paths(argv[1], argv[2])
    else:
        print(__doc__, file=sys.stderr)
        return 1
    result = classify(paths)
    lines = [f"{k}={'true' if v else 'false'}" for k, v in result.items()]
    target = os.environ.get("GITHUB_OUTPUT")
    if target:
        with open(target, "a", encoding="utf-8") as fh:
            fh.write("\n".join(lines) + "\n")
    print("\n".join(lines))
    print(f"{len(paths)} arquivo(s) alterado(s)", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
