"""Source-guarded installation of the Phase 173 R15R16 presentation patch."""
from __future__ import annotations

import argparse
from hashlib import sha256
import json
import os
from pathlib import Path
import subprocess

from .projection_patch import TRANSFORMERS

ROOT = Path(__file__).resolve().parents[1]
PACKAGE = Path(__file__).resolve().parent
BACKUP = PACKAGE / "backups"
STATE = PACKAGE / "installed_state.json"
REVIEWED_HEAD = "92f967c079f4a66e19a598e0acc54b742f11df9c"
REVIEWED_BLOBS = {
    "phase173_r4_r15r9_shared_abstract_renderer/projection.py":
        "55eadbd3deb6a7ca54f78d1fe3c470053196840d",
    "phase173_r4_r15r13_unified_presentation/layout.py":
        "05d2b3a0353c0ff1251f65dcd53d902c9ffbb140",
}


def _command(*arguments: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", *arguments], cwd=ROOT, capture_output=True,
        text=True, encoding="utf-8", errors="replace", check=False,
    )


def _git(*arguments: str) -> str:
    completed = _command(*arguments)
    if completed.returncode != 0:
        raise RuntimeError("git command failed: " + " ".join(arguments)
                           + ": " + completed.stderr.strip()[:400])
    return completed.stdout.strip()


def _guard() -> str:
    branch = _git("branch", "--show-current")
    head = _git("rev-parse", "HEAD")
    remote = _git("rev-parse", "origin/develop")
    if branch != "develop" or head != remote:
        raise RuntimeError("develop local/remote HEAD mismatch")
    ancestry = _command("merge-base", "--is-ancestor", REVIEWED_HEAD, "HEAD")
    if ancestry.returncode != 0:
        raise RuntimeError("current HEAD is not descended from reviewed R15R15")
    if _git("diff", "--cached", "--name-only"):
        raise RuntimeError("staged changes require inspection")
    for name, expected in REVIEWED_BLOBS.items():
        if _git("rev-parse", "HEAD:" + name) != expected:
            raise RuntimeError("reviewed GitHub source blob changed: " + name)
        if not (ROOT / name).is_file():
            raise RuntimeError("reviewed source file missing: " + name)
    local_changes = set(filter(None, _git("diff", "--name-only").splitlines()))
    unexpected = local_changes.difference(TRANSFORMERS)
    if unexpected:
        raise RuntimeError("unreviewed tracked changes: " + ", ".join(sorted(unexpected)))
    print("R15R16_BRANCH=" + branch, flush=True)
    print("R15R16_LOCAL_HEAD=" + head, flush=True)
    print("R15R16_REMOTE_HEAD=" + remote, flush=True)
    print("R15R16_REVIEWED_ANCESTOR=" + REVIEWED_HEAD, flush=True)
    print("R15R16_SOURCE_GUARD=PASS", flush=True)
    return head


def _target_bytes(original: bytes, name: str) -> bytes:
    normalized = original.decode("utf-8").replace("\r\n", "\n")
    transformed = TRANSFORMERS[name](normalized)
    compile(transformed, name, "exec")
    if b"\r\n" in original:
        transformed = transformed.replace("\n", "\r\n")
    return transformed.encode("utf-8")


def _read_previous(state: dict, name: str) -> bytes:
    entry = state["files"][name]
    previous = (BACKUP / entry["backup"]).read_bytes()
    if sha256(previous).hexdigest() != entry["original_sha256"]:
        raise RuntimeError("backup checksum mismatch: " + name)
    return previous


def _preflight() -> tuple[dict[str, bytes], dict[str, bytes], str]:
    head = _guard()
    installed = STATE.is_file()
    if BACKUP.exists() and not installed:
        raise RuntimeError("orphan R15R16 backups require inspection")
    state = json.loads(STATE.read_text(encoding="utf-8")) if installed else None
    if state is not None and state["head"] != head:
        raise RuntimeError("HEAD changed after installation: inspect before proceeding")
    original: dict[str, bytes] = {}
    expected: dict[str, bytes] = {}
    for name in TRANSFORMERS:
        current = (ROOT / name).read_bytes()
        previous = _read_previous(state, name) if state is not None else current
        result = _target_bytes(previous, name)
        if state is not None:
            if sha256(result).hexdigest() != state["files"][name]["target_sha256"]:
                raise RuntimeError("patched content changed: " + name)
            if current != result:
                raise RuntimeError("installed file locally altered: " + name)
        else:
            changed = _git("diff", "--", name)
            if changed:
                raise RuntimeError("file locally altered: " + name)
        original[name] = previous
        expected[name] = result
    return original, expected, head


def dry_run() -> None:
    _preflight()
    print("R15R16_DRY_RUN=PASS", flush=True)
    print("R15R16_PRODUCTION_EDIT=NONE", flush=True)


def install() -> None:
    original, target, head = _preflight()
    if STATE.exists():
        print("R15R16_ALREADY_INSTALLED=True", flush=True)
        return
    BACKUP.mkdir(exist_ok=False)
    state = {"head": head, "files": {}}
    try:
        for index, (name, data) in enumerate(original.items()):
            filename = f"source_{index}.backup"
            (BACKUP / filename).write_bytes(data)
            state["files"][name] = {
                "backup": filename,
                "original_sha256": sha256(data).hexdigest(),
                "target_sha256": sha256(target[name]).hexdigest(),
            }
        STATE.write_text(json.dumps(state, indent=2) + "\n", encoding="utf-8")
        for name, data in target.items():
            location = ROOT / name
            temporary = location.with_name(location.name + ".r15r16.tmp")
            temporary.write_bytes(data)
            os.replace(temporary, location)
    except BaseException:
        if STATE.exists():
            restore()
        else:
            for path in BACKUP.iterdir():
                path.unlink()
            BACKUP.rmdir()
        raise
    print("R15R16_INSTALLED=True", flush=True)
    print("R15R16_FULL_PYTEST_RUN=False", flush=True)


def restore() -> None:
    if not STATE.is_file():
        raise RuntimeError("installation state missing")
    state = json.loads(STATE.read_text(encoding="utf-8"))
    if _git("rev-parse", "HEAD") != state["head"]:
        raise RuntimeError("HEAD changed after installation; restore refused")
    original = {}
    for name, entry in state["files"].items():
        previous = _read_previous(state, name)
        current_hash = sha256((ROOT / name).read_bytes()).hexdigest()
        if current_hash not in (entry["original_sha256"], entry["target_sha256"]):
            raise RuntimeError("unexpected post-install local change: " + name)
        original[name] = previous
    for name, data in original.items():
        (ROOT / name).write_bytes(data)
    STATE.unlink()
    for entry in state["files"].values():
        (BACKUP / entry["backup"]).unlink()
    BACKUP.rmdir()
    print("R15R16_RESTORED=True", flush=True)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--dry-run", action="store_true")
    group.add_argument("--install", action="store_true")
    group.add_argument("--restore", action="store_true")
    args = parser.parse_args()
    try:
        if args.restore:
            restore()
        elif args.install:
            install()
        else:
            dry_run()
        return 0
    except (RuntimeError, TypeError, ValueError, OSError, UnicodeError,
            KeyError, SyntaxError) as exc:
        print("R15R16_ERROR=" + type(exc).__name__ + ": " + str(exc), flush=True)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
