"""Regras da CI, do guarda de dados e dos hooks do agente (docs/ci-cd.md, docs/desenvolvimento-agentico.md)."""

import importlib.util
import json
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def _load(rel):
    spec = importlib.util.spec_from_file_location(Path(rel).stem, ROOT / rel)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


classify = _load("scripts/ci/classify_changes.py").classify
check_docs = _load("scripts/ci/check_docs.py")
check_dados = _load("scripts/ci/check_dados.py")
guarda = _load("scripts/hooks/guarda.py")

EXPORTACAO_PAGINA = json.dumps({"versao": 1, "campos": {"rotina-1": "texto"}, "situacoes": []}).encode()


class ClassifyChangesTest(unittest.TestCase):
    def test_docs_only(self):
        self.assertEqual(classify(["README.md", "AGENTS.md", "docs/especificacao/01-especificacao.md"]),
                         {"system": False, "docs": True})

    def test_code_tooling_and_agent_config_are_system(self):
        for p in ["src/caliope/cli.py", "tests/x.py", "scripts/verificar.py", ".github/workflows/ci.yml",
                  ".claude/settings.json", "pyproject.toml", "estudos/streaming-2026/instrumento.json"]:
            self.assertTrue(classify([p])["system"], p)

    def test_any_data_file_is_system_even_inside_docs(self):
        for p in ["docs/respostas.json", "docs/especificacao/anexos/exemplo-ficticio-v1.json",
                  "docs/notas.ipynb", "docs/base.sqlite", "docs/tabela.csv"]:
            self.assertTrue(classify([p])["system"], p)

    def test_unknown_or_empty_runs_everything(self):
        self.assertTrue(classify(["LICENSE"])["system"])
        self.assertTrue(classify([])["system"])


class CheckDocsTest(unittest.TestCase):
    def test_repository_has_no_broken_links(self):
        self.assertEqual(check_docs.broken_links(ROOT), [])


class CheckDadosTest(unittest.TestCase):
    def test_repository_is_clean(self):
        self.assertEqual(check_dados.verificar(ROOT), [])

    def test_sqlite_and_env_names_are_refused(self):
        for p in ["base.sqlite", "x/base.sqlite-wal", "a.db-journal", ".env", "x/.env.local"]:
            self.assertTrue(check_dados.problemas_do_nome(p), p)
        self.assertFalse(check_dados.problemas_do_nome("src/caliope/base/schema.sql"))

    def test_page_export_needs_fixture_flag_or_registered_hash(self):
        self.assertTrue(check_dados.problemas_do_conteudo("x.json", EXPORTACAO_PAGINA, set()))
        marcado = json.dumps({"_fixture": True, "versao": 1, "campos": {}}).encode()
        self.assertEqual(check_dados.problemas_do_conteudo("x.json", marcado, set()), [])

    def test_registered_example_keeps_its_hash(self):
        # .gitattributes marca o anexo como binário: o checkout no Windows não troca LF por CRLF.
        self.assertEqual(check_dados.problemas_do_conteudo(
            "docs/especificacao/anexos/exemplo-ficticio-v1.json",
            (ROOT / "docs/especificacao/anexos/exemplo-ficticio-v1.json").read_bytes()), [])

    def test_base_export_only_fictitious_without_identification(self):
        def doc(natureza, ident):
            return json.dumps({"formato": "pesquisa-streaming/exportacao", "estudo": {"natureza": natureza},
                               "inclui_identificacao": ident}).encode()
        self.assertEqual(check_dados.problemas_do_conteudo("e.json", doc("ficticio", False)), [])
        self.assertTrue(check_dados.problemas_do_conteudo("e.json", doc("real", False)))
        self.assertTrue(check_dados.problemas_do_conteudo("e.json", doc("ficticio", True)))

    def test_notebook_with_outputs_is_refused(self):
        sujo = json.dumps({"cells": [{"outputs": [{"text": "resposta"}]}]}).encode()
        limpo = json.dumps({"cells": [{"outputs": []}]}).encode()
        self.assertTrue(check_dados.problemas_do_conteudo("n.ipynb", sujo))
        self.assertEqual(check_dados.problemas_do_conteudo("n.ipynb", limpo), [])


