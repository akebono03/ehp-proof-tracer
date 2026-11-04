"""Apply or restore the R15R15 Web status banner with strict source guards."""
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
REVIEWED_HEAD = "9729d3ee51e93f26cf6b31a3880cb1a92a552f2c"
REVIEWED_BLOBS = {
    "web_group_proof_common.py": "045d2ae677c0e62c243270e760c786ce61224c59",
    "phase165_r52_r3_web_adapter.py": "211fdb73342019cee4503c01e549c118e286125a",
    "templates/index.html": "d84b9eed4c8d070c4ed98c5ed31fd9241987a42e",
    "phase173_r4_r15r13_unified_presentation/layout.py": "809effb7fcb70361e5580d9716d4aa143685f275",
}
RETAINED_R15R14_PATHS = {
    "web_group_proof_common.py",
    "phase173_r4_r15r13_unified_presentation/layout.py",
}


def git(*args: str) -> str:
    command = subprocess.run(
        ["git", *args], cwd=ROOT, text=True,
        stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        encoding="utf-8", errors="replace", check=False,
    )
    if command.returncode != 0:
        raise RuntimeError(f"git {' '.join(args)}: {command.stderr.strip()[:400]}")
    return command.stdout.strip()


def normalized(raw: bytes) -> str:
    return raw.decode("utf-8").replace("\r\n", "\n")


def preserved_newlines(original: bytes, text: str) -> bytes:
    if b"\r\n" in original:
        return text.replace("\n", "\r\n").encode("utf-8")
    return text.encode("utf-8")


def baseline_for(path: str) -> str:
    return git("show", f"HEAD:{path}").replace("\r\n", "\n") + "\n"


def _expected_r15r14() -> tuple[str, str]:
    # The user installed R15R14 but has not committed that separate change.
    # Reuse its reviewed transform and compare the *whole* local source.
    from phase173_r4_r15r14_common_partial_presentation.patches import (
        patch_common, patch_layout,
    )
    return (
        patch_common(baseline_for("web_group_proof_common.py")),
        patch_layout(baseline_for("phase173_r4_r15r13_unified_presentation/layout.py")),
    )


def preflight(*, installed_allowed: bool = False) -> tuple[dict[str, bytes], dict[str, bytes]]:
    branch = git("branch", "--show-current")
    head = git("rev-parse", "HEAD")
    remote = git("rev-parse", "origin/develop")
    if branch != "develop" or head != REVIEWED_HEAD or remote != REVIEWED_HEAD:
        raise RuntimeError(f"source HEAD/branch guard mismatch: {branch} local={head} remote={remote}")
    if git("diff", "--cached", "--name-only"):
        raise RuntimeError("staged changes require review")
    for path, expected_blob in REVIEWED_BLOBS.items():
        if git("rev-parse", f"HEAD:{path}") != expected_blob:
            raise RuntimeError("reviewed Git blob mismatch: " + path)
    expected_common, expected_layout = _expected_r15r14()
    layout_path = "phase173_r4_r15r13_unified_presentation/layout.py"
    if normalized((ROOT / layout_path).read_bytes()) != expected_layout:
        raise RuntimeError("R15R14 local layout has changed since review")
    expected_sources = {
        "web_group_proof_common.py": expected_common,
        "phase165_r52_r3_web_adapter.py": baseline_for("phase165_r52_r3_web_adapter.py"),
        "templates/index.html": baseline_for("templates/index.html"),
    }
    originals = {}
    modified = {}
    for path, expected in expected_sources.items():
        original = (ROOT / path).read_bytes()
        before = normalized(original)
        if before != expected:
            if not installed_allowed or before != TRANSFORMERS[path](expected):
                raise RuntimeError("unreviewed source content: " + path)
        originals[path] = original
        modified[path] = preserved_newlines(original, TRANSFORMERS[path](expected))
    changed = set(git("diff", "--name-only").splitlines())
    allowed = RETAINED_R15R14_PATHS | (set(TRANSFORMERS) if installed_allowed else set())
    if not changed.issubset(allowed):
        raise RuntimeError("unexpected tracked edits: " + ", ".join(sorted(changed - allowed)))
    print("R15R15_BRANCH=" + branch, flush=True)
    print("R15R15_LOCAL_HEAD=" + head, flush=True)
    print("R15R15_REMOTE_HEAD=" + remote, flush=True)
    print("R15R15_SOURCE_GUARD=PASS", flush=True)
    print("R15R15_R15R14_LOCAL_CHANGES_PRESERVED=True", flush=True)
    return originals, modified


def install() -> None:
    if STATE.exists():
        original, target = preflight(installed_allowed=True)
        if all(original[k] == target[k] for k in target):
            print("R15R15_ALREADY_INSTALLED=True", flush=True)
            return
        raise RuntimeError("install state exists but source content differs")
    originals, targets = preflight()
    BACKUP.mkdir(exist_ok=True)
    hashes = {}
    for i, (path, original) in enumerate(originals.items()):
        label = f"source_{i}.backup"
        destination = BACKUP / label
        if destination.exists():
            raise RuntimeError("pre-existing backup requires inspection: " + label)
        destination.write_bytes(original)
        hashes[path] = {"backup": label, "sha256": sha256(original).hexdigest(),
                        "target_sha256": sha256(targets[path]).hexdigest()}
    STATE.write_text(json.dumps({"head": REVIEWED_HEAD, "files": hashes}, indent=2) + "\n", encoding="utf-8")
    try:
        for path, target in targets.items():
            location = ROOT / path
            temporary = location.with_name(location.name + ".r15r15.tmp")
            temporary.write_bytes(target)
            os.replace(temporary, location)
    except BaseException:
        restore()
        raise
    print("R15R15_INSTALLED=True", flush=True)


def restore() -> None:
    if not STATE.exists():
        raise RuntimeError("no R15R15 installation state to restore")
    data = json.loads(STATE.read_text(encoding="utf-8"))
    if data["head"] != REVIEWED_HEAD:
        raise RuntimeError("installation state head changed")
    for path, saved in data["files"].items():
        previous = (BACKUP / saved["backup"]).read_bytes()
        current = (ROOT / path).read_bytes()
        if sha256(previous).hexdigest() != saved["sha256"]:
            raise RuntimeError("corrupt backup: " + path)
        if sha256(current).hexdigest() not in (saved["sha256"], saved["target_sha256"]):
            raise RuntimeError("edited installed file requires inspection: " + path)
    for path, saved in data["files"].items():
        (ROOT / path).write_bytes((BACKUP / saved["backup"]).read_bytes())
    STATE.unlink()
    for saved in data["files"].values():
        (BACKUP / saved["backup"]).unlink()
    BACKUP.rmdir()
    print("R15R15_RESTORED=True", flush=True)
    print("R15R15_R15R14_RETAINED=True", flush=True)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--dry-run", action="store_true")
    mode.add_argument("--install", action="store_true")
    mode.add_argument("--restore", action="store_true")
    opts = parser.parse_args()
    try:
        if opts.restore:
            restore()
        elif opts.install:
            install()
        else:
            preflight(installed_allowed=STATE.exists())
            print("R15R15_DRY_RUN=PASS", flush=True)
            print("R15R15_PRODUCTION_EDIT=NONE", flush=True)
        return 0
    except (RuntimeError, ValueError, OSError, UnicodeError, KeyError) as exc:
        print("R15R15_ERROR=" + type(exc).__name__ + ": " + str(exc), flush=True)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
