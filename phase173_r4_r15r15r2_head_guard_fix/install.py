"""Safely install or restore a reviewed, presentation-only R15R15 patch.

R15R14 is committed at the reviewed baseline. Newer develop commits are
allowed only while the exact four reviewed Git blobs remain unchanged.
"""
from __future__ import annotations

import argparse
from hashlib import sha256
import json
import os
from pathlib import Path
import subprocess

from .patches import TRANSFORMERS

ROOT = Path(__file__).resolve().parents[1]
PACKAGE = Path(__file__).resolve().parent
BACKUP = PACKAGE / "backups"
STATE = PACKAGE / "installed_state.json"
REVIEWED_HEAD = "5563a67008d097d08745481ee299dbb94e12c2b9"
REVIEWED_BLOBS = {
    "web_group_proof_common.py": "52ef8170874c714d4aa4bf4f8b525a7f9953154b",
    "phase165_r52_r3_web_adapter.py": "211fdb73342019cee4503c01e549c118e286125a",
    "templates/index.html": "d84b9eed4c8d070c4ed98c5ed31fd9241987a42e",
    "phase173_r4_r15r13_unified_presentation/layout.py":
        "05d2b3a0353c0ff1251f65dcd53d902c9ffbb140",
}


def command(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", *args], cwd=ROOT, text=True, capture_output=True,
        encoding="utf-8", errors="replace", check=False,
    )


def git(*args: str) -> str:
    result = command(*args)
    if result.returncode != 0:
        raise RuntimeError(
            "git " + " ".join(args) + ": " + result.stderr.strip()[:400]
        )
    return result.stdout.strip()


def normalized(original: bytes) -> str:
    return original.decode("utf-8").replace("\r\n", "\n")


def preserved_newlines(original: bytes, source: str) -> bytes:
    if b"\r\n" in original:
        return source.replace("\n", "\r\n").encode("utf-8")
    return source.encode("utf-8")


def source_guard(*, installed: bool) -> str:
    branch = git("branch", "--show-current")
    head = git("rev-parse", "HEAD")
    remote = git("rev-parse", "origin/develop")
    if branch != "develop" or head != remote:
        raise RuntimeError(
            f"develop local/remote mismatch: branch={branch} local={head} remote={remote}"
        )
    lineage = command("merge-base", "--is-ancestor", REVIEWED_HEAD, "HEAD")
    if lineage.returncode != 0:
        raise RuntimeError("HEAD is not a descendant of the reviewed R15R14 commit")
    if git("diff", "--cached", "--name-only"):
        raise RuntimeError("staged changes require review")
    for path, blob in REVIEWED_BLOBS.items():
        if git("rev-parse", f"HEAD:{path}") != blob:
            raise RuntimeError("reviewed content changed on GitHub: " + path)
        if not (ROOT / path).is_file():
            raise RuntimeError("missing reviewed file: " + path)
    changed = set(filter(None, git("diff", "--name-only").splitlines()))
    allowed = set(TRANSFORMERS) if installed else set()
    if not changed.issubset(allowed):
        raise RuntimeError(
            "unreviewed tracked local changes: " + ", ".join(sorted(changed - allowed))
        )
    print("R15R15R2_BRANCH=" + branch, flush=True)
    print("R15R15R2_LOCAL_HEAD=" + head, flush=True)
    print("R15R15R2_REMOTE_HEAD=" + remote, flush=True)
    print("R15R15R2_REVIEWED_ANCESTOR=" + REVIEWED_HEAD, flush=True)
    print("R15R15R2_SOURCE_GUARD_FILES=" + str(len(REVIEWED_BLOBS)), flush=True)
    print("R15R15R2_SOURCE_GUARD=PASS", flush=True)
    return head


def project(before: bytes, path: str) -> bytes:
    return preserved_newlines(before, TRANSFORMERS[path](normalized(before)))


def read_backup(state: dict, path: str) -> bytes:
    entry = state["files"][path]
    previous = (BACKUP / entry["backup"]).read_bytes()
    if sha256(previous).hexdigest() != entry["original_sha256"]:
        raise RuntimeError("backup integrity failure: " + path)
    return previous


