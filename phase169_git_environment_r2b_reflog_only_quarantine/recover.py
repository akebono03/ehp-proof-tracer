"""Non-destructive-first Git ref conflict recovery for a paused Dropbox workspace.

Default audit is read only. Quarantine requires explicit confirmation and makes
an off-Dropbox complete .git backup before moving ONLY three audited reflog conflict copies.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import subprocess
import sys
from datetime import datetime
from pathlib import Path


CONFLICT_PATHS = (
    "logs/HEAD (oomae-pc11 の競合コピー 2026-10-28)",
    "logs/refs/heads/develop (oomae-pc11 の競合コピー 2026-10-28)",
    "logs/refs/remotes/origin/develop (oomae-pc11 の競合コピー 2026-10-28)",
)
R5D_TRACKED = (
    "phase165_r52_r9_shared_math.py",
    "phase169_r10a_verified_stable_chain_projection/tests/test_r10a_verified_stable_chain.py",
    "phase169_r10ec_direct_sum_narrative_projection/tests/test_r10ec_projection.py",
    "phase169_r10el_shared_generator_suppression/tests/test_r10el_live.py",
    "phase169_r10er_r1_mixed_definition_projection/tests/test_r10er_projection.py",
)


def git(root: Path, *args: str, check: bool = True) -> subprocess.CompletedProcess:
    env = dict(os.environ)
    env["GIT_OPTIONAL_LOCKS"] = "0"
    cmd = ["git", "--no-optional-locks", "-C", str(root), "-c", "core.longpaths=true", *args]
    result = subprocess.run(
        cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        timeout=90, check=False, env=env,
    )
    if check and result.returncode:
        raise RuntimeError(
            f"Git read-only check failed ({result.returncode}): "
            + " ".join(args) + "\n"
            + result.stderr.decode("utf-8", errors="replace")[:1500]
        )
    return result


def sha256(path: Path) -> str:
    hasher = hashlib.sha256()
    with path.open("rb") as stream:
        for data in iter(lambda: stream.read(1024 * 1024), b""):
            hasher.update(data)
    return hasher.hexdigest()


def conflict_paths(root: Path) -> tuple[str, ...]:
    gitdir = root / ".git"
    matches: list[str] = []
    for section in ("refs", "logs"):
        base = gitdir / section
        if not base.exists():
            continue
        for p in base.rglob("*"):
            if p.is_file() and ("競合コピー" in p.name or "conflicted copy" in p.name.lower()):
                matches.append(p.relative_to(gitdir).as_posix())
    return tuple(sorted(matches))


def path_within(inside: Path, outside: Path) -> bool:
    try:
        inside.resolve().relative_to(outside.resolve())
        return True
    except ValueError:
        return False


def preflight(root: Path, output_root: Path, mode: str, dropbox_paused: bool) -> dict:
    root, output_root = root.resolve(), output_root.resolve()
    gitdir = root / ".git"
    if not gitdir.is_dir() or gitdir.is_symlink():
        raise RuntimeError("Expected a real .git directory in the repository")
    if path_within(output_root, root) or path_within(root, output_root):
        raise RuntimeError("Recovery output must be separate from the repository")
    if "dropbox" in (part.casefold() for part in output_root.parts):
        raise RuntimeError("Recovery output must be OUTSIDE Dropbox")
    symbolic_head = git(root, "symbolic-ref", "HEAD").stdout.decode().strip()
    if symbolic_head != "refs/heads/develop":
        raise RuntimeError(f"Expected the develop branch; got {symbolic_head}")
    head = git(root, "rev-parse", "--verify", "HEAD").stdout.decode().strip()
    branch_head = git(root, "rev-parse", "--verify", "refs/heads/develop").stdout.decode().strip()
    if head != branch_head or len(head) != 40:
        raise RuntimeError("HEAD is not a valid develop commit")
    paths = conflict_paths(root)
    expected = tuple(sorted(CONFLICT_PATHS))
    if mode == "quarantine":
        if not dropbox_paused:
            raise RuntimeError("Quarantine requires -DropboxPaused after pausing sync on ALL PCs")
        if paths != expected:
            raise RuntimeError(f"Unexpected conflict-copy set: {paths!r}")
        if any((gitdir / p).is_symlink() for p in paths):
            raise RuntimeError("Refusing to quarantine symlinked Git entries")
        for name in ("index.lock", "packed-refs.lock", "HEAD.lock"):
            if (gitdir / name).exists():
                raise RuntimeError(f"Git lock present: {name}; stop concurrent Git processes")
    return {"head": head, "branch": symbolic_head, "conflict_paths": paths}


def capture_paths(root: Path) -> tuple[str, ...]:
    staged = git(root, "diff", "--cached", "--name-only", "-z").stdout
    changed = git(root, "diff", "--name-only", "-z").stdout
    names: set[str] = set(R5D_TRACKED)
    for stream in (staged, changed):
        for encoded in stream.split(b"\0"):
            if encoded:
                names.add(encoded.decode("utf-8", errors="surrogateescape"))
    return tuple(sorted(names))


def backup_and_quarantine(root: Path, output_root: Path, pre: dict) -> Path:
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
    target = output_root / f"ehp_git_conflict_backup_{timestamp}"
    target.mkdir(parents=True, exist_ok=False)
    original_git = root / ".git"
    git_backup = target / "git_complete_backup"
    worktree_backup = target / "tracked_worktree_backup"
    moved: list[tuple[Path, Path]] = []
    try:
        # Complete metadata snapshot, including all refs, reflogs and the Git index.
        shutil.copytree(original_git, git_backup, symlinks=True)
        if (original_git / "index").is_file():
            if sha256(original_git / "index") != sha256(git_backup / "index"):
                raise RuntimeError("Git index changed during backup")
        fingerprints: dict[str, str] = {}
        for rel in pre["conflict_paths"]:
            source = original_git / rel
            copy = git_backup / rel
            if not source.is_file() or not copy.is_file():
                raise RuntimeError("Conflict file missing from complete backup")
            if sha256(source) != sha256(copy):
                raise RuntimeError("Conflict file changed during backup")
            fingerprints[rel] = sha256(source)
        protected = capture_paths(root)
        for rel in protected:
            source = root / rel
            if not source.is_file() or source.is_symlink():
                continue
            if not path_within(source, root):
                raise RuntimeError("Protected path escaped repository")
            destination = worktree_backup / rel
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, destination)
            if sha256(destination) != sha256(source):
                raise RuntimeError("Modified worktree file backup mismatch")
        (target / "backup_manifest.json").write_text(
            json.dumps({"head": pre["head"], "conflicts": fingerprints,
                        "protected_worktree_paths": protected,
                        "git_index_sha256": sha256(git_backup / "index")
                        if (git_backup / "index").is_file() else None},
                       ensure_ascii=False, indent=2) + "\n", encoding="utf-8",
        )
        # All Git writes are restricted to the three known *reflog conflict copies*.
        for rel in pre["conflict_paths"]:
            source = original_git / rel
            if sha256(source) != fingerprints[rel]:
                raise RuntimeError("Conflict copy changed before quarantine")
            dest = target / "quarantined_git_files" / rel
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.move(str(source), str(dest))
            moved.append((source, dest))
            if sha256(dest) != fingerprints[rel]:
                raise RuntimeError("Quarantined copy does not match backup")
        status = git(root, "status", "--short", "--untracked-files=no", check=False)
        refs = git(root, "show-ref", check=False)
        if status.returncode or refs.returncode:
            raise RuntimeError("Post-quarantine Git check failed; restoring conflict files")
        if ((original_git / "index").is_file()
                and sha256(original_git / "index") != sha256(git_backup / "index")):
            raise RuntimeError("Git index changed during quarantine; restoring conflict files")
        if conflict_paths(root):
            raise RuntimeError("Unexpected conflict copies remain; restoring")
        (target / "result.json").write_text(
            json.dumps({"status": "PASS", "head": pre["head"],
                        "moved": list(pre["conflict_paths"]),
                        "git_status": status.stdout.decode("utf-8", errors="replace"),
                        "git_show_ref": refs.stdout.decode("utf-8", errors="replace")[:4000]},
                       ensure_ascii=False, indent=2) + "\n", encoding="utf-8",
        )
    except Exception:
        for source, dest in reversed(moved):
            if dest.is_file() and not source.exists():
                source.parent.mkdir(parents=True, exist_ok=True)
                shutil.move(str(dest), str(source))
        raise
    return target


def main(args=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", required=True, type=Path)
    parser.add_argument("--output-root", required=True, type=Path)
    parser.add_argument("--mode", choices=("audit", "quarantine"), default="audit")
    parser.add_argument("--dropbox-paused", action="store_true")
    params = parser.parse_args(args)
    root = params.root.resolve()
    output_root = params.output_root.resolve()
    print(f"GIT_RECOVERY_MODE={params.mode.upper()}", flush=True)
    pre = preflight(root, output_root, params.mode, params.dropbox_paused)
    print(f"GIT_RECOVERY_HEAD={pre['head']}", flush=True)
    print(f"GIT_RECOVERY_CONFLICT_COUNT={len(pre['conflict_paths'])}", flush=True)
    for rel in pre["conflict_paths"]:
        print(f"GIT_RECOVERY_CONFLICT={rel}", flush=True)
    if params.mode == "audit":
        print("GIT_RECOVERY_NO_CHANGES=True", flush=True)
        return 0
    path = backup_and_quarantine(root, output_root, pre)
    print(f"GIT_RECOVERY_BACKUP={path}", flush=True)
    print("GIT_RECOVERY_QUARANTINE=PASS", flush=True)
    print("GIT_RECOVERY_INDEX_PRESERVED_BY_COPY=True", flush=True)
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as exc:
        print(f"GIT_RECOVERY_REFUSED_OR_FAILED={type(exc).__name__}: {exc}", flush=True)
        sys.exit(1)
