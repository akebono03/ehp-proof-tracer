"""Guarded R15R16R2 installer. Preserve the prior R15R16 local state."""
from __future__ import annotations

import argparse
from hashlib import sha256
import json
import os
from pathlib import Path
import subprocess

from .patches import TRANSFORMERS, patch_progress, patch_test
from phase173_r4_r15r16_verified_progress_punctuation.projection_patch import (
    patch_projection, patch_layout,
)

ROOT = Path(__file__).resolve().parents[1]
PACKAGE = Path(__file__).resolve().parent
STATE = PACKAGE / "installed_state.json"
BACKUP = PACKAGE / "backups"
REVIEWED_HEAD = "92f967c079f4a66e19a598e0acc54b742f11df9c"
REVIEWED_BLOBS = {
    "phase173_r4_r15r9_shared_abstract_renderer/projection.py":
        "55eadbd3deb6a7ca54f78d1fe3c470053196840d",
    "phase173_r4_r15r13_unified_presentation/layout.py":
        "05d2b3a0353c0ff1251f65dcd53d902c9ffbb140",
}
PREVIOUS_PATCH_SHA256 = "266b4cb7087e86428c82d048737b2982cf427a21ec10022796d9a300f310cb22"
PREVIOUS_TEST_SHA256 = "c278677439fe17675e36d76b2f4d2cb80150887cedbd9ab437ab0fb8635e07fc"
PROJECTION = "phase173_r4_r15r9_shared_abstract_renderer/projection.py"
LAYOUT = "phase173_r4_r15r13_unified_presentation/layout.py"
PREVIOUS_TEST = "phase173_r4_r15r16_verified_progress_punctuation/tests/test_integration.py"
PREVIOUS_PATCH = "phase173_r4_r15r16_verified_progress_punctuation/projection_patch.py"


def command(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", *args], cwd=ROOT, capture_output=True, text=True,
        encoding="utf-8", errors="replace", check=False,
    )


def git(*args: str) -> str:
    response = command(*args)
    if response.returncode != 0:
        raise RuntimeError("git " + " ".join(args) + ": " + response.stderr.strip()[:400])
    return response.stdout.strip()


def clean_text(source: bytes) -> str:
    return source.decode("utf-8").replace("\r\n", "\n")


def preserve_eol(source: bytes, text: str) -> bytes:
    return (text.replace("\n", "\r\n") if b"\r\n" in source else text).encode("utf-8")


def expected_prior_local(name: str, current: bytes) -> bytes:
    if name == PREVIOUS_TEST:
        if sha256(current).hexdigest() == PREVIOUS_TEST_SHA256:
            return current
        if sha256(clean_text(current).encode("utf-8")).hexdigest() == PREVIOUS_TEST_SHA256:
            return current
        raise RuntimeError("previous R15R16 regression test was edited: " + name)
    committed_bytes = command("show", "HEAD:" + name)
    if committed_bytes.returncode != 0:
        raise RuntimeError("reviewed source is not present on HEAD: " + name)
    # Use git show via a binary subprocess to prevent encoding/newline changes.
    raw = subprocess.run(
        ["git", "show", "HEAD:" + name], cwd=ROOT,
        capture_output=True, check=False,
    )
    if raw.returncode != 0:
        raise RuntimeError("unable to retrieve exact Git blob: " + name)
    previous = patch_projection(clean_text(raw.stdout)) if name == PROJECTION else (
        patch_layout(clean_text(raw.stdout))
    )
    return preserve_eol(current, previous)


def source_guard() -> str:
    branch = git("branch", "--show-current")
    local = git("rev-parse", "HEAD")
    remote = git("rev-parse", "origin/develop")
    if branch != "develop" or local != remote:
        raise RuntimeError("develop branch or local/remote HEAD mismatch")
    if command("merge-base", "--is-ancestor", REVIEWED_HEAD, "HEAD").returncode != 0:
        raise RuntimeError("HEAD is not descended from reviewed R15R15")
    if git("diff", "--cached", "--name-only"):
        raise RuntimeError("staged edits require review")
    for name, expected in REVIEWED_BLOBS.items():
        if git("rev-parse", "HEAD:" + name) != expected:
            raise RuntimeError("reviewed GitHub code changed: " + name)
    changed = set(filter(None, git("diff", "--name-only").splitlines()))
    allowed = {PROJECTION, LAYOUT}
    if not changed.issubset(allowed):
        raise RuntimeError("unexpected local changes: " + ", ".join(sorted(changed - allowed)))
    if not (ROOT / PREVIOUS_PATCH).is_file() or (
        sha256((ROOT / PREVIOUS_PATCH).read_bytes()).hexdigest()
        != PREVIOUS_PATCH_SHA256
    ):
        raise RuntimeError("R15R16 prior patch file is missing or changed")
    for name in (PROJECTION, LAYOUT, PREVIOUS_TEST):
        path = ROOT / name
        if not path.is_file():
            raise RuntimeError("reviewed R15R16 source missing: " + name)
        if STATE.exists() and name in TRANSFORMERS:
            continue
        expected = expected_prior_local(name, path.read_bytes())
        if path.read_bytes() != expected:
            raise RuntimeError("R15R16 previous patch not applied as reviewed: " + name)
    print("R15R16R2_BRANCH=" + branch, flush=True)
    print("R15R16R2_LOCAL_HEAD=" + local, flush=True)
    print("R15R16R2_REMOTE_HEAD=" + remote, flush=True)
    print("R15R16R2_REVIEWED_ANCESTOR=" + REVIEWED_HEAD, flush=True)
    print("R15R16R2_SOURCE_GUARD=PASS", flush=True)
    return local


