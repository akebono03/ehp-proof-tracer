"""Install one reviewed shared Web-adapter projection with full rollback."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import subprocess

from phase173_r4_r15r9_shared_abstract_renderer.patch_source import (
    BASELINE_BLOB,
    normalized,
    transform,
    write_complete_sources,
)


REVIEWED_HEAD = "e3fa8cf71777b1bf5bb431ec06cd2147bce69086"
TARGET = "phase165_r52_r3_web_adapter.py"
DEPENDENCY_BLOBS = {
    "phase168_r3_5_model_renderer.py": "6bfd5e992f6c9ee9441920e10e63e0db4bece289",
    "phase165_r52_r9_shared_math.py": "f49b0b7699e29ec1b78d73578dc66a0e33d6e336",
    "web_group_proof.py": "2c66da9c8e80a13812a63b6adda34c9414d8413c",
    "phase165_r52_partial_proof.py": "0af6b459ed5a136a8e30a9e349ccf9fa601d448b",
    "phase165_r55_nk_only_goal.py": "9aa232c8f98a7a75f27266044224eddfa98c5e04",
}
ALLOWED_CHANGED_PREFIXES = (
    "phase173_r4_r15r8_public_abstract_sidecar/",
)
ALLOWED_CHANGED_PATHS = frozenset({
    ".pytest_cache/v/cache/nodeids",
    "phase165_r52_partial_proof.py",
    "phase165_r55_nk_only_goal.py",
})


def _run(root: Path, *args: str, binary: bool = False) -> bytes | str:
    result = subprocess.run(
        ("git", *args), cwd=root, check=False, capture_output=True,
        text=not binary, encoding=None if binary else "utf-8",
        errors=None if binary else "replace",
    )
    if result.returncode:
        raise RuntimeError("Git command failed: " + " ".join(args)
                           + " " + str(result.stderr)[:250])
    return result.stdout if binary else result.stdout.strip()


def sha(data: bytes) -> str:
    return hashlib.sha256(normalized(data)).hexdigest()


def preflight(root: Path) -> tuple[bytes, bytes, str]:
    """Guard committed R15R8 dependencies and unchanged shared renderer."""
    root = root.resolve()
    if Path(_run(root, "rev-parse", "--show-toplevel")).resolve() != root:
        raise RuntimeError("Wrong repository root")
    if _run(root, "branch", "--show-current") != "develop":
        raise RuntimeError("Expected develop branch")
    head = _run(root, "rev-parse", "HEAD")
    remote = _run(root, "rev-parse", "origin/develop")
    if head != remote:
        raise RuntimeError("Local and origin/develop HEAD disagree")
    ancestor = subprocess.run(
        ("git", "merge-base", "--is-ancestor", REVIEWED_HEAD, head),
        cwd=root, check=False, capture_output=True,
    )
    if ancestor.returncode:
        raise RuntimeError("Unreviewed Git HEAD lineage")
    changed = _run(root, "diff", "--name-only", REVIEWED_HEAD, head).splitlines()
    if any(path not in ALLOWED_CHANGED_PATHS and not path.startswith(ALLOWED_CHANGED_PREFIXES)
           for path in changed):
        raise RuntimeError("Unreviewed committed change after R15R8: " + repr(changed))
    if _run(root, "diff", "--cached", "--name-only"):
        raise RuntimeError("Staged source changes require review")
    dirty = _run(root, "diff", "--name-only").splitlines()
    if any(path not in {TARGET, ".pytest_cache/v/cache/nodeids"} for path in dirty):
        raise RuntimeError("Unreviewed local tracked changes: " + repr(dirty))
    for path, blob in DEPENDENCY_BLOBS.items():
        if _run(root, "rev-parse", "HEAD:" + path) != blob:
            raise RuntimeError("Unreviewed dependency Git blob: " + path)
        if _run(root, "hash-object", "--", path) != blob:
            raise RuntimeError("Dependency file has local edits: " + path)
    if _run(root, "rev-parse", "HEAD:" + TARGET) != BASELINE_BLOB:
        raise RuntimeError("Shared Web adapter Git baseline was not reviewed")
    baseline = _run(root, "show", "HEAD:" + TARGET, binary=True)
    candidate = transform(baseline)
    existing = (root / TARGET).read_bytes()
    if normalized(existing) == normalized(baseline):
        state = "BASELINE"
    elif normalized(existing) == normalized(candidate):
        state = "PATCHED"
    else:
        raise RuntimeError("Unreviewed shared Web adapter content")
    package = Path(__file__).resolve().parent
    reviewed_source = package / "reviewed_source" / "phase165_r52_r3_web_adapter_BASELINE.py.txt"
    if not reviewed_source.is_file() or normalized(reviewed_source.read_bytes()) != normalized(baseline):
        raise RuntimeError("Packaged reviewed full adapter differs from Git baseline")
    print("PHASE173_R4_R15R9_HEAD=" + head, flush=True)
    print("PHASE173_R4_R15R9_HEAD_LINEAGE=PASS", flush=True)
    print("PHASE173_R4_R15R9_SOURCE_GUARD=PASS", flush=True)
    print("PHASE173_R4_R15R9_INSTALL_STATE=" + state, flush=True)
    return baseline, candidate, state


def install(root: Path, *, dry_run: bool) -> None:
    baseline, candidate, state = preflight(root)
    package = Path(__file__).resolve().parent
    write_complete_sources(baseline, package / "reviewed_full_source")
    if dry_run:
        print("PHASE173_R4_R15R9_DRY_RUN=PASS", flush=True)
        print("PHASE173_R4_R15R9_PRODUCTION_EDIT=NONE", flush=True)
        return
    if state == "PATCHED":
        print("PHASE173_R4_R15R9_ALREADY_INSTALLED=True", flush=True)
        return
    backup = package / "reviewed_full_source" / "original_adapter.py.bak"
    original_bytes = (root / TARGET).read_bytes()
    backup.write_bytes(original_bytes)
    # Preserve a clean CRLF checkout rather than normalizing unrelated lines.
    candidate_for_worktree = transform(original_bytes)
    destination = root / TARGET
    temporary = destination.with_suffix(destination.suffix + ".r15r9_tmp")
    try:
        temporary.write_bytes(candidate_for_worktree)
        temporary.replace(destination)
    except Exception:
        temporary.unlink(missing_ok=True)
        destination.write_bytes(baseline)
        raise
    (package / "installed_state.json").write_text(json.dumps({
        "phase": "173-R4-R15R9",
        "original_sha256": sha(baseline),
        "patched_sha256": sha(candidate),
        "complete_named_proof_promoted": False,
        "public_web_partial_status_preserved": True,
    }, indent=2) + "\n", encoding="utf-8")
    print("PHASE173_R4_R15R9_PATCHED=" + TARGET, flush=True)


def restore(root: Path) -> None:
    baseline, candidate, state = preflight(root)
    if state == "BASELINE":
        print("PHASE173_R4_R15R9_ROLLBACK=ALREADY_BASELINE", flush=True)
        return
    package = Path(__file__).resolve().parent
    backup = package / "reviewed_full_source" / "original_adapter.py.bak"
    if not backup.is_file() or normalized(backup.read_bytes()) != normalized(baseline):
        raise RuntimeError("Guarded rollback backup absent or incorrect")
    (root / TARGET).write_bytes(backup.read_bytes())
    print("PHASE173_R4_R15R9_ROLLBACK=PASS", flush=True)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--restore", action="store_true")
    args = parser.parse_args()
    root = args.root.resolve()
    if args.restore:
        restore(root)
    else:
        install(root, dry_run=args.dry_run)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
