"""R3-41L: fail-closed, whole-function patch of the current shared renderer."""
from __future__ import annotations

import ast
import hashlib
import json
from pathlib import Path

PACKAGE = Path(__file__).resolve().parent
ROOT = PACKAGE.parent
TARGET = ROOT / "phase168_r3_5_model_renderer.py"
FULL_FUNCTION = PACKAGE / "modified_function_full.py"
OUTPUT = PACKAGE / "output"
BACKUP = OUTPUT / "phase168_r3_5_model_renderer.py.before"
FULL_FILE = OUTPUT / "phase168_r3_5_model_renderer.py"
EXPECTED_SHA256 = "1e60a98a3b76f4544d053ac97cc6deb3bb321c0b41ce3c0991bee7a0277ea92f"


def sha256(content: bytes) -> str:
    return hashlib.sha256(content).hexdigest()


def patch_function(content: bytes, replacement: str) -> bytes:
    old_text = content.decode("utf-8-sig")
    root = ast.parse(old_text)
    nodes = [node for node in root.body if isinstance(node, ast.FunctionDef)
             and node.name == "render_model_backed_narrative_markdown"]
    if len(nodes) != 1:
        raise RuntimeError("expected exactly one shared renderer function")
    new_nodes = ast.parse(replacement).body
    if (len(new_nodes) != 1 or not isinstance(new_nodes[0], ast.FunctionDef)
            or new_nodes[0].name != "render_model_backed_narrative_markdown"):
        raise RuntimeError("replacement must contain exactly one complete renderer function")
    lines = old_text.splitlines(keepends=True)
    node = nodes[0]
    newline = "\r\n" if b"\r\n" in content else "\n"
    text = "".join(lines[:node.lineno - 1])
    text += replacement.replace("\r\n", "\n").replace("\n", newline)
    text += "".join(lines[node.end_lineno:])
    ast.parse(text)
    prefix = b"\xef\xbb\xbf" if content.startswith(b"\xef\xbb\xbf") else b""
    return prefix + text.encode("utf-8")


def main() -> int:
    original = TARGET.read_bytes()
    if sha256(original) != EXPECTED_SHA256:
        raise RuntimeError(
            "R3-41J2 verified Renderer source is required; nothing patched. "
            "sha256=" + sha256(original)
        )
    replacement = FULL_FUNCTION.read_text(encoding="utf-8")
    patched = patch_function(original, replacement)
    if patched == original:
        raise RuntimeError("no scoped renderer change found")
    OUTPUT.mkdir(parents=True, exist_ok=True)
    if BACKUP.exists() and BACKUP.read_bytes() != original:
        raise RuntimeError("existing backup differs from current source; nothing patched")
    if not BACKUP.exists():
        BACKUP.write_bytes(original)
    FULL_FILE.write_bytes(patched)
    try:
        TARGET.write_bytes(patched)
        if TARGET.read_bytes() != patched:
            raise RuntimeError("post-write renderer verification failed")
    except BaseException:
        TARGET.write_bytes(original)
        raise
    report = {
        "phase": "168 R3-41L",
        "changed_files": [str(TARGET)],
        "function": "render_model_backed_narrative_markdown",
        "old_sha256": sha256(original),
        "new_sha256": sha256(patched),
        "full_file": str(FULL_FILE),
        "full_function": str(FULL_FUNCTION),
        "full_pytest_run": False,
    }
    (OUTPUT / "install.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("PATCHED", TARGET)
    print("BACKUP", BACKUP)
    print("FULL_FUNCTION", FULL_FUNCTION)
    print("FULL_FILE", FULL_FILE)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
