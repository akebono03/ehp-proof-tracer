"""R3I guarded minimal installer; validates the applied R3H source state."""
from __future__ import annotations

import ast
import subprocess
import sys
from pathlib import Path

PACKAGE = Path(__file__).resolve().parent
ROOT = PACKAGE.parent
SHARED = ROOT / "phase165_r52_r9_shared_math.py"
ADAPTER = ROOT / "phase165_r14_r5_ehp_connection.py"
R3H_MODULE = ROOT / "phase169_r3h_source_registry.py"
R3H_MODULE_REVIEWED = PACKAGE / "reviewed_r3h" / "phase169_r3h_source_registry.py"
R3H_FUNCTION = PACKAGE / "reviewed_r3h" / "build_shared_typed_bridge.py"
SHARED_FUNCTION = PACKAGE / "full_functions" / "shared_expansion_provider.py"
ADDED_FUNCTION = PACKAGE / "full_functions" / "expand_cited_ehp_terminal_goal.py"
OUTPUT = PACKAGE / "output"
SHARED_BACKUP = OUTPUT / "phase165_r52_r9_shared_math.py.before"
ADAPTER_BACKUP = OUTPUT / "phase165_r14_r5_ehp_connection.py.before"
SHARED_AFTER = OUTPUT / "phase165_r52_r9_shared_math.py.full.py"
ADAPTER_AFTER = OUTPUT / "phase165_r14_r5_ehp_connection.py.full.py"
R3F3_SHARED_BLOB = "628395c31025828c645f5641536913c56afafcb3"
R3F3_ADAPTER_BLOB = "ff134de5cefb62b9586209d4dfc8533a6be479f8"


def git(*args: str) -> bytes:
    proc = subprocess.run(("git",) + args, cwd=ROOT, capture_output=True)
    if proc.returncode:
        raise RuntimeError(proc.stderr.decode("utf-8", errors="replace"))
    return proc.stdout


def normalize(data: bytes) -> str:
    return data.decode("utf-8-sig").replace("\r\n", "\n")


def preserve_format(original: bytes, text: str) -> bytes:
    bom = b"\xef\xbb\xbf" if original.startswith(b"\xef\xbb\xbf") else b""
    newline = "\r\n" if b"\r\n" in original else "\n"
    return bom + text.replace("\n", newline).encode("utf-8")


def require_single_function(source: str, name: str) -> ast.FunctionDef:
    nodes = tuple(n for n in ast.parse(source).body
                  if isinstance(n, ast.FunctionDef) and n.name == name)
    if len(nodes) != 1:
        raise ValueError("expected exactly one function: " + name)
    return nodes[0]


def replace_whole_function(source: str, full_function: str, name: str) -> str:
    old = require_single_function(source, name)
    new_tree = ast.parse(full_function)
    if (len(new_tree.body) != 1
            or not isinstance(new_tree.body[0], ast.FunctionDef)
            or new_tree.body[0].name != name):
        raise ValueError("full replacement is not exactly " + name)
    lines = source.splitlines(keepends=True)
    return "".join(lines[:old.lineno - 1]) + (full_function if full_function.endswith("\n") else full_function + "\n") + "".join(lines[old.end_lineno:])


def insert_whole_function(source: str, full_function: str, name: str, before: str) -> str:
    tree = ast.parse(full_function)
    if (len(tree.body) != 1 or not isinstance(tree.body[0], ast.FunctionDef)
            or tree.body[0].name != name):
        raise ValueError("new function payload invalid: " + name)
    if any(isinstance(node, ast.FunctionDef) and node.name == name for node in ast.parse(source).body):
        raise ValueError("function unexpectedly already present: " + name)
    anchor = require_single_function(source, before)
    lines = source.splitlines(keepends=True)
    return "".join(lines[:anchor.lineno - 1]) + full_function.rstrip("\n") + "\n\n\n" + "".join(lines[anchor.lineno - 1:])


def expected_r3h_shared() -> str:
    blob = git("rev-parse", "HEAD:phase165_r52_r9_shared_math.py").decode().strip()
    r3h_body = R3H_FUNCTION.read_text(encoding="utf-8")
    if blob == R3F3_SHARED_BLOB:
        base = normalize(git("show", "HEAD:phase165_r52_r9_shared_math.py"))
    else:
        # Also accept the immediately following, committed R3H state,
        # but *only* if the entire file is the exact reviewed R3H replacement.
        parent_blob = git("rev-parse", "HEAD^:phase165_r52_r9_shared_math.py").decode().strip()
        if parent_blob != R3F3_SHARED_BLOB:
            raise ValueError("unreviewed shared-math Git baseline: " + blob)
        base = normalize(git("show", "HEAD^:phase165_r52_r9_shared_math.py"))
    expected = replace_whole_function(base, r3h_body, "build_shared_typed_bridge")
    if blob != R3F3_SHARED_BLOB:
        committed = normalize(git("show", "HEAD:phase165_r52_r9_shared_math.py"))
        if committed != expected:
            raise ValueError("committed shared math differs from exact reviewed R3H")
    return expected


