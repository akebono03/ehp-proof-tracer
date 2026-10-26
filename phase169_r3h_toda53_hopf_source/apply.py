"""Guarded R3H: add one explicit cited source; replace one whole function."""
from __future__ import annotations

import ast
import subprocess
import sys
from pathlib import Path

PACKAGE = Path(__file__).resolve().parent
ROOT = PACKAGE.parent
SOURCE_PATH = ROOT / "phase165_r52_r9_shared_math.py"
MODULE_PATH = ROOT / "phase169_r3h_source_registry.py"
FULL_FUNCTION = PACKAGE / "full_functions" / "build_shared_typed_bridge.py"
NEW_MODULE = PACKAGE / "phase169_r3h_source_registry.py"
OUTPUT = PACKAGE / "output"
BACKUP = OUTPUT / "phase165_r52_r9_shared_math.py.before"
INSTALLED_SNAPSHOT = OUTPUT / "phase165_r52_r9_shared_math.py.full.py"
INSTALLED_MODULE = OUTPUT / "phase169_r3h_source_registry.py.full.py"
EXPECTED_BLOB = "628395c31025828c645f5641536913c56afafcb3"


def git(*arguments: str) -> bytes:
    result = subprocess.run(
        ("git",) + arguments, cwd=ROOT, capture_output=True,
    )
    if result.returncode:
        raise RuntimeError("Git error: " + result.stderr.decode("utf-8", errors="replace"))
    return result.stdout


def normalized(data: bytes) -> str:
    return data.decode("utf-8-sig").replace("\r\n", "\n")


def match_format(original: bytes, new_source: str) -> bytes:
    bom = b"\xef\xbb\xbf" if original.startswith(b"\xef\xbb\xbf") else b""
    newline = "\r\n" if b"\r\n" in original else "\n"
    return bom + new_source.replace("\n", newline).encode("utf-8")


def replace_entire_function(original: str, function: str, name: str) -> str:
    old_tree = ast.parse(original)
    new_tree = ast.parse(function)
    if (len(new_tree.body) != 1
            or not isinstance(new_tree.body[0], ast.FunctionDef)
            or new_tree.body[0].name != name):
        raise ValueError("full-function payload does not define exactly " + name)
    matches = tuple(
        node for node in old_tree.body
        if isinstance(node, ast.FunctionDef) and node.name == name
    )
    if len(matches) != 1:
        raise ValueError("expected one existing " + name)
    node = matches[0]
    original_lines = original.splitlines(keepends=True)
    return "".join(
        original_lines[:node.lineno - 1]
        + function.splitlines(keepends=True)
        + original_lines[node.end_lineno:]
    )


def install() -> int:
    if not SOURCE_PATH.is_file() or not FULL_FUNCTION.is_file() or not NEW_MODULE.is_file():
        print("REFUSED: required source or complete replacement files missing")
        return 2
    current = SOURCE_PATH.read_bytes()
    wanted_module = NEW_MODULE.read_bytes()
    if BACKUP.exists() or INSTALLED_SNAPSHOT.exists() or INSTALLED_MODULE.exists():
        if (BACKUP.is_file() and INSTALLED_SNAPSHOT.is_file() and INSTALLED_MODULE.is_file()
                and current == INSTALLED_SNAPSHOT.read_bytes()
                and MODULE_PATH.is_file()
                and MODULE_PATH.read_bytes() == INSTALLED_MODULE.read_bytes()
                and MODULE_PATH.read_bytes() == wanted_module):
            print("ALREADY_APPLIED: R3H source and full function verified")
            return 0
        print("REFUSED: backup exists or unexpected installed content")
        return 3
    if MODULE_PATH.exists():
        print("REFUSED: new module already exists and is not controlled by R3H")
        return 4
    recorded_blob = git("rev-parse", "HEAD:phase165_r52_r9_shared_math.py").decode().strip()
    if recorded_blob != EXPECTED_BLOB:
        print("REFUSED: Git blob differs from reviewed R3F3 baseline", recorded_blob)
        return 5
    committed = normalized(git("show", "HEAD:phase165_r52_r9_shared_math.py"))
    if normalized(current) != committed:
        print("REFUSED: production function differs from reviewed Git baseline")
        return 6
    if ("expand_registered_ehp_terminal_goal" not in committed
            or "expand_registered_ehp_goal" not in committed):
        print("REFUSED: R3F3 EHP adapters are not connected")
        return 7
    new_function = FULL_FUNCTION.read_text(encoding="utf-8")
    new_source = replace_entire_function(committed, new_function, "build_shared_typed_bridge")
    if new_source.count("build_adopted_toda53_hopf_reference(production)") != 1:
        print("REFUSED: newly adopted source not connected exactly once")
        return 8
    ast.parse(new_source, filename=str(SOURCE_PATH))
    ast.parse(wanted_module.decode("utf-8"), filename=str(MODULE_PATH))
    written = match_format(current, new_source)
    OUTPUT.mkdir(parents=True, exist_ok=True)
    BACKUP.write_bytes(current)
    INSTALLED_SNAPSHOT.write_bytes(written)
    INSTALLED_MODULE.write_bytes(wanted_module)
    try:
        MODULE_PATH.write_bytes(wanted_module)
        SOURCE_PATH.write_bytes(written)
        if (MODULE_PATH.read_bytes() != wanted_module
                or SOURCE_PATH.read_bytes() != written):
            raise RuntimeError("post-write verification failed")
    except Exception:
        if SOURCE_PATH.is_file() and SOURCE_PATH.read_bytes() in (current, written):
            SOURCE_PATH.write_bytes(current)
        if MODULE_PATH.is_file() and MODULE_PATH.read_bytes() == wanted_module:
            MODULE_PATH.unlink()
        raise
    print("PATCHED:", SOURCE_PATH)
    print("BACKUP:", BACKUP)
    print("FULL_FUNCTION:", FULL_FUNCTION)
    print("FULL_FILE:", INSTALLED_SNAPSHOT)
    print("NEW_MODULE:", MODULE_PATH)
    return 0


def restore() -> int:
    if not BACKUP.is_file() or not INSTALLED_SNAPSHOT.is_file() or not INSTALLED_MODULE.is_file():
        print("REFUSED_RESTORE: backup or patched snapshots missing")
        return 11
    if (SOURCE_PATH.read_bytes() != INSTALLED_SNAPSHOT.read_bytes()
            or not MODULE_PATH.is_file()
            or MODULE_PATH.read_bytes() != INSTALLED_MODULE.read_bytes()):
        print("REFUSED_RESTORE: production files changed after R3H")
        return 12
    SOURCE_PATH.write_bytes(BACKUP.read_bytes())
    MODULE_PATH.unlink()
    print("RESTORED:", SOURCE_PATH)
    print("REMOVED:", MODULE_PATH)
    return 0


if __name__ == "__main__":
    if len(sys.argv) != 2 or sys.argv[1] not in ("install", "restore"):
        raise SystemExit("Usage: python apply.py install|restore")
    raise SystemExit(install() if sys.argv[1] == "install" else restore())
