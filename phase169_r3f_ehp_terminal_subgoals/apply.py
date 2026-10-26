"""Guarded R3F two-module patch, with atomic preparation and safe restore."""
from __future__ import annotations

import ast
import subprocess
import sys
from pathlib import Path

PACKAGE = Path(__file__).resolve().parent
ROOT = PACKAGE.parent
SHARED = Path("phase165_r52_r9_shared_math.py")
CONNECTION = Path("phase165_r14_r5_ehp_connection.py")
OLD_PROVIDER = ROOT / "phase169_r3e1_ehp_audit_module_fix" / "full_functions" / "shared_expansion_provider.py"
NEW_PROVIDER = PACKAGE / "full_functions" / "shared_expansion_provider.py"
TERMINAL = PACKAGE / "full_functions" / "expand_registered_ehp_terminal_goal.py"
EXPECTED_BLOBS = {
    SHARED: "36a4c355758ee55ba4d39606a8e0f281bb43efff",
    CONNECTION: "e76a0a772a709aff94b31583c4e80291b2537f36",
}


def git(*args: str) -> str:
    run = subprocess.run(("git",) + args, cwd=ROOT, capture_output=True,
                         encoding="utf-8", errors="replace", text=True)
    if run.returncode:
        raise RuntimeError("git failed: " + run.stderr.strip())
    return run.stdout


def normalized(data: bytes) -> str:
    return data.decode("utf-8-sig").replace("\r\n", "\n")


def same_format(data: bytes, changed: str) -> bytes:
    bom = b"\xef\xbb\xbf" if data.startswith(b"\xef\xbb\xbf") else b""
    nl = "\r\n" if b"\r\n" in data else "\n"
    return bom + changed.replace("\n", nl).encode("utf-8")


def function_replace(source: str, name: str, replacement: str) -> str:
    old_tree = ast.parse(source)
    new_tree = ast.parse(replacement)
    if len(new_tree.body) != 1 or not isinstance(new_tree.body[0], ast.FunctionDef) or new_tree.body[0].name != name:
        raise ValueError("invalid entire replacement function: " + name)
    matches = [x for x in old_tree.body if isinstance(x, ast.FunctionDef) and x.name == name]
    if len(matches) != 1:
        raise ValueError("expected one original function: " + name)
    node = matches[0]
    return "".join(source.splitlines(keepends=True)[:node.lineno-1]
                   + replacement.splitlines(keepends=True)
                   + source.splitlines(keepends=True)[node.end_lineno:])


def connection_insert(source: str, replacement: str) -> str:
    tree = ast.parse(source)
    if any(isinstance(x, ast.FunctionDef) and x.name == "expand_registered_ehp_terminal_goal" for x in tree.body):
        raise ValueError("terminal expansion function already present")
    anchors = [x for x in tree.body if isinstance(x, ast.FunctionDef) and x.name == "audit_ehp_connection"]
    if len(anchors) != 1:
        raise ValueError("missing unique audit_ehp_connection insertion anchor")
    lines = source.splitlines(keepends=True)
    line = anchors[0].lineno-1
    return "".join(lines[:line] + [replacement + "\n\n"] + lines[line:])


def paths(which: Path) -> tuple[Path, Path, Path]:
    target = ROOT / which
    backup = PACKAGE / "output" / (which.name + ".before")
    patched = PACKAGE / "output" / (which.name + ".full.py")
    return target, backup, patched


def restore() -> int:
    prepared = []
    for rel in (SHARED, CONNECTION):
        target, backup, patched = paths(rel)
        if not backup.is_file() or not patched.is_file():
            print("REFUSED_RESTORE: backup or registered patched file missing:", rel)
            return 3
        if target.read_bytes() != patched.read_bytes():
            print("REFUSED_RESTORE: production file has changed:", rel)
            return 4
        prepared.append((target, backup.read_bytes()))
    for target, original in prepared:
        target.write_bytes(original)
        print("RESTORED:", target)
    return 0


def install() -> int:
    expected = []
    for rel in (SHARED, CONNECTION):
        target, backup, patched = paths(rel)
        if not target.is_file():
            print("REFUSED: missing production file", rel)
            return 2
        old_bytes = target.read_bytes()
        if backup.exists() or patched.exists():
            if backup.exists() and patched.exists() and old_bytes == patched.read_bytes():
                expected.append((target, None, None, backup, patched))
                continue
            print("REFUSED: previous backup/patch exists or unexpected production change", rel)
            return 5
        git_blob = git("rev-parse", "HEAD:" + rel.as_posix()).strip()
        if git_blob != EXPECTED_BLOBS[rel]:
            print("REFUSED: reviewed GitHub blob changed", rel, git_blob)
            return 6
        base = normalized(git("show", "HEAD:" + rel.as_posix()).encode("utf-8"))
        if rel == SHARED:
            old_fn = OLD_PROVIDER.read_text(encoding="utf-8")
            old_expected = function_replace(base, "shared_expansion_provider", old_fn)
            if normalized(old_bytes) != old_expected:
                print("REFUSED: R3E1 provider is not exactly installed", rel)
                return 7
            changed = function_replace(old_expected, "shared_expansion_provider", NEW_PROVIDER.read_text(encoding="utf-8"))
        else:
            if normalized(old_bytes) != base:
                print("REFUSED: EHP connection module is not pristine", rel)
                return 8
            changed = connection_insert(base, TERMINAL.read_text(encoding="utf-8"))
        ast.parse(changed, filename=str(rel))
        expected.append((target, old_bytes, same_format(old_bytes, changed), backup, patched))
    if all(record[1] is None for record in expected):
        print("ALREADY_APPLIED: both production modules match R3F outputs")
        return 0
    if any(record[1] is None for record in expected):
        print("REFUSED: partially applied R3F package")
        return 9
    try:
        for target, original, changed, backup, patched in expected:
            backup.parent.mkdir(parents=True, exist_ok=True)
            backup.write_bytes(original)
            patched.write_bytes(changed)
        for target, original, changed, backup, patched in expected:
            target.write_bytes(changed)
            if target.read_bytes() != changed:
                raise OSError("post-write verification failed: " + str(target))
            print("PATCHED:", target)
            print("BACKUP:", backup)
            print("FULL_FILE:", patched)
        print("FULL_FUNCTIONS:", PACKAGE / "full_functions")
        return 0
    except Exception:
        for target, original, changed, backup, patched in expected:
            if target.read_bytes() in (original, changed):
                target.write_bytes(original)
        raise


def main(command: str) -> int:
    if command == "restore":
        return restore()
    if command == "install":
        return install()
    raise ValueError("specify install or restore")


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1] if len(sys.argv) == 2 else ""))
