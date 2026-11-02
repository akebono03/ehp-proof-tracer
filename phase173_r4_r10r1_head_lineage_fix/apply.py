"""Guarded HEAD-lineage correction for the unchanged Phase 173 R4-R10 core.

Only the reviewed verify.py constant may change. No repository production file
or existing proof rule is modified. Source content and remote branch are pinned.
"""
from __future__ import annotations

import argparse
import hashlib
import os
from pathlib import Path
import subprocess
import tempfile

REVIEWED_HEAD = "924888b257f9fed1e2d34790127b4ff108a7badb"
OLD_HEAD = "7158a7f544cd7c6750ebdf82a3b946caa980ea04"
TARGET = "phase173_r4_r10_general_toda56_core/verify.py"
OLD_SHA256 = "1c36e050bf8a40a393a51aa31366c74a93de5616c1072b8693142cbadc8ed64b"
NEW_SHA256 = "a4476b1f19a2bbabcec57b8bf79b57375f63806a4c0c031136032ffe4312b472"
OLD_LINE = 'REVIEWED_HEAD = "' + OLD_HEAD + '"'
NEW_LINE = 'REVIEWED_HEAD = "' + REVIEWED_HEAD + '"'
UNCHANGED_CORE_FILES = {
    "core.py": "453b13c25a1b92e54ce574469734f547c6a52577b817c7bcd1d5ba2df7718f68",
    "run.ps1": "f41964da0ce6124728bb2cf7607786fd1f14aed1110118a466aa8171c11ecdbd",
    "tests/test_core.py": "3156d405961234d456e548b21afbe5d0d74abb24f3284b5d5e88dd6bf8f9c9e0"
}
SOURCE_BLOBS = {
    "phase173_r4_r1_source_bound_56/rule.py": "e9921f6ae5c575e86ec4b7647133382ec613fb5f",
    "phase173_r4_r7_source_first_rule/rule.py": "5113c88e263c28b748c1543ec57bbcedb3eff5bf",
    "phase173_r4_r7_source_first_rule/source.py": "abdc05c731e5ede1258962705bc577b5307b6f38",
    "phase173_r4_r1_narrative_source_fix/projection.py": "ef81a01df157075bc2a21b91bc4ad5fcd56d2cd1",
    "phase165_r52_r3_web_adapter.py": "cfe2c244567535ffaf1e1c2e3ac27dc539ed3c21",
    "phase165_r52_r9_shared_math.py": "f49b0b7699e29ec1b78d73578dc66a0e33d6e336",
    "phase173_r4_r8_public_connection/route.py": "06a402083a23595861f2856255947e4d26a2cc88",
    "phase169_r10e4_ordered_db_prior/db_prior.py": "ed8c6a1f0f6f130005d42a2edba4ab40991e879b",
    "phase166_r3af_goal_adapter.py": "d85f595c9c8be18a2db760b8a20868b40eb15300",
    "phase165_r55_nk_only_goal.py": "b207b8169590e634229d412324d857ffb3857939"
}


def sha256(data: bytes) -> str:
    """Hash literal bytes, not a normalized or inferred source."""
    return hashlib.sha256(data).hexdigest()


def git(root: Path, *arguments: str) -> str:
    """Read Git state and fail closed on a subprocess error."""
    result = subprocess.run(
        ["git", *arguments], cwd=root, capture_output=True,
        text=True, encoding="utf-8", errors="replace", check=False,
    )
    if result.returncode != 0:
        raise RuntimeError(
            "git " + " ".join(arguments) + " failed: " + result.stderr[:600]
        )
    return result.stdout.strip()


def prepared_replacement(old: bytes, replacement: bytes) -> bytes:
    """Reject any other edit to the full reviewed verify.py source."""
    if sha256(old) != OLD_SHA256:
        raise RuntimeError("Original verify.py changed; refusing overwrite")
    if sha256(replacement) != NEW_SHA256:
        raise RuntimeError("Packaged full verify.py has incorrect checksum")
    old_marker = OLD_LINE.encode("ascii")
    new_marker = NEW_LINE.encode("ascii")
    if old.count(old_marker) != 1 or replacement.count(new_marker) != 1:
        raise RuntimeError("Expected HEAD anchor is absent or ambiguous")
    if old.replace(old_marker, new_marker) != replacement:
        raise RuntimeError("Only the reviewed HEAD constant may differ")
    compile(replacement.decode("utf-8"), TARGET, "exec")
    return replacement