def install() -> int:
    required = (SHARED, ADAPTER, R3H_MODULE, R3H_MODULE_REVIEWED,
                R3H_FUNCTION, SHARED_FUNCTION, ADDED_FUNCTION)
    if not all(path.is_file() for path in required):
        print("REFUSED: missing reviewed R3H or R3I dependency")
        return 2
    shared_current = SHARED.read_bytes()
    adapter_current = ADAPTER.read_bytes()
    if any(p.exists() for p in (SHARED_BACKUP, ADAPTER_BACKUP, SHARED_AFTER, ADAPTER_AFTER)):
        if (all(p.is_file() for p in (SHARED_BACKUP, ADAPTER_BACKUP, SHARED_AFTER, ADAPTER_AFTER))
                and shared_current == SHARED_AFTER.read_bytes()
                and adapter_current == ADAPTER_AFTER.read_bytes()):
            print("ALREADY_APPLIED: R3I reviewed two-file result")
            return 0
        print("REFUSED: existing backup or unknown installed source")
        return 3
    if R3H_MODULE.read_bytes() != R3H_MODULE_REVIEWED.read_bytes():
        print("REFUSED: R3H source registry differs from reviewed payload")
        return 4
    try:
        expected = expected_r3h_shared()
        if normalize(shared_current) != expected:
            print("REFUSED: R3H function/source does not match reviewed state")
            return 5
        adapter_blob = git("rev-parse", "HEAD:phase165_r14_r5_ehp_connection.py").decode().strip()
        if adapter_blob != R3F3_ADAPTER_BLOB:
            print("REFUSED: historical EHP adapter changed", adapter_blob)
            return 6
        if normalize(adapter_current) != normalize(git("show", "HEAD:phase165_r14_r5_ehp_connection.py")):
            print("REFUSED: historical EHP adapter has local modifications")
            return 7
        modified_shared = replace_whole_function(
            expected, SHARED_FUNCTION.read_text(encoding="utf-8"),
            "shared_expansion_provider",
        )
        modified_adapter = insert_whole_function(
            normalize(adapter_current), ADDED_FUNCTION.read_text(encoding="utf-8"),
            "expand_cited_ehp_terminal_goal", "audit_ehp_connection",
        )
        if (modified_shared.count("options.extend(expand_cited_ehp_terminal_goal(") != 1
                or modified_adapter.count("def expand_cited_ehp_terminal_goal(") != 1):
            print("REFUSED: R3I provider connected unexpectedly")
            return 8
        ast.parse(modified_shared)
        ast.parse(modified_adapter)
    except (RuntimeError, ValueError, SyntaxError) as exc:
        print("REFUSED:", str(exc))
        return 9
    new_shared = preserve_format(shared_current, modified_shared)
    new_adapter = preserve_format(adapter_current, modified_adapter)
    OUTPUT.mkdir(parents=True, exist_ok=True)
    SHARED_BACKUP.write_bytes(shared_current)
    ADAPTER_BACKUP.write_bytes(adapter_current)
    SHARED_AFTER.write_bytes(new_shared)
    ADAPTER_AFTER.write_bytes(new_adapter)
    try:
        SHARED.write_bytes(new_shared)
        ADAPTER.write_bytes(new_adapter)
        if SHARED.read_bytes() != new_shared or ADAPTER.read_bytes() != new_adapter:
            raise RuntimeError("post-write verification failure")
    except Exception:
        if SHARED.is_file() and SHARED.read_bytes() in (shared_current, new_shared):
            SHARED.write_bytes(shared_current)
        if ADAPTER.is_file() and ADAPTER.read_bytes() in (adapter_current, new_adapter):
            ADAPTER.write_bytes(adapter_current)
        raise
    print("PATCHED:", SHARED)
    print("PATCHED:", ADAPTER)
    print("BACKUPS:", SHARED_BACKUP, ADAPTER_BACKUP)
    print("FULL_FILES:", SHARED_AFTER, ADAPTER_AFTER)
    print("FULL_FUNCTIONS:", SHARED_FUNCTION, ADDED_FUNCTION)
    return 0


def restore() -> int:
    required = (SHARED_BACKUP, ADAPTER_BACKUP, SHARED_AFTER, ADAPTER_AFTER)
    if not all(p.is_file() for p in required):
        print("REFUSED_RESTORE: backups or patched snapshots missing")
        return 11
    if SHARED.read_bytes() != SHARED_AFTER.read_bytes() or ADAPTER.read_bytes() != ADAPTER_AFTER.read_bytes():
        print("REFUSED_RESTORE: modified files since installation")
        return 12
    SHARED.write_bytes(SHARED_BACKUP.read_bytes())
    ADAPTER.write_bytes(ADAPTER_BACKUP.read_bytes())
    print("RESTORED:", SHARED)
    print("RESTORED:", ADAPTER)
    return 0


if __name__ == "__main__":
    if len(sys.argv) != 2 or sys.argv[1] not in ("install", "restore"):
        raise SystemExit("Usage: python apply.py install|restore")
    raise SystemExit(install() if sys.argv[1] == "install" else restore())
