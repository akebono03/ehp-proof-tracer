"""Apply the minimal R3-41B model and renderer changes, with rollback."""
from __future__ import annotations

import ast
import hashlib
import json
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path

PACKAGE = Path(__file__).resolve().parent
ROOT = PACKAGE.parent
STATE = PACKAGE / "installed_state.json"
EXPECTED = {
    "phase168_r3_3_proof_narrative_model.py": "ea6862248a3db4da511d46b50a4e5d6bd090ed6c214a87526788b72117c14792",
    "phase168_r3_5_model_renderer.py": "3d7a116a7f49b2da726726f421003939753ece41512638f5ac7a823d9b5695ac",
}


def _sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _one_replace(text: str, old: str, new: str) -> str:
    if text.count(old) != 1:
        raise ValueError("Required existing import is missing or repeated: " + old)
    return text.replace(old, new, 1)


def _replace_definition(source: str, name: str, replacement: str, kind: str) -> str:
    tree = ast.parse(source)
    matches = [node for node in tree.body
               if ((kind == "class" and isinstance(node, ast.ClassDef)) or
                   (kind == "function" and isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))))
               and node.name == name]
    if len(matches) != 1:
        raise ValueError(f"Exactly one {kind} named {name} must exist")
    node = matches[0]
    first = (min(item.lineno for item in node.decorator_list)
             if isinstance(node, (ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef))
             and node.decorator_list else node.lineno)
    newline = "\r\n" if "\r\n" in source else "\n"
    lines = source.splitlines(keepends=True)
    rendered = replacement.rstrip("\n") + "\n"
    lines[first - 1:node.end_lineno] = [rendered.replace("\n", newline)]
    merged = "".join(lines)
    ast.parse(merged)
    return merged


def _transform_model(data: bytes) -> bytes:
    content = data.decode("utf-8")
    newline = "\r\n" if "\r\n" in content else "\n"
    imports = "from dataclasses import dataclass" + newline
    content = _one_replace(
        content,
        imports,
        imports + "from homotopy_groups import TodaPrimaryGroup" + newline,
    )
    content = _one_replace(
        content,
        "from phase165_r52_partial_proof import PartialProofResult",
        "from phase165_r52_partial_proof import PartialProofResult, ProofSearchStatus",
    )
    cls = (PACKAGE / "full_functions" / "ProofNarrativeModel_FULL.py").read_text(encoding="utf-8")
    fn = (PACKAGE / "full_functions" / "build_proof_narrative_model_FULL.py").read_text(encoding="utf-8")
    content = _replace_definition(content, "ProofNarrativeModel", cls, "class")
    content = _replace_definition(content, "build_proof_narrative_model", fn, "function")
    return content.encode("utf-8")


def _transform_renderer(data: bytes) -> bytes:
    content = data.decode("utf-8")
    fn = (PACKAGE / "full_functions" / "render_model_backed_narrative_markdown_FULL.py").read_text(encoding="utf-8")
    content = _replace_definition(content, "render_model_backed_narrative_markdown", fn, "function")
    return content.encode("utf-8")


def _rollback() -> None:
    if not STATE.exists():
        raise ValueError("No applied R3-41B patch is registered")
    state = json.loads(STATE.read_text(encoding="utf-8"))
    backup = PACKAGE / "backup" / state["backup_name"]
    for filename in EXPECTED:
        current = (ROOT / filename).read_bytes()
        if _sha(current) != state["installed_shas"][filename]:
            raise ValueError(f"Cannot roll back a subsequently modified file: {filename}")
    for filename in EXPECTED:
        original = (backup / filename).read_bytes()
        (ROOT / filename).write_bytes(original)
        print("ROLLBACK", filename)
    STATE.unlink()


def _apply() -> None:
    if STATE.exists():
        state = json.loads(STATE.read_text(encoding="utf-8"))
        if all(_sha((ROOT / f).read_bytes()) == state["installed_shas"].get(f)
               for f in EXPECTED):
            print("R3-41B already applied; no modifications")
            return
        raise ValueError("Existing R3-41B state does not match current files")
    old = {name: (ROOT / name).read_bytes() for name in EXPECTED}
    for filename, data in old.items():
        if _sha(data) != EXPECTED[filename]:
            raise ValueError(
                f"R3-41A audited source SHA mismatch: {filename}; no changes made"
            )
    transformed = {
        "phase168_r3_3_proof_narrative_model.py":
            _transform_model(old["phase168_r3_3_proof_narrative_model.py"]),
        "phase168_r3_5_model_renderer.py":
            _transform_renderer(old["phase168_r3_5_model_renderer.py"]),
    }
    backup_name = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")
    backup = PACKAGE / "backup" / backup_name
    backup.mkdir(parents=True, exist_ok=False)
    for filename in EXPECTED:
        (backup / filename).write_bytes(old[filename])
    try:
        for filename, data in transformed.items():
            (ROOT / filename).write_bytes(data)
            print("PATCHED", filename)
        for filename, data in transformed.items():
            if (ROOT / filename).read_bytes() != data:
                raise ValueError("Patch output was not preserved: " + filename)
        state = {
            "backup_name": backup_name,
            "installed_shas": {name: _sha(content) for name, content in transformed.items()},
        }
        STATE.write_text(json.dumps(state, indent=2) + "\n", encoding="utf-8")
        full = PACKAGE / "full_files"
        full.mkdir(exist_ok=True)
        for filename, data in transformed.items():
            (full / filename).write_bytes(data)
            print("FULL_FILE", full / filename)
    except Exception:
        for filename in EXPECTED:
            (ROOT / filename).write_bytes(old[filename])
        if STATE.exists():
            STATE.unlink()
        raise


def main() -> None:
    if len(sys.argv) > 2 or (len(sys.argv) == 2 and sys.argv[1] != "--rollback"):
        raise SystemExit("Usage: python -m phase168_r3_41b1_citation_fixture_fix.apply [--rollback]")
    if len(sys.argv) == 2:
        _rollback()
    else:
        _apply()


if __name__ == "__main__":
    main()