def preflight(*, installed_allowed: bool = False) -> tuple[dict[str, bytes], dict[str, bytes], str]:
    installed = STATE.is_file()
    if installed and not installed_allowed:
        raise RuntimeError("already installed; inspect installation state")
    if not installed and BACKUP.exists():
        raise RuntimeError("orphan backup directory requires inspection")
    head = source_guard(installed=installed)
    state = json.loads(STATE.read_text(encoding="utf-8")) if installed else None
    if state is not None and head != state["head"]:
        raise RuntimeError("HEAD changed after R15R15 install; inspect before proceeding")
    originals: dict[str, bytes] = {}
    targets: dict[str, bytes] = {}
    for path in TRANSFORMERS:
        current = (ROOT / path).read_bytes()
        original = read_backup(state, path) if state is not None else current
        target = project(original, path)
        if state is not None:
            entry = state["files"][path]
            if sha256(target).hexdigest() != entry["target_sha256"]:
                raise RuntimeError("expected patch changed: " + path)
            if current != target:
                raise RuntimeError("installed content has changed: " + path)
        else:
            if current != original:
                raise RuntimeError("local source changed: " + path)
        originals[path] = original
        targets[path] = target
    return originals, targets, head


def install() -> None:
    originals, targets, head = preflight(installed_allowed=True)
    if STATE.exists():
        print("R15R15R2_ALREADY_INSTALLED=True", flush=True)
        return
    BACKUP.mkdir(exist_ok=False)
    state: dict[str, object] = {"head": head, "files": {}}
    try:
        for i, (path, original) in enumerate(originals.items()):
            name = f"source_{i}.backup"
            (BACKUP / name).write_bytes(original)
            state["files"][path] = {
                "backup": name,
                "original_sha256": sha256(original).hexdigest(),
                "target_sha256": sha256(targets[path]).hexdigest(),
            }
        STATE.write_text(json.dumps(state, indent=2) + "\n", encoding="utf-8")
        for path, target in targets.items():
            location = ROOT / path
            temporary = location.with_name(location.name + ".r15r15r2.tmp")
            temporary.write_bytes(target)
            os.replace(temporary, location)
    except BaseException:
        if STATE.exists():
            restore()
        else:
            for backup in BACKUP.iterdir():
                backup.unlink()
            BACKUP.rmdir()
        raise
    print("R15R15R2_INSTALLED=True", flush=True)
    print("R15R15R2_FULL_PYTEST_RUN=False", flush=True)


def restore() -> None:
    if not STATE.is_file():
        raise RuntimeError("no R15R15R2 installation state")
    state = json.loads(STATE.read_text(encoding="utf-8"))
    if git("rev-parse", "HEAD") != state["head"]:
        raise RuntimeError("HEAD changed after patch; refusal to overwrite")
    files: dict = state["files"]
    originals: dict[str, bytes] = {}
    for path, entry in files.items():
        previous = read_backup(state, path)
        current = (ROOT / path).read_bytes()
        if sha256(current).hexdigest() not in (
            entry["original_sha256"], entry["target_sha256"]
        ):
            raise RuntimeError("local edit after install: " + path)
        originals[path] = previous
    for path, previous in originals.items():
        (ROOT / path).write_bytes(previous)
    STATE.unlink()
    for entry in files.values():
        (BACKUP / entry["backup"]).unlink()
    BACKUP.rmdir()
    print("R15R15R2_RESTORED=True", flush=True)
    print("R15R15R2_RESTORED_TO_COMMITTED_R15R14=True", flush=True)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    options = parser.add_mutually_exclusive_group(required=True)
    options.add_argument("--dry-run", action="store_true")
    options.add_argument("--install", action="store_true")
    options.add_argument("--restore", action="store_true")
    args = parser.parse_args()
    try:
        if args.restore:
            restore()
        elif args.install:
            install()
        else:
            preflight(installed_allowed=True)
            print("R15R15R2_DRY_RUN=PASS", flush=True)
            print("R15R15R2_PRODUCTION_EDIT=NONE", flush=True)
        return 0
    except (RuntimeError, TypeError, ValueError, OSError, UnicodeError, KeyError) as exc:
        print("R15R15R2_ERROR=" + type(exc).__name__ + ": " + str(exc), flush=True)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
