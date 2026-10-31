#!/usr/bin/env python3
"""Hook de guarda do Claude Code (PreToolUse e PostToolUse).

O agente também é um cliente com acesso a arquivos. A barreira de conteúdo
(ADR-ps-007) só vale se ele não ler a pasta de dados nem a base SQLite. Este
hook aplica isso ao próprio agente e reaproveita as regras de dados da CI
(scripts/ci/check_dados.py).

PreToolUse  bloqueia (código 2):
  G1  Read, Grep, Glob, Edit, Write ou Bash que toque a pasta de dados
      (uma pasta chamada exatamente "pesquisa-streaming") ou um arquivo *.sqlite*;
  G2  o comando de terminal sqlite3;
  G3  Write de arquivo que viola as regras D1–D5 (nome ou conteúdo).
PostToolUse avisa (código 2) quando um Edit deixou o arquivo violando D3–D5.

Configurado em .claude/settings.json. Sem stdin ou com JSON inválido, permite:
a CI aplica as mesmas regras de dados no PR.
"""

from __future__ import annotations

import importlib.util
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PASTA_DE_DADOS = re.compile(r"(^|[\\/\s\"'=])pesquisa-streaming([\\/\s\"']|$)", re.I)
SQLITE = re.compile(r"\.sqlite3?(-wal|-shm|-journal)?\b", re.I)
SQLITE_CLI = re.compile(r"(^|[;&|(]\s*)sqlite3(\.exe)?(\s|$)", re.I)


def _check_dados():
    spec = importlib.util.spec_from_file_location("check_dados", ROOT / "scripts" / "ci" / "check_dados.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def _rel(caminho: str) -> str:
    p = Path(caminho)
    try:
        return p.resolve().relative_to(ROOT).as_posix()
    except (ValueError, OSError):
        return p.as_posix()


def motivos_pre(ferramenta: str, entrada: dict) -> list[str]:
    # No Grep, "pattern" é o texto procurado, não um caminho: procurar ".sqlite" no código é permitido.
    chaves = ["file_path", "path", "notebook_path", "glob", "command"]
    if ferramenta == "Glob":
        chaves.append("pattern")
    alvos = [str(entrada.get(k, "")) for k in chaves]
    texto = " ".join(a for a in alvos if a)
    motivos = []
    if PASTA_DE_DADOS.search(texto) or SQLITE.search(texto):
        motivos.append("G1 a pasta de dados e a base SQLite ficam fora do alcance do agente (ADR-ps-007). "
                       "Use a CLI caliope; leitura de texto de resposta é tarefa da pessoa, no terminal")
    if ferramenta == "Bash" and SQLITE_CLI.search(str(entrada.get("command", ""))):
        motivos.append("G2 o agente não abre a base com sqlite3; use as ferramentas do caliope")
    if ferramenta == "Write" and entrada.get("file_path"):
        cd = _check_dados()
        rel = _rel(entrada["file_path"])
        conteudo = str(entrada.get("content", "")).encode("utf-8")
        motivos += [f"G3 {m}" for m in cd.problemas_do_nome(rel) + cd.problemas_do_conteudo(rel, conteudo)]
    return motivos


def motivos_pos(entrada: dict) -> list[str]:
    caminho = entrada.get("file_path") or entrada.get("notebook_path")
    if not caminho or not Path(caminho).is_file():
        return []
    cd = _check_dados()
    return cd.problemas_do_conteudo(_rel(caminho), Path(caminho).read_bytes())


def main() -> int:
    if hasattr(sys.stderr, "reconfigure"):
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    try:
        evento = json.loads(sys.stdin.buffer.read().decode("utf-8") or "{}")
    except (OSError, ValueError):
        return 0
    ferramenta = evento.get("tool_name", "")
    entrada = evento.get("tool_input") or {}
    if evento.get("hook_event_name") == "PostToolUse":
        motivos = motivos_pos(entrada)
        prefixo = "[guarda] O arquivo ficou fora das regras de dados. Desfaça a mudança:"
    else:
        motivos = motivos_pre(ferramenta, entrada)
        prefixo = f"[guarda] {ferramenta} bloqueado:"
    if not motivos:
        return 0
    print(prefixo, *motivos, sep="\n- ", file=sys.stderr)
    return 2


if __name__ == "__main__":
    sys.exit(main())
