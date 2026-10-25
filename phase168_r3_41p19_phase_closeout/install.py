"""Apply only one reviewed proof verifier function, with safe retry semantics."""
from __future__ import annotations

import ast
import hashlib
import json
from pathlib import Path

PACKAGE = Path(__file__).resolve().parent
ROOT = PACKAGE.parent
TARGET = ROOT / "phase168_r3_41p13_trust_boundary" / "verification.py"
OUTPUT = PACKAGE / "output"
NAME = "verify_proof_tree_for_narrative"


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def function_node(source: str) -> ast.FunctionDef:
    matches = [node for node in ast.parse(source).body
               if isinstance(node, ast.FunctionDef) and node.name == NAME]
    if len(matches) != 1:
        raise RuntimeError("expected exactly one verifier function")
    return matches[0]


def install() -> None:
    OUTPUT.mkdir(parents=True, exist_ok=True)
    manifest_path = OUTPUT / "manifest.json"
    if manifest_path.exists():
        raise RuntimeError("an active installation manifest already exists")
    original = TARGET.read_bytes()
    source = original.decode("utf-8-sig")
    old_node = function_node(source)
    expected = (PACKAGE / "full_functions" / (NAME + "_BEFORE.py")).read_text(encoding="utf-8")
    after = (PACKAGE / "full_functions" / (NAME + "_FULL.py")).read_text(encoding="utf-8")
    if (ast.dump(old_node, include_attributes=False)
            != ast.dump(function_node(expected), include_attributes=False)):
        raise RuntimeError("current verifier differs from the reviewed develop baseline")
    lines = source.splitlines(keepends=True)
    modified = "".join(lines[:old_node.lineno - 1]) + after.rstrip("\n") + "\n" + "".join(lines[old_node.end_lineno:])
    ast.parse(modified)
    eol = "\r\n" if b"\r\n" in original else "\n"
    content = modified.replace("\r\n", "\n").replace("\n", eol).encode("utf-8")
    if original.startswith(b"\xef\xbb\xbf"):
        content = b"\xef\xbb\xbf" + content
    backup_path = OUTPUT / "verification.py.before"
    if backup_path.exists():
        if backup_path.read_bytes() != original:
            raise RuntimeError("existing backup differs; refusing overwrite")
    else:
        backup_path.write_bytes(original)
    manifest = {
        "target": str(TARGET.relative_to(ROOT)),
        "backup": backup_path.name,
        "before_sha256": digest(original),
        "after_sha256": digest(content),
    }
    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    try:
        if TARGET.read_bytes() != original:
            raise RuntimeError("source changed before installation")
        TARGET.write_bytes(content)
        (OUTPUT / "verification.py.FULL.py").write_bytes(content)
    except BaseException:
        if TARGET.read_bytes() == content:
            TARGET.write_bytes(original)
        manifest_path.unlink(missing_ok=True)
        raise
    print("PATCHED", TARGET)
    print("BACKUP", backup_path)
    print("FULL_FILE", OUTPUT / "verification.py.FULL.py")


if __name__ == "__main__":
    install()
