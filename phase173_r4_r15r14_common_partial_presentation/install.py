"""Guarded apply/rollback. Source files are never downloaded or rewritten blindly."""
from __future__ import annotations

import argparse
from hashlib import sha256
import json
import os
from pathlib import Path
import subprocess
import sys

from .patches import patch_common, patch_layout


REVIEWED_HEAD = "9729d3ee51e93f26cf6b31a3880cb1a92a552f2c"
REVIEWED_BLOBS = {
    "web_group_proof_common.py": "045d2ae677c0e62c243270e760c786ce61224c59",
    "phase173_r4_r15r13_unified_presentation/layout.py":
        "809effb7fcb70361e5580d9716d4aa143685f275",
}
TRANSFORMERS = {
    "web_group_proof_common.py": patch_common,
    "phase173_r4_r15r13_unified_presentation/layout.py": patch_layout,
}
ROOT = Path(__file__).resolve().parents[1]
PACKAGE = Path(__file__).resolve().parent
STATE = PACKAGE / "installed_state.json"
BACKUP = PACKAGE / "backups"


def git(*args: str) -> str:
    process = subprocess.run(
        ("git", *args), cwd=ROOT, text=True, encoding="utf-8",
        errors="replace", capture_output=True, check=False,
    )
    if process.returncode != 0:
        raise RuntimeError("git " + " ".join(args) + ": " + process.stderr[:500])
    return process.stdout.strip()


def original_encoding(data: bytes) -> tuple[str, str]:
    """Reject mixed EOL, preserving exact original newline conventions."""
    if data.startswith(b"\xef\xbb\xbf"):
        raise ValueError("UTF-8 BOM source requires review")
    crlf = data.count(b"\r\n")
    lf = data.count(b"\n")
    if data.count(b"\r") != crlf or (crlf and crlf != lf):
        raise ValueError("Mixed EOL source requires review")
    return data.decode("utf-8"), "\r\n" if crlf else "\n"


def transformed_bytes(path: Path, transformer) -> bytes:
    raw = path.read_bytes()
    decoded, eol = original_encoding(raw)
    normalized = decoded.replace("\r\n", "\n")
    modified = transformer(normalized)
    return modified.replace("\n", eol).encode("utf-8")


def digest(data: bytes) -> str:
    return sha256(data).hexdigest()


def check_checkout() -> None:
    root = Path(git("rev-parse", "--show-toplevel")).resolve()
    if root != ROOT.resolve():
        raise RuntimeError("Repository root does not match package parent")
    branch = git("branch", "--show-current")
    head = git("rev-parse", "HEAD")
    remote = git("rev-parse", "origin/develop")
    print("R15R14_BRANCH=" + branch, flush=True)
    print("R15R14_LOCAL_HEAD=" + head, flush=True)
    print("R15R14_REMOTE_HEAD=" + remote, flush=True)
    if branch != "develop" or head != REVIEWED_HEAD or remote != REVIEWED_HEAD:
        raise RuntimeError("Develop HEAD moved; review changes before installation")
    if git("diff", "--cached", "--name-only"):
        raise RuntimeError("Staged changes require review")


def prepare_changes() -> dict[str, tuple[bytes, bytes]]:
    """Require exact reviewed source Git blobs and a clean tracked tree."""
    if git("status", "--porcelain", "--untracked-files=no"):
        raise RuntimeError("Tracked worktree changes require review")
    changes = {}
    for name, transformer in TRANSFORMERS.items():
        file = ROOT / name
        if not file.is_file():
            raise FileNotFoundError(name)
        reviewed = git("rev-parse", "HEAD:" + name)
        local = git("hash-object", "--path=" + name, "--", name)
        if reviewed != REVIEWED_BLOBS[name] or local != REVIEWED_BLOBS[name]:
            raise RuntimeError("Unreviewed source contents: " + name)
        before = file.read_bytes()
        after = transformed_bytes(file, transformer)
        if after == before:
            raise RuntimeError("Patch did not change: " + name)
        changes[name] = before, after
    return changes


def verify_installed() -> bool:
    if not STATE.is_file():
        return False
    state = json.loads(STATE.read_text(encoding="utf-8"))
    if state.get("reviewed_head") != REVIEWED_HEAD:
        raise RuntimeError("Installed state does not match reviewed HEAD")
    if sorted(state.get("modified", {})) != sorted(TRANSFORMERS):
        raise RuntimeError("Installed state is incomplete")
    for name, hash_value in state["modified"].items():
        if digest((ROOT / name).read_bytes()) != hash_value:
            raise RuntimeError("Previously installed source was changed: " + name)
        if not (BACKUP / name).is_file():
            raise RuntimeError("Missing backup: " + name)
    remaining_changes = set(git("diff", "--name-only").splitlines())
    if remaining_changes != set(TRANSFORMERS):
        raise RuntimeError("Unreviewed worktree modifications after installation")
    print("R15R14_ALREADY_INSTALLED=True", flush=True)
    return True


def apply(changes: dict[str, tuple[bytes, bytes]]) -> None:
    if STATE.exists():
        raise RuntimeError("Existing install state must be reviewed before install")
    for name, (before, after) in changes.items():
        saved = BACKUP / name
        saved.parent.mkdir(parents=True, exist_ok=True)
        saved.write_bytes(before)
    replaced = []
    try:
        for name, (before, after) in changes.items():
            target = ROOT / name
            temporary = target.with_name(target.name + ".r15r14-new")
            temporary.write_bytes(after)
            os.replace(temporary, target)
            replaced.append(name)
        state = {
            "reviewed_head": REVIEWED_HEAD,
            "modified": {name: digest(after) for name, (before, after) in changes.items()},
            "backups": {name: digest(before) for name, (before, after) in changes.items()},
            "proof_search_changed": False,
            "full_pytest_run": False,
        }
        STATE.write_text(json.dumps(state, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    except Exception:
        for name in replaced:
            (ROOT / name).write_bytes((BACKUP / name).read_bytes())
        raise


def restore() -> None:
    check_checkout()
    if not verify_installed():
        raise RuntimeError("No verified install to restore")
    record = json.loads(STATE.read_text(encoding="utf-8"))
    for name, expected in record["backups"].items():
        saved = (BACKUP / name).read_bytes()
        if digest(saved) != expected:
            raise RuntimeError("Backup integrity failure: " + name)
    for name in TRANSFORMERS:
        (ROOT / name).write_bytes((BACKUP / name).read_bytes())
    STATE.unlink()
    print("R15R14_RESTORED=PASS", flush=True)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--dry-run", action="store_true")
    mode.add_argument("--install", action="store_true")
    mode.add_argument("--restore", action="store_true")
    args = parser.parse_args()
    try:
        if args.restore:
            restore()
            return 0
        check_checkout()
        if verify_installed():
            print("R15R14_SOURCE_GUARD=PASS", flush=True)
            print("R15R14_DRY_RUN=PASS" if args.dry_run else "R15R14_INSTALLED=True", flush=True)
            return 0
        changes = prepare_changes()
        print("R15R14_SOURCE_GUARD=PASS", flush=True)
        print("R15R14_SOURCE_GUARD_FILES=" + str(len(changes)), flush=True)
        if args.dry_run:
            print("R15R14_DRY_RUN=PASS", flush=True)
            print("R15R14_PRODUCTION_EDIT=NONE", flush=True)
        else:
            apply(changes)
            print("R15R14_INSTALLED=True", flush=True)
        return 0
    except (OSError, ValueError, TypeError, RuntimeError) as exc:
        print("R15R14_ERROR=" + type(exc).__name__ + ": " + str(exc), file=sys.stderr, flush=True)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
