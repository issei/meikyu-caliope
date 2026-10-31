#!/usr/bin/env python3
"""Verificação local: o mesmo que a CI roda, numa chamada só.

Uso:
  python scripts/verificar.py           tudo (dados, links, compilação, testes, ruff se instalado)
  python scripts/verificar.py --rapido  sem ruff; é o que o hook Stop roda

Sai com 0 só se tudo passou. Verde obrigatório antes de qualquer push.
"""

from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PY = sys.executable
PASTAS_DE_CODIGO = ("src", "tests", "scripts", "estudos")


def passos(rapido: bool) -> list[tuple[str, list[str]]]:
    lista = [
        ("dados (D1–D5)", [PY, "scripts/ci/check_dados.py"]),
        ("links dos .md", [PY, "scripts/ci/check_docs.py"]),
        ("compilação", [PY, "-m", "compileall", "-q", *[d for d in PASTAS_DE_CODIGO if (ROOT / d).exists()]]),
        ("testes", [PY, "-m", "unittest", "discover", "-s", "tests", "-t", "."]),
    ]
    if not rapido and shutil.which("ruff"):
        lista.append(("ruff", ["ruff", "check", "."]))
    return lista


def main(argv: list[str]) -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    falhas = []
    for nome, cmd in passos("--rapido" in argv):
        print(f"── {nome}", flush=True)
        if subprocess.run(cmd, cwd=ROOT).returncode != 0:
            falhas.append(nome)
    print("verificar:", "verde" if not falhas else "VERMELHO em " + ", ".join(falhas))
    return 1 if falhas else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