class GuardaTest(unittest.TestCase):
    def _run(self, evento):
        return subprocess.run([sys.executable, "scripts/hooks/guarda.py"], cwd=ROOT,
                              input=json.dumps(evento).encode(), capture_output=True)

    def test_data_folder_and_sqlite_are_out_of_reach(self):
        casos = [
            ("Read", {"file_path": r"C:\Users\x\AppData\Local\pesquisa-streaming\real\base.sqlite"}),
            ("Read", {"file_path": "/home/x/pesquisa-streaming/real/entrada/a.json"}),
            ("Bash", {"command": "cat ~/pesquisa-streaming/real/saida/x.json"}),
            ("Bash", {"command": "sqlite3 demo.db .dump"}),
            ("Glob", {"pattern": "**/*.sqlite"}),
            ("Grep", {"pattern": "x", "path": "D:/dados/pesquisa-streaming"}),
        ]
        for ferramenta, entrada in casos:
            self.assertTrue(guarda.motivos_pre(ferramenta, entrada), (ferramenta, entrada))

    def test_normal_work_is_allowed(self):
        casos = [
            ("Read", {"file_path": str(ROOT / "docs/especificacao/01-especificacao.md")}),
            ("Read", {"file_path": "/mnt/project-files/backend-pesquisa-streaming/README.md"}),
            ("Grep", {"pattern": r"base\.sqlite", "path": "src"}),
            ("Bash", {"command": "python -m unittest discover -s tests -t ."}),
            ("Bash", {"command": "python -c 'import sqlite3'"}),
        ]
        for ferramenta, entrada in casos:
            self.assertEqual(guarda.motivos_pre(ferramenta, entrada), [], (ferramenta, entrada))

    def test_write_of_unmarked_page_export_is_blocked_by_the_hook_process(self):
        evento = {"hook_event_name": "PreToolUse", "tool_name": "Write",
                  "tool_input": {"file_path": str(ROOT / "tests/fixtures/ficticio/x.json"),
                                 "content": EXPORTACAO_PAGINA.decode()}}
        res = self._run(evento)
        self.assertEqual(res.returncode, 2)
        self.assertIn("D3", res.stderr.decode("utf-8"))

    def test_invalid_stdin_allows(self):
        res = subprocess.run([sys.executable, "scripts/hooks/guarda.py"], cwd=ROOT,
                             input=b"nao e json", capture_output=True)
        self.assertEqual(res.returncode, 0)


class SettingsTest(unittest.TestCase):
    def test_hooks_point_to_existing_scripts(self):
        settings = json.loads((ROOT / ".claude/settings.json").read_text(encoding="utf-8"))
        comandos = [h["command"] for grupos in settings["hooks"].values() for g in grupos for h in g["hooks"]]
        self.assertTrue(comandos)
        for cmd in comandos:
            # Caminho a partir de $CLAUDE_PROJECT_DIR: o hook funciona mesmo depois de um cd.
            self.assertIn('"$CLAUDE_PROJECT_DIR/', cmd)
            script = cmd.split('"$CLAUDE_PROJECT_DIR/', 1)[1].split('"', 1)[0]
            self.assertTrue((ROOT / script).is_file(), cmd)


class WorkflowTest(unittest.TestCase):
    def setUp(self):
        self.ci = (ROOT / ".github/workflows/ci.yml").read_text(encoding="utf-8")

    def test_automerge_only_for_docs_only_prs(self):
        # Decisão D-08 do Issei: código espera por ele.
        bloco = self.ci.split("  automerge:", 1)[1].split("\n  release:", 1)[0]
        self.assertIn("needs.changes.outputs.system == 'false'", bloco)
        # Sem !cancelled(), o GitHub pula o job quando build e testes foram pulados (knowledge-os, PR #14).
        self.assertIn("!cancelled()", bloco)

    def test_windows_is_in_the_test_matrix(self):
        self.assertIn("windows-latest", self.ci)

    def test_data_check_always_runs(self):
        bloco = self.ci.split("  dados:", 1)[1].split("\n  docs:", 1)[0]
        self.assertNotIn("if:", bloco)


if __name__ == "__main__":
    unittest.main()
