#!/usr/bin/env python3
"""Impede que dado real de pesquisa entre no repositório.

Uso: check_dados.py [caminho ...]   (sem argumentos: varre o repositório)

Regras (docs/ci-cd.md, ADR-ps-006 e ADR-ps-007):
  D1  Nenhuma base SQLite nem arquivo auxiliar dela (*.sqlite, *-wal, *-shm, ...).
  D2  Nenhum arquivo .env.
  D3  JSON no formato da página de entrevista (objeto com "campos") só com
      "_fixture": true ou com SHA-256 registrado em scripts/ci/ficticios.sha256.
  D4  JSON de exportação da base só com natureza "ficticio" e sem identificação.
  D5  Notebook (.ipynb) sem saídas gravadas: uma saída pode mostrar resposta real.

Só biblioteca padrão. O hook de guarda (scripts/hooks/guarda.py) usa as mesmas
funções, para que o agente e a CI apliquem a mesma regra.
"""

from __future__ import annotations

import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
REGISTRO = ROOT / "scripts" / "ci" / "ficticios.sha256"
SKIP_DIRS = {".git", ".venv", "venv", "node_modules", "build", "dist", "__pycache__", ".codegraph"}
NOME_PROIBIDO = re.compile(r"(\.sqlite3?|\.sqlite3?-(wal|shm|journal)|\.db-(wal|shm|journal))$", re.I)
ENV = re.compile(r"(^|/)\.env(\.[^/]*)?$")


def registrados() -> set[str]:
    if not REGISTRO.exists():
        return set()
    hashes = set()
    for linha in REGISTRO.read_text(encoding="utf-8").splitlines():
        linha = linha.strip()
        if linha and not linha.startswith("#"):
            hashes.add(linha.split()[0].lower())
    return hashes


def problemas_do_nome(rel: str) -> list[str]:
    rel = rel.replace("\\", "/")
    if NOME_PROIBIDO.search(rel):
        return [f"{rel}: D1 base SQLite não entra no repositório (fica na pasta de dados, fora dele)"]
    if ENV.search(rel):
        return [f"{rel}: D2 arquivo .env não entra no repositório"]
    return []


def problemas_do_conteudo(rel: str, dados: bytes, hashes: set[str] | None = None) -> list[str]:
    rel = rel.replace("\\", "/")
    if rel.endswith(".ipynb"):
        return _notebook(rel, dados)
    if not rel.endswith(".json"):
        return []
    try:
        doc = json.loads(dados.decode("utf-8-sig"))
    except (UnicodeDecodeError, ValueError):
        return []  # JSON inválido não é dado de pesquisa reconhecível; outros testes cuidam dele.
    if not isinstance(doc, dict):
        return []
    if isinstance(doc.get("campos"), dict):
        if doc.get("_fixture") is True:
            return []
        if hashes is None:
            hashes = registrados()
        if hashlib.sha256(dados).hexdigest() in hashes:
            return []
        return [f"{rel}: D3 parece resposta da página de entrevista. Use só dado fictício, "
                f'com "_fixture": true, ou registre o SHA-256 em scripts/ci/ficticios.sha256']
    if str(doc.get("formato", "")).endswith("/exportacao") or "inclui_identificacao" in doc:
        estudo = doc.get("estudo") if isinstance(doc.get("estudo"), dict) else {}
        erros = []
        if estudo.get("natureza") != "ficticio":
            erros.append(f'{rel}: D4 exportação sem natureza "ficticio" não entra no repositório')
        if doc.get("inclui_identificacao") is not False:
            erros.append(f"{rel}: D4 exportação com identificação não entra no repositório")
        return erros
    return []


def _notebook(rel: str, dados: bytes) -> list[str]:
    try:
        nb = json.loads(dados.decode("utf-8"))
    except (UnicodeDecodeError, ValueError):
        return []
    for celula in nb.get("cells", []):
        if celula.get("outputs"):
            return [f"{rel}: D5 notebook com saídas gravadas. Limpe as saídas antes do commit"]
    return []


def arquivos_versionados(root: Path) -> list[str]:
    try:
        out = subprocess.run(["git", "ls-files", "-z", "--cached", "--others", "--exclude-standard"],
                             cwd=root, check=True, capture_output=True).stdout
        return [p.decode("utf-8", "surrogateescape") for p in out.split(b"\0") if p]
    except (OSError, subprocess.CalledProcessError):
        return [p.relative_to(root).as_posix() for p in root.rglob("*")
                if p.is_file() and not SKIP_DIRS.intersection(p.relative_to(root).parts)]


def verificar(root: Path, caminhos: list[str] | None = None) -> list[str]:
    hashes = registrados()
    problemas = []
    for rel in caminhos if caminhos is not None else arquivos_versionados(root):
        caminho = root / rel
        problemas += problemas_do_nome(rel)
        if caminho.is_file():
            problemas += problemas_do_conteudo(rel, caminho.read_bytes(), hashes)
    return problemas


def main(argv: list[str]) -> int:
    if hasattr(sys.stderr, "reconfigure"):
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    problemas = verificar(ROOT, argv[1:] or None)
    for p in problemas:
        print(p, file=sys.stderr)
    print(f"check_dados: {len(problemas)} problema(s)")
    return 1 if problemas else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