def preflight(root: Path, package: Path) -> tuple[Path, bytes, bytes, bool]:
    """Validate local/remote lineage, unchanged sources, and target file bytes."""
    if Path(git(root, "rev-parse", "--show-toplevel")).resolve() != root.resolve():
        raise RuntimeError("Installer must run at the repository root")
    if git(root, "branch", "--show-current") != "develop":
        raise RuntimeError("Only the reviewed develop branch is supported")
    local = git(root, "rev-parse", "HEAD")
    if local != REVIEWED_HEAD:
        raise RuntimeError("Unreviewed local HEAD: " + local)
    remote_line = git(root, "ls-remote", "--exit-code", "origin", "refs/heads/develop")
    if not remote_line or remote_line.split()[0] != REVIEWED_HEAD:
        raise RuntimeError("GitHub develop HEAD differs from reviewed local HEAD")
    if git(root, "status", "--porcelain", "--untracked-files=no"):
        raise RuntimeError("Tracked changes require review; nothing overwritten")
    for relative, expected in SOURCE_BLOBS.items():
        path = root / relative
        if not path.is_file() or git(root, "hash-object", "--", relative) != expected:
            raise RuntimeError("Reviewed source blob changed: " + relative)
    for relative, expected in UNCHANGED_CORE_FILES.items():
        path = root / "phase173_r4_r10_general_toda56_core" / relative
        if not path.is_file() or sha256(path.read_bytes()) != expected:
            raise RuntimeError("R4-R10 core content changed: " + relative)
    target = root / TARGET
    replacement_path = package / "replacement_verify.py.txt"
    if not target.is_file() or not replacement_path.is_file():
        raise RuntimeError("The original R4-R10 package and replacement must exist")
    current = target.read_bytes()
    replacement = replacement_path.read_bytes()
    if sha256(current) == NEW_SHA256:
        if current != replacement:
            raise RuntimeError("Installed verify.py has a conflicting payload")
        return target, current, replacement, True
    prepared_replacement(current, replacement)
    return target, current, replacement, False


def apply_fix(root: Path, package: Path, *, dry_run: bool) -> str:
    """Atomically replace precisely one untracked file after all guards pass."""
    target, current, replacement, installed = preflight(root, package)
    print("PHASE173_R4_R10R1_SOURCE_GUARD=PASS", flush=True)
    print("PHASE173_R4_R10R1_REVIEWED_HEAD=" + REVIEWED_HEAD, flush=True)
    if installed:
        print("PHASE173_R4_R10R1_ALREADY_INSTALLED=True", flush=True)
        return "ALREADY_INSTALLED"
    if dry_run:
        print("PHASE173_R4_R10R1_DRY_RUN=PASS", flush=True)
        return "DRY_RUN_PASS"
    # All checks ran before this write. The old file is exactly the reviewed ZIP.
    temporary_name = None
    try:
        with tempfile.NamedTemporaryFile(mode="wb", dir=target.parent,
                                         prefix=".r4r10r1_", suffix=".tmp",
                                         delete=False) as stream:
            temporary_name = stream.name
            stream.write(replacement)
            stream.flush()
            os.fsync(stream.fileno())
        if target.read_bytes() != current:
            raise RuntimeError("verify.py changed during preflight")
        os.replace(temporary_name, target)
        temporary_name = None
    finally:
        if temporary_name is not None:
            Path(temporary_name).unlink(missing_ok=True)
    if sha256(target.read_bytes()) != NEW_SHA256:
        raise RuntimeError("Patched verify.py failed its content checksum")
    print("PHASE173_R4_R10R1_PATCHED=verify.py_HEAD_ONLY", flush=True)
    return "PATCHED"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", required=True)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    apply_fix(Path(args.root).resolve(), Path(__file__).resolve().parent,
              dry_run=args.dry_run)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
