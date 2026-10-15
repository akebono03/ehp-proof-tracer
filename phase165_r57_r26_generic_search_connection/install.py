"""Idempotently install R26 without replacing unrelated code."""
from __future__ import annotations

import ast
from pathlib import Path
import shutil

ROOT = Path(__file__).resolve().parent.parent
PACKAGE = Path(__file__).resolve().parent
MODULE = ROOT / "phase165_r52_r9_shared_math.py"
HELPER = ROOT / "phase165_r57_r26_generic_search_connection.py"
BACKUP = ROOT / "phase165_r52_r9_shared_math.py.r57_r26_before.bak"


def install() -> None:
    for name in (
        "phase165_r57_r23_conclusion_unification.py",
        "phase165_r57_r24_candidate_discovery.py",
        "phase165_r57_r25_premise_generation.py",
    ):
        if not (ROOT / name).is_file():
            raise SystemExit("Missing prerequisite: " + name)
    original = MODULE.read_text(encoding="utf-8")
    tree = ast.parse(original)
    functions = [node for node in tree.body if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and node.name == "shared_expansion_provider"]
    if len(functions) != 1:
        raise SystemExit("Expected precisely one shared_expansion_provider")
    node = functions[0]
    existing = ast.get_source_segment(original, node)
    replacement = (PACKAGE / "shared_expansion_provider.py.txt").read_text(encoding="utf-8").rstrip("\n")
    if existing == replacement:
        if HELPER.read_text(encoding="utf-8") != (PACKAGE / HELPER.name).read_text(encoding="utf-8"):
            raise SystemExit("R26 installed but helper differs: manual review required")
        print("R26 already installed")
        return
    if "from phase165_r57_r26_generic_search_connection import" in existing:
        raise SystemExit("Unexpected R26 modification: manual review required")
    for expected in ("expand_existing_pi43_rules", "retain_ordered_root_expansions", "expand_cited_general_specialization"):
        if expected not in existing:
            raise SystemExit("Changed shared provider: missing " + expected)
    if HELPER.exists() and HELPER.read_text(encoding="utf-8") != (PACKAGE / HELPER.name).read_text(encoding="utf-8"):
        raise SystemExit("Existing R26 helper differs: manual review required")
    if BACKUP.exists() and BACKUP.read_text(encoding="utf-8") != original:
        raise SystemExit("Conflicting pre-R26 backup: manual review required")
    if not BACKUP.exists():
        shutil.copy2(MODULE, BACKUP)
    lines = original.splitlines(keepends=True)
    ending = "\r\n" if "\r\n" in original else "\n"
    newlines = replacement.splitlines()
    lines[node.lineno - 1:node.end_lineno] = [line + ending for line in newlines]
    rewritten = "".join(lines)
    ast.parse(rewritten)
    if "def search_shared_group_goal(" not in rewritten:
        raise SystemExit("Search API disappeared unexpectedly")
    shutil.copy2(PACKAGE / HELPER.name, HELPER)
    MODULE.write_text(rewritten, encoding="utf-8", newline="")
    print("R26 shared provider connected; canonical search unchanged")


if __name__ == "__main__":
    install()
