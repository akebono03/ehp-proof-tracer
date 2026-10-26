"""Guarded Phase 169 R3E replacement of one complete function in one production module."""
from __future__ import annotations

import ast
import hashlib
import subprocess
import sys
from pathlib import Path

PACKAGE = Path(__file__).resolve().parent
ROOT = PACKAGE.parent
RELATIVE = Path("phase165_r52_r9_shared_math.py")
TARGET = ROOT / RELATIVE
REPLACEMENT = PACKAGE / "full_functions" / "shared_expansion_provider.py"
BACKUP = PACKAGE / "output" / "phase165_r52_r9_shared_math.py.before"
FULL_FILE = PACKAGE / "output" / "phase165_r52_r9_shared_math.py.full.py"
EXPECTED_GIT_BLOB = "36a4c355758ee55ba4d39606a8e0f281bb43efff"
MARKER = "from phase165_r14_r5_ehp_connection import expand_registered_ehp_goal"


def _git(*args: str) -> str:
    result = subprocess.run(
        ("git",) + args, cwd=ROOT, capture_output=True,
        encoding="utf-8", errors="replace", text=True,
    )
    if result.returncode != 0:
        raise RuntimeError("git failed: " + result.stderr.strip())
    return result.stdout.strip()


def _replacement_text() -> str:
    replacement = REPLACEMENT.read_text(encoding="utf-8")
    parsed = ast.parse(replacement)
    if len(parsed.body) != 1 or not isinstance(parsed.body[0], ast.FunctionDef):
        raise ValueError("replacement must contain one complete function")
    if parsed.body[0].name != "shared_expansion_provider":
        raise ValueError("unexpected function name")
    if replacement.count(MARKER) != 1:
        raise ValueError("EHP provider must be connected once")
    return replacement


def _replace_function(original: str, replacement: str) -> str:
    lines = original.splitlines(keepends=True)
    tree = ast.parse(original)
    matches = [node for node in tree.body
               if isinstance(node, ast.FunctionDef) and node.name == "shared_expansion_provider"]
    if len(matches) != 1:
        raise ValueError("expected exactly one production provider function")
    node = matches[0]
    new_lines = replacement.splitlines(keepends=True)
    return "".join(lines[:node.lineno - 1] + new_lines + lines[node.end_lineno:])


def _decode(raw: bytes) -> tuple[str, bytes, str]:
    bom = b"\xef\xbb\xbf" if raw.startswith(b"\xef\xbb\xbf") else b""
    text = raw[len(bom):].decode("utf-8")
    newline = "\r\n" if "\r\n" in text else "\n"
    return text.replace("\r\n", "\n"), bom, newline


def _encode(text: str, bom: bytes, newline: str) -> bytes:
    return bom + text.replace("\n", newline).encode("utf-8")


def _write(path: Path, contents: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(contents)


def main(command: str) -> int:
    replacement = _replacement_text()
    if not TARGET.is_file():
        print("REFUSED: production module missing")
        return 2
    current = TARGET.read_bytes()
    normalized, bom, newline = _decode(current)
    if command == "restore":
        if not BACKUP.exists() or not FULL_FILE.exists():
            print("REFUSED: no registered patch-and-backup pair")
            return 3
        if current != FULL_FILE.read_bytes():
            print("REFUSED: production has changed since R3E patch")
            return 4
        TARGET.write_bytes(BACKUP.read_bytes())
        print("RESTORED:", TARGET)
        return 0
    if command != "install":
        raise ValueError("expected install or restore")
    if MARKER in normalized:
        if FULL_FILE.exists() and current == FULL_FILE.read_bytes():
            print("ALREADY_APPLIED:", TARGET)
            return 0
        print("REFUSED: EHP provider already present but not this exact patch")
        return 5
    blob = _git("rev-parse", "HEAD:" + str(RELATIVE).replace("\\", "/"))
    if blob != EXPECTED_GIT_BLOB:
        print("REFUSED: reviewed GitHub source differs from the local HEAD")
        print("EXPECTED_GIT_BLOB=" + EXPECTED_GIT_BLOB)
        print("ACTUAL_GIT_BLOB=" + blob)
        return 6
    dirty = subprocess.run(
        ("git", "diff", "--quiet", "--", str(RELATIVE)), cwd=ROOT,
    )
    if dirty.returncode != 0:
        print("REFUSED: production file has uncommitted changes")
        return 7
    changed = _replace_function(normalized, replacement)
    ast.parse(changed, filename=str(TARGET))
    updated = _encode(changed, bom, newline)
    if BACKUP.exists() and BACKUP.read_bytes() != current:
        print("REFUSED: pre-existing backup does not match current source")
        return 8
    _write(BACKUP, current)
    _write(FULL_FILE, updated)
    TARGET.write_bytes(updated)
    if TARGET.read_bytes() != updated:
        TARGET.write_bytes(current)
        print("FAILED: verification failed, original source restored")
        return 9
    print("PATCHED:", TARGET)
    print("BACKUP:", BACKUP)
    print("FULL_FILE:", FULL_FILE)
    print("FULL_FUNCTION:", REPLACEMENT)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1] if len(sys.argv) == 2 else ""))
