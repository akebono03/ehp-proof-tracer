"""Guarded replacement of one full Renderer function, with backup and rollback."""
from __future__ import annotations

import ast
import datetime
import json
import os
from pathlib import Path
import shutil
import sys

PACKAGE = Path(__file__).resolve().parent
ROOT = PACKAGE.parent
TARGET = ROOT / "phase168_r3_5_model_renderer.py"
STATE = PACKAGE / "installed_state.json"
BEFORE = PACKAGE / "full_functions" / "render_model_backed_narrative_markdown_BEFORE.py"
AFTER = PACKAGE / "full_functions" / "render_model_backed_narrative_markdown_FULL.py"


def make_updated_source(source: str) -> str:
    """Replace exactly the previously inspected function; preserve other code."""
    tree = ast.parse(source)
    candidates = [node for node in tree.body
                  if isinstance(node, ast.FunctionDef)
                  and node.name == "render_model_backed_narrative_markdown"]
    if len(candidates) != 1:
        raise RuntimeError("Expected exactly one common renderer function")
    node = candidates[0]
    lines = source.splitlines(keepends=True)
    actual = "".join(lines[node.lineno - 1:node.end_lineno]).replace("\r\n", "\n")
    expected = BEFORE.read_text(encoding="utf-8")
    if actual.rstrip() != expected.rstrip():
        raise RuntimeError("R3-41B1/R3-41C1 renderer prerequisite differs; nothing modified")
    replacement = AFTER.read_text(encoding="utf-8")
    newline = "\r\n" if "\r\n" in source else "\n"
    replacement = replacement.rstrip("\n").replace("\n", newline) + newline
    updated = ("".join(lines[:node.lineno - 1]) + replacement
               + "".join(lines[node.end_lineno:]))
    ast.parse(updated)
    if updated == source:
        raise RuntimeError("R3-41F patch did not change source")
    return updated


def apply() -> None:
    if STATE.exists():
        raise RuntimeError("Existing patch state: preserve backup; do not reapply")
    data = TARGET.read_bytes()
    bom = b"\xef\xbb\xbf" if data.startswith(b"\xef\xbb\xbf") else b""
    source = data.decode("utf-8-sig")
    updated = make_updated_source(source)
    stamp = datetime.datetime.now().strftime("%Y%m%dT%H%M%S%f")
    backup = PACKAGE / "backup" / stamp
    backup.mkdir(parents=True, exist_ok=False)
    (backup / TARGET.name).write_bytes(data)
    temp = TARGET.with_name(TARGET.name + ".r3_41f_tmp")
    try:
        temp.write_bytes(bom + updated.encode("utf-8"))
        os.replace(temp, TARGET)
        STATE.write_text(json.dumps({"backup": str(backup)}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    except Exception:
        temp.unlink(missing_ok=True)
        TARGET.write_bytes(data)
        raise
    # Full updated file is also shipped in the ZIP, not just a few-line diff.
    print("PATCHED", TARGET.name)
    print("FULL_FUNCTION", PACKAGE / "full_functions" / "render_model_backed_narrative_markdown_FULL.py")
    print("FULL_FILE", PACKAGE / "full_files" / TARGET.name)


def rollback() -> None:
    if not STATE.is_file():
        print("NO_PATCH_STATE_TO_ROLLBACK")
        return
    state = json.loads(STATE.read_text(encoding="utf-8"))
    source = Path(state["backup"]) / TARGET.name
    if not source.is_file():
        raise FileNotFoundError("Required original backup is missing: " + str(source))
    shutil.copyfile(source, TARGET)
    STATE.unlink()
    print("ROLLBACK", TARGET.name)


if __name__ == "__main__":
    if sys.argv[1:] == ["--rollback"]:
        rollback()
    elif not sys.argv[1:]:
        apply()
    else:
        raise SystemExit("usage: python -m phase168_r3_41f_inline_step_citations.apply [--rollback]")
