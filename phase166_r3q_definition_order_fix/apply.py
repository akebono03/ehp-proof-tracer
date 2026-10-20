from __future__ import annotations

import ast
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TARGET = ROOT / "phase165_r52_r16_web_citation_gate.py"
BACKUP_DIR = ROOT / "phase166_r3q_definition_order_fix_backups"


def main() -> None:
    original = TARGET.read_text(encoding="utf-8")
    parsed = ast.parse(original, filename=str(TARGET))
    functions = [item for item in parsed.body if isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef)) and item.name == "screen_shared_proof_context"]
    if len(functions) != 1:
        raise RuntimeError("expected exactly one screen_shared_proof_context")
    node = functions[0]
    lines = original.splitlines(keepends=True)
    fragment = "".join(lines[node.lineno - 1:node.end_lineno])
    before = "            if assertion.kind is not AssertionKind.STATEMENT:\n                continue\n"
    after = "            if assertion.kind not in (AssertionKind.STATEMENT, AssertionKind.DEFINITION):\n                continue\n"
    if fragment.count(before) != 1:
        raise RuntimeError("expected kind filter not found exactly once; no modification made")
    replacement = fragment.replace(before, after)
    updated = "".join(lines[:node.lineno - 1]) + replacement + "".join(lines[node.end_lineno:])
    ast.parse(updated, filename=str(TARGET))
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")
    backup = BACKUP_DIR / stamp
    backup.mkdir(parents=True, exist_ok=False)
    (backup / TARGET.name).write_text(original, encoding="utf-8")
    (backup / "modified_function.py.txt").write_text(replacement, encoding="utf-8")
    TARGET.write_text(updated, encoding="utf-8")
    (ROOT / "phase166_r3q_definition_order_fix" / "latest_backup.txt").write_text(str(backup), encoding="utf-8")
    print("PATCHED:", TARGET)
    print("BACKUP:", backup)
    print("FUNCTION: screen_shared_proof_context")


if __name__ == "__main__":
    main()
