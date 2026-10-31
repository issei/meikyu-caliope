#!/usr/bin/env python3
"""Hook Stop do Claude Code: mantém a verificação verde ao fim de cada turno.

Roda `scripts/verificar.py --rapido` só quando há mudança não commitada em
src/, tests/, scripts/, estudos/ ou .claude/. Falhou: sai com 2, e o agente
recebe o erro antes de encerrar (fail-closed). Na segunda tentativa seguida
(stop_hook_active), deixa encerrar para não entrar em laço; o PR ainda passa
pela CI.
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PASTAS = ("src/", "tests/", "scripts/", "estudos/", ".claude/")


def main() -> int:
    try:
        evento = json.loads(sys.stdin.buffer.read().decode("utf-8") or "{}")
    except (OSError, ValueError):
        evento = {}
    if evento.get("stop_hook_active"):
        return 0
    status = subprocess.run(["git", "status", "--porcelain", "--", *PASTAS],
                            cwd=ROOT, capture_output=True, text=True, encoding="utf-8")
    if status.returncode != 0 or not status.stdout.strip():
        return 0
    res = subprocess.run([sys.executable, "scripts/verificar.py", "--rapido"],
                         cwd=ROOT, capture_output=True, text=True, encoding="utf-8", errors="replace")
    if res.returncode == 0:
        return 0
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    print("[stop] verificação vermelha. Corrija antes de encerrar:\n"
          + (res.stdout + res.stderr)[-4000:], file=sys.stderr)
    return 2


if __name__ == "__main__":
    sys.exit(main())
