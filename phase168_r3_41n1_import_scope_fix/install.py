"""R3-41N1 guarded repair of R3-41N import-scope error."""
from __future__ import annotations

import ast
import hashlib
import json
from pathlib import Path

PACKAGE = Path(__file__).resolve().parent
REPO = PACKAGE.parent
TARGET = REPO / "phase168_r3_5_model_renderer.py"
OUTPUT = PACKAGE / "output"
EXPECTED_SHA = "4d0f1b509c6e92704db96e73b6da00220235b6300c9adaa432e062b3ea2b5e51"
EXPECTED_TEST_SHA = "6cda3248f3ef0afe059a67845ce365ca7bb9302168ffd4bc78d36c22ff383112"
TEST_TARGET = REPO / "phase168_r3_41l_reasoned_prose" / "tests" / "test_phase168_r3_41l_reasoned_prose.py"


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def only_function(source: str, function_name: str):
    matches = [n for n in ast.parse(source).body
               if isinstance(n, ast.FunctionDef) and n.name == function_name]
    if len(matches) != 1:
        raise ValueError("Expected exactly one top-level function: " + function_name)
    return matches[0]


def install() -> int:
    before = TARGET.read_bytes()
    before_test = TEST_TARGET.read_bytes()
    if digest(before) != EXPECTED_SHA:
        raise RuntimeError("R3-41N1 requires restored R3-41M2 renderer; found: found " + digest(before)
                           + "; no change made")
    if digest(before_test) != EXPECTED_TEST_SHA:
        raise RuntimeError("R3-41N1 requires restored R3-41M2 test; found: found " + digest(before_test)
                           + "; no change made")
    text = before.decode("utf-8-sig")
    new_function = (PACKAGE / "renderer_function_full.py").read_text(encoding="utf-8")
    old_node = only_function(text, "render_model_backed_narrative_markdown")
    only_function(new_function, "render_model_backed_narrative_markdown")
    old_lines = text.splitlines(keepends=True)
    newline = "\r\n" if b"\r\n" in before else "\n"
    updated_text = ("".join(old_lines[:old_node.lineno - 1])
                    + new_function.rstrip("\r\n").replace("\n", newline) + newline
                    + "".join(old_lines[old_node.end_lineno:]))
    ast.parse(updated_text)
    after = ((b"\xef\xbb\xbf" if before.startswith(b"\xef\xbb\xbf") else b"")
             + updated_text.encode("utf-8"))
    revised_test = (PACKAGE / "r341l_test_full.py").read_text(encoding="utf-8")
    ast.parse(revised_test)
    test_newline = "\r\n" if b"\r\n" in before_test else "\n"
    after_test = ((b"\xef\xbb\xbf" if before_test.startswith(b"\xef\xbb\xbf") else b"")
                  + revised_test.replace("\n", test_newline).encode("utf-8"))
    patches = ((TARGET, before, after), (TEST_TARGET, before_test, after_test))
    OUTPUT.mkdir(parents=True, exist_ok=True)
    for path, old, new in patches:
        if old == new:
            raise RuntimeError("Patch has no content change: " + str(path))
        backup = OUTPUT / (path.name + ".before")
        if backup.exists() and backup.read_bytes() != old:
            raise RuntimeError("Backup exists with different bytes; no change made: " + str(backup))
    for path, old, new in patches:
        backup = OUTPUT / (path.name + ".before")
        if not backup.exists():
            backup.write_bytes(old)
        if backup.read_bytes() != old:
            raise RuntimeError("Backup verification failed; no change made")
    written = []
    try:
        for path, old, new in patches:
            path.write_bytes(new)
            if path.read_bytes() != new:
                raise RuntimeError("Write verification failed: " + str(path))
            written.append((path, old))
            (OUTPUT / (path.name + ".full.py")).write_bytes(new)
    except BaseException:
        for path, old in reversed(written):
            path.write_bytes(old)
            if path.read_bytes() != old:
                raise RuntimeError("Rollback failed: " + str(path))
        raise
    (OUTPUT / "install.json").write_text(json.dumps({
        "changes": [{"file": str(path), "before_sha256": digest(old),
                     "after_sha256": digest(new)} for path, old, new in patches],
        "full_suite_tested": False}, ensure_ascii=False, indent=2), encoding="utf-8")
    for path, old, new in patches:
        print("PATCHED", path)
        print("BACKUP", OUTPUT / (path.name + ".before"))
        print("FULL_FILE", OUTPUT / (path.name + ".full.py"))
    print("FULL_FUNCTION", PACKAGE / "renderer_function_full.py")
    print("FULL_TEST_FILE", PACKAGE / "r341l_test_full.py")
    return 0


if __name__ == "__main__":
    raise SystemExit(install())
