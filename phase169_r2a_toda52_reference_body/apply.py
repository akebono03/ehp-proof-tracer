"""Guarded, single-file installation of the Phase 169 R2A Reference body."""
from __future__ import annotations

import argparse
from pathlib import Path
import sys


PACKAGE = Path(__file__).resolve().parent
ROOT = PACKAGE.parent
TARGET = ROOT / "phase168_r3_37c_reference_projection.py"
BEFORE = PACKAGE / "baseline" / TARGET.name
AFTER = PACKAGE / "full_files" / TARGET.name
OUTPUT = PACKAGE / "output"
BACKUP = OUTPUT / "phase168_r3_37c_reference_projection.py.before"


def normalize(raw: bytes) -> str:
    return raw.decode("utf-8-sig").replace("\r\n", "\n")


def install() -> int:
    if not TARGET.is_file():
        raise FileNotFoundError(f"Missing expected repository file: {TARGET}")
    before = normalize(BEFORE.read_bytes())
    after = normalize(AFTER.read_bytes())
    original_raw = TARGET.read_bytes()
    current = normalize(original_raw)
    if current == after:
        print("ALREADY_APPLIED:", TARGET)
        return 0
    if current != before:
        raise RuntimeError(
            "Source does not match the inspected develop version; no patch was applied. "
            "Inspect the local source before deciding on a new patch."
        )
    import ast
    ast.parse(after, filename=str(TARGET))
    OUTPUT.mkdir(parents=True, exist_ok=True)
    if BACKUP.exists():
        if normalize(BACKUP.read_bytes()) != before:
            raise RuntimeError("An incompatible backup exists; refusing to overwrite it")
    else:
        BACKUP.write_bytes(original_raw)
    newline = "\r\n" if b"\r\n" in original_raw else "\n"
    bom = b"\xef\xbb\xbf" if original_raw.startswith(b"\xef\xbb\xbf") else b""
    TARGET.write_bytes(bom + after.replace("\n", newline).encode("utf-8"))
    print("PATCHED:", TARGET)
    print("BACKUP:", BACKUP)
    print("FULL_FILE:", AFTER)
    print("FULL_FUNCTION:", PACKAGE / "full_functions" / "project_reference_bodies.py")
    return 0


def restore() -> int:
    if not BACKUP.is_file():
        raise FileNotFoundError("No Phase 169 R2A backup is available")
    current = normalize(TARGET.read_bytes())
    before = normalize(BEFORE.read_bytes())
    after = normalize(AFTER.read_bytes())
    if current == before:
        print("ALREADY_RESTORED:", TARGET)
        return 0
    if current != after:
        raise RuntimeError("Source changed after installation; restore refused")
    TARGET.write_bytes(BACKUP.read_bytes())
    print("RESTORED:", TARGET)
    return 0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("action", choices=("install", "restore"))
    args = parser.parse_args()
    if args.action == "install":
        return install()
    return restore()


if __name__ == "__main__":
    try:
        sys.exit(main())
    except (RuntimeError, OSError, SyntaxError, UnicodeError) as exc:
        print(f"R2A INSTALL ERROR: {exc}", file=sys.stderr)
        sys.exit(1)
