"""Install the R3-41O minimal renderer + focused test compatibility update."""
from __future__ import annotations

import ast
import hashlib
import json
from pathlib import Path

BASE = Path(__file__).resolve().parent
REPO = BASE.parent
OUT = BASE / "output"
RENDERER = REPO / "phase168_r3_5_model_renderer.py"
N_TEST = REPO / "phase168_r3_41n1_import_scope_fix" / "tests" / "test_phase168_r3_41n_composed_proof_display.py"
EXPECTED_RENDERER = "e88c08ce09e253e52464f7aed94275fe3ec66961235090613508c4a3acff434c"
EXPECTED_N_TEST = "e6cf946c0220c59aa5463eda0c1aecdf6347a9aa61bdf60b89f67aabef18f564"


def checksum(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def replace_function(original: bytes, replacement: Path, function_name: str) -> bytes:
    text = original.decode("utf-8-sig")
    source = replacement.read_text(encoding="utf-8")
    nodes = [node for node in ast.parse(text).body
             if isinstance(node, ast.FunctionDef) and node.name == function_name]
    new_nodes = [node for node in ast.parse(source).body
                 if isinstance(node, ast.FunctionDef) and node.name == function_name]
    if len(nodes) != 1 or len(new_nodes) != 1:
        raise ValueError("Expected exactly one complete function")
    node = nodes[0]
    lines = text.splitlines(keepends=True)
    newline = "\r\n" if b"\r\n" in original else "\n"
    result = ("".join(lines[:node.lineno-1])
              + source.rstrip("\r\n").replace("\n", newline) + newline
              + "".join(lines[node.end_lineno:]))
    ast.parse(result)
    return (b"\xef\xbb\xbf" if original.startswith(b"\xef\xbb\xbf") else b"") + result.encode("utf-8")


def run() -> None:
    old_renderer = RENDERER.read_bytes()
    old_test = N_TEST.read_bytes()
    actual = (checksum(old_renderer), checksum(old_test))
    expected = (EXPECTED_RENDERER, EXPECTED_N_TEST)
    if actual != expected:
        raise RuntimeError("R3-41O requires R3-41N1 PASS state: expected " + repr(expected)
                           + " actual " + repr(actual) + ". No changes made.")
    after_renderer = replace_function(old_renderer, BASE / "renderer_function_full.py",
                                      "render_model_backed_narrative_markdown")
    newline = "\r\n" if b"\r\n" in old_test else "\n"
    revised_test = (BASE / "updated_r341n_test_full.py").read_text(encoding="utf-8")
    ast.parse(revised_test)
    after_test = ((b"\xef\xbb\xbf" if old_test.startswith(b"\xef\xbb\xbf") else b"")
                  + revised_test.replace("\n", newline).encode("utf-8"))
    entries = ((RENDERER, old_renderer, after_renderer), (N_TEST, old_test, after_test))
    OUT.mkdir(parents=True, exist_ok=True)
    for path, old, after in entries:
        if old == after:
            raise ValueError("No change: " + str(path))
        backup = OUT / (path.name + ".before")
        if backup.exists() and backup.read_bytes() != old:
            raise RuntimeError("Backup already exists with different contents: " + str(backup))
    for path, old, after in entries:
        backup = OUT / (path.name + ".before")
        backup.write_bytes(old)
        if backup.read_bytes() != old:
            raise RuntimeError("Backup verification failed")
    completed = []
    try:
        for path, old, after in entries:
            path.write_bytes(after)
            if path.read_bytes() != after:
                raise RuntimeError("Write verification failed: " + str(path))
            completed.append((path, old))
            (OUT / (path.name + ".full.py")).write_bytes(after)
            print("PATCHED", path)
            print("BACKUP", OUT / (path.name + ".before"))
    except BaseException:
        for path, old in reversed(completed):
            path.write_bytes(old)
        raise
    (OUT / "install.json").write_text(json.dumps({
        "changes": [{"file": str(path), "old_sha256": checksum(old),
                     "new_sha256": checksum(after)} for path,old,after in entries],
        "full_pytest_not_run": True,
    }, ensure_ascii=False, indent=2), encoding="utf-8")
    print("FULL_RENDERER_FUNCTION", BASE / "renderer_function_full.py")
    print("FULL_RENDERER_FILE", OUT / (RENDERER.name + ".full.py"))
    print("FULL_TEST_FILE", BASE / "updated_r341n_test_full.py")


if __name__ == "__main__":
    run()