def read_backup(state: dict, name: str) -> bytes:
    entry = state["files"][name]
    original = (BACKUP / entry["backup"]).read_bytes()
    if sha256(original).hexdigest() != entry["original_sha256"]:
        raise RuntimeError("R15R16R2 backup checksum mismatch: " + name)
    return original


def preflight() -> tuple[dict[str, bytes], dict[str, bytes], str]:
    head = source_guard()
    installed = STATE.is_file()
    if BACKUP.exists() and not installed:
        raise RuntimeError("orphan backup directory requires inspection")
    state = json.loads(STATE.read_text(encoding="utf-8")) if installed else None
    if state is not None and state["head"] != head:
        raise RuntimeError("HEAD changed after R15R16R2 installation")
    originals: dict[str, bytes] = {}
    projected: dict[str, bytes] = {}
    for name, transform in TRANSFORMERS.items():
        current = (ROOT / name).read_bytes()
        original = read_backup(state, name) if state is not None else current
        target_text = transform(clean_text(original))
        compile(target_text, name, "exec")
        target = preserve_eol(original, target_text)
        if state is not None:
            if sha256(target).hexdigest() != state["files"][name]["target_sha256"]:
                raise RuntimeError("R15R16R2 projected source hash mismatch")
            if current != target:
                raise RuntimeError("R15R16R2 source was subsequently edited: " + name)
        originals[name], projected[name] = original, target
    return originals, projected, head


def install() -> None:
    originals, targets, head = preflight()
    if STATE.exists():
        print("R15R16R2_ALREADY_INSTALLED=True", flush=True)
        return
    BACKUP.mkdir(exist_ok=False)
    state: dict = {"head": head, "files": {}}
    try:
        for index, (name, original) in enumerate(originals.items()):
            backup_name = f"original_{index}.backup"
            (BACKUP / backup_name).write_bytes(original)
            state["files"][name] = {
                "backup": backup_name,
                "original_sha256": sha256(original).hexdigest(),
                "target_sha256": sha256(targets[name]).hexdigest(),
            }
        STATE.write_text(json.dumps(state, indent=2) + "\n", encoding="utf-8")
        for name, target in targets.items():
            destination = ROOT / name
            temporary = destination.with_name(destination.name + ".r15r16r2.tmp")
            temporary.write_bytes(target)
            os.replace(temporary, destination)
    except BaseException:
        if STATE.exists():
            restore()
        else:
            for path in BACKUP.iterdir():
                path.unlink()
            BACKUP.rmdir()
        raise
    print("R15R16R2_INSTALLED=True", flush=True)
    print("R15R16R2_FULL_PYTEST_RUN=False", flush=True)


def restore() -> None:
    if not STATE.exists():
        raise RuntimeError("R15R16R2 installation state is absent")
    state = json.loads(STATE.read_text(encoding="utf-8"))
    if git("rev-parse", "HEAD") != state["head"]:
        raise RuntimeError("HEAD changed; refusing to overwrite local edits")
    originals = {}
    for name, entry in state["files"].items():
        original = read_backup(state, name)
        current = (ROOT / name).read_bytes()
        if sha256(current).hexdigest() not in (
            entry["target_sha256"], entry["original_sha256"],
        ):
            raise RuntimeError("post-install user edit detected: " + name)
        originals[name] = original
    for name, original in originals.items():
        (ROOT / name).write_bytes(original)
    STATE.unlink()
    for entry in state["files"].values():
        (BACKUP / entry["backup"]).unlink()
    BACKUP.rmdir()
    print("R15R16R2_RESTORED=True", flush=True)
    print("R15R16R2_RESTORED_TO_R15R16=True", flush=True)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    switches = parser.add_mutually_exclusive_group(required=True)
    switches.add_argument("--dry-run", action="store_true")
    switches.add_argument("--install", action="store_true")
    switches.add_argument("--restore", action="store_true")
    args = parser.parse_args()
    try:
        if args.restore:
            restore()
        elif args.install:
            install()
        else:
            preflight()
            print("R15R16R2_DRY_RUN=PASS", flush=True)
            print("R15R16R2_PRODUCTION_EDIT=NONE", flush=True)
        return 0
    except (RuntimeError, TypeError, ValueError, OSError, UnicodeError,
            KeyError, SyntaxError) as exc:
        print("R15R16R2_ERROR=" + type(exc).__name__ + ": " + str(exc), flush=True)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
