"""Guarded, reversible installation of one common Web display projection."""
from __future__ import annotations

import argparse
import ast
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parent.parent
PACKAGE = Path(__file__).resolve().parent
TARGET = ROOT / "web_group_proof_common.py"
BACKUP = PACKAGE / "backups" / "web_group_proof_common.py"
REVIEWED_HEAD = "5de68856b4e83a1de008a970f62c79e727c49f7f"
REVIEWED_BLOB = "943e25ff4607bad2f6a7a8284304f4160131765c"


def git(*args: str) -> str:
    done = subprocess.run(
        ["git", *args], cwd=ROOT, capture_output=True, text=True,
        encoding="utf-8", errors="replace", check=False,
    )
    if done.returncode:
        raise RuntimeError("git " + " ".join(args) + ": " + done.stderr[:400])
    return done.stdout.strip()


def make_updated(original: bytes) -> bytes:
    crlf = b"\r\n" in original
    text = original.decode("utf-8")
    if "\r" in text.replace("\r\n", ""):
        raise ValueError("Mixed line endings in reviewed Web file")
    normalized = text.replace("\r\n", "\n")
    marker = "def _build_group_proof_rendered_lines("
    if normalized.count(marker) != 1 or not normalized.endswith("  return tuple(lines)\n"):
        raise ValueError("Web parser source structure has changed")
    replacement = (PACKAGE / "full_web_function.py.txt").read_text(encoding="utf-8")
    ast.parse(replacement)
    revised = normalized[:normalized.index(marker)] + replacement
    ast.parse(revised)
    if revised == normalized:
        raise ValueError("Patch already installed or source unchanged")
    return (revised.replace("\n", "\r\n") if crlf else revised).encode("utf-8")


def preflight() -> bytes:
    if Path(git("rev-parse", "--show-toplevel")).resolve() != ROOT.resolve():
        raise RuntimeError("Wrong repository root")
    if git("branch", "--show-current") != "develop":
        raise RuntimeError("Expected branch develop")
    head = git("rev-parse", "HEAD")
    remote = git("rev-parse", "origin/develop")
    if head != REVIEWED_HEAD or remote != REVIEWED_HEAD:
        raise RuntimeError("Unreviewed HEAD: " + head + " origin=" + remote)
    if git("diff", "--name-only") or git("diff", "--cached", "--name-only"):
        raise RuntimeError("Tracked changes require review before patch")
    if git("rev-parse", "HEAD:web_group_proof_common.py") != REVIEWED_BLOB:
        raise RuntimeError("Committed Web file blob mismatches reviewed code")
    if git("hash-object", "web_group_proof_common.py") != REVIEWED_BLOB:
        raise RuntimeError("Local Web file differs from reviewed original")
    data = TARGET.read_bytes()
    make_updated(data)
    print("R15R13_UNIFIED_LOCAL_HEAD=" + head, flush=True)
    print("R15R13_UNIFIED_REMOTE_HEAD=" + remote, flush=True)
    print("R15R13_UNIFIED_SOURCE_GUARD=PASS", flush=True)
    return data


def main() -> int:
    parser = argparse.ArgumentParser()
    operations = parser.add_mutually_exclusive_group(required=True)
    operations.add_argument("--dry-run", action="store_true")
    operations.add_argument("--install", action="store_true")
    operations.add_argument("--restore", action="store_true")
    args = parser.parse_args()
    if args.restore:
        if not BACKUP.is_file():
            raise RuntimeError("No backup available")
        original = BACKUP.read_bytes()
        # Backup SHA must be exactly the original reviewed file.
        if git("hash-object", str(BACKUP)) != REVIEWED_BLOB:
            raise RuntimeError("Backup blob differs from reviewed original")
        TARGET.write_bytes(original)
        print("R15R13_UNIFIED_RESTORE=PASS", flush=True)
        return 0
    original = preflight()
    modified = make_updated(original)
    if args.dry_run:
        print("R15R13_UNIFIED_DRY_RUN=PASS", flush=True)
        print("R15R13_UNIFIED_PRODUCTION_EDIT=NONE", flush=True)
        return 0
    BACKUP.parent.mkdir(parents=True, exist_ok=True)
    if BACKUP.exists():
        raise RuntimeError("Backup already exists; inspect local state first")
    BACKUP.write_bytes(original)
    try:
        TARGET.write_bytes(modified)
        if TARGET.read_bytes() != modified:
            raise RuntimeError("Edited file verification failed")
        print("R15R13_UNIFIED_INSTALLED=True", flush=True)
    except Exception:
        TARGET.write_bytes(original)
        raise
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (RuntimeError, ValueError, OSError) as err:
        print("R15R13_UNIFIED_ERROR=" + str(err), file=sys.stderr, flush=True)
        raise SystemExit(2)
