"""Conservative rescue of invalid Dropbox conflict copies inside Git refs.

No branch ref, index, worktree, pack, log, or tracked source is modified.
Only a verified invalid loose-ref conflict copy may be relocated.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
from datetime import datetime

PREFIX = "GIT_REF_R1"
EXPECTED_PARENTS = (Path("refs/heads"), Path("refs/remotes/origin"))
CONFLICT = "競合コピー"


def git(root: Path, *args: str, check: bool = True) -> tuple[int, str, str]:
    completed = subprocess.run(
        ["git", *args], cwd=root, stdout=subprocess.PIPE,
        stderr=subprocess.PIPE, check=False,
    )
    stdout = completed.stdout.decode("utf-8", errors="replace").strip()
    stderr = completed.stderr.decode("utf-8", errors="replace").strip()
    if check and completed.returncode != 0:
        raise RuntimeError(f"git {' '.join(args)}: exit {completed.returncode}; {stderr or stdout}")
    return completed.returncode, stdout, stderr


def git_directory(root: Path, option: str) -> Path:
    _, value, _ = git(root, "rev-parse", option)
    if not value:
        raise RuntimeError(f"Cannot determine {option}")
    directory = Path(value)
    if not directory.is_absolute():
        directory = root / directory
    directory = directory.resolve()
    if not directory.is_dir():
        raise RuntimeError(f"Not a Git directory: {directory}")
    return directory


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        while True:
            block = stream.read(1048576)
            if not block:
                break
            digest.update(block)
    return digest.hexdigest()


def classify_loose_ref(relative: Path) -> str:
    """Use semantic markers, not a brittle literal filename or encoding guess."""
    if relative.parent not in EXPECTED_PARENTS:
        return "OUT_OF_SCOPE"
    name = relative.name
    if not name.startswith("develop"):
        return "OUT_OF_SCOPE"
    if CONFLICT not in name:
        return "DEVELOP_NEIGHBOR"
    if name == "develop":
        return "PROTECTED_VALID_REF"
    return "CONFLICT_CANDIDATE"


def scan_git_metadata(directory: Path) -> dict:
    """Read recursively, including loose ref candidates and packed-refs markers."""
    candidates: list[dict] = []
    adjacent: list[dict] = []
    refs = directory / "refs"
    if refs.is_dir():
        for folder, _, files in os.walk(refs, followlinks=False):
            for name in sorted(files):
                path = Path(folder) / name
                if path.is_symlink():
                    continue
                relative = path.relative_to(directory)
                kind = classify_loose_ref(relative)
                if kind == "OUT_OF_SCOPE":
                    continue
                if kind == "DEVELOP_NEIGHBOR":
                    adjacent.append({
                        "path": str(relative).replace("\\", "/"),
                        "name_repr": ascii(name),
                    })
                if kind == "CONFLICT_CANDIDATE":
                    candidates.append({
                        "path": str(relative).replace("\\", "/"),
                        "name_repr": ascii(name),
                        "sha256": sha256_file(path),
                        "size": path.stat().st_size,
                    })
    packed_findings: list[str] = []
    packed_path = directory / "packed-refs"
    if packed_path.is_file():
        for line_number, raw in enumerate(packed_path.read_bytes().splitlines(), 1):
            if (b"refs/heads/develop" in raw or b"refs/remotes/origin/develop" in raw) and b" " in raw:
                # A well-formed packed ref line itself contains a SHA and a space.
                parts = raw.split(b" ", 1)
                if len(parts) == 2 and (
                    b" " in parts[1] or b"\t" in parts[1]
                ):
                    packed_findings.append(f"packed-refs:{line_number}:{raw[:240]!r}")
    return {
        "directory": str(directory),
        "candidates": candidates,
        "adjacent": adjacent,
        "packed_findings": packed_findings,
    }


def reference_snapshot(root: Path) -> dict:
    _, branch, _ = git(root, "branch", "--show-current")
    if branch != "develop":
        raise RuntimeError(f"Expected develop; got {branch!r}")
    values = {}
    for name in ("HEAD", "refs/heads/develop", "refs/remotes/origin/develop"):
        _, value, _ = git(root, "rev-parse", "--verify", name + "^{commit}")
        if re.fullmatch("[a-f0-9]{40}", value) is None:
            raise RuntimeError("Invalid SHA for " + name)
        values[name] = value
    if values["HEAD"] != values["refs/heads/develop"]:
        raise RuntimeError("HEAD and develop do not agree")
    return values


def diagnostics(root: Path) -> dict:
    common = git_directory(root, "--git-common-dir")
    own = git_directory(root, "--git-dir")
    scans = [scan_git_metadata(common)]
    if own != common:
        scans.append(scan_git_metadata(own))
    code, _, ref_warning = git(root, "for-each-ref", "--format=%(refname)", check=False)
    return {
        "git_dir": str(own),
        "common_dir": str(common),
        "scans": scans,
        "ref_enumeration_exit": code,
        "ref_enumeration_warnings": ref_warning.splitlines()[:24],
    }


def rescue(root: Path, repair: bool, backup_parent: Path | None = None) -> dict:
    root = root.resolve()
    snapshot = reference_snapshot(root)
    info = diagnostics(root)
    matches = []
    for scan in info["scans"]:
        directory = Path(scan["directory"])
        for item in scan["candidates"]:
            original = directory / Path(item["path"])
            if (not original.is_file() or original.is_symlink()
                    or not original.resolve().is_relative_to(directory)):
                raise RuntimeError("Unexpected loose-ref candidate path")
            # A valid branch ref must NEVER be removed.
            code, _, _ = git(root, "check-ref-format", item["path"], check=False)
            if code == 0:
                raise RuntimeError(f"Valid Git ref cannot be relocated: {item['path']}")
            matches.append((directory, original, item))
    if len(matches) > 2:
        raise RuntimeError("More than two candidates; refusing automatic repair")
    packed = [value for scan in info["scans"] for value in scan["packed_findings"]]
    warnings = info["ref_enumeration_warnings"]
    result = {
        "mode": "REPAIR" if repair else "DRY_RUN",
        "references_before": snapshot,
        "diagnostics": info,
        "matched_count": len(matches),
        "moved": [],
        "backup": None,
        "status": "INSPECT_ONLY",
    }
    if packed:
        result["status"] = "PACKED_REFS_NEEDS_MANUAL_REVIEW"
        return result
    if not matches:
        result["status"] = (
            "NO_CANDIDATE_BUT_GIT_REPORTS_BROKEN_REF"
            if any("broken name" in s or "bad ref" in s for s in warnings)
            else "NO_CONFLICT_CANDIDATE_FOUND"
        )
        return result
    if not repair:
        result["status"] = "CANDIDATES_FOUND_DRY_RUN"
        return result
    if backup_parent is None:
        backup_parent = Path.home()
    backup_parent = backup_parent.resolve()
    if backup_parent == root or root in backup_parent.parents:
        raise RuntimeError("Backup cannot be within repository")
    stamp = datetime.now().strftime("%Y%m%d-%H%M%S-%f")
    backup = backup_parent / ("ehp-git-ref-conflict-backup-r1-" + stamp)
    backup.mkdir(parents=False, exist_ok=False)
    moved: list[tuple[Path, Path, dict]] = []
    try:
        for position, (directory, original, item) in enumerate(matches):
            dest = backup / str(position) / Path(item["path"])
            dest.parent.mkdir(parents=True, exist_ok=True)
            if sha256_file(original) != item["sha256"]:
                raise RuntimeError("Candidate changed during audit: " + item["path"])
            shutil.move(str(original), str(dest))
            moved.append((original, dest, item))
            if sha256_file(dest) != item["sha256"]:
                raise RuntimeError("Backup hash differs: " + item["path"])
        after = reference_snapshot(root)
        if after != snapshot:
            raise RuntimeError("Protected refs changed during repair")
        after_info = diagnostics(root)
        if any("broken name" in w for w in after_info["ref_enumeration_warnings"]):
            raise RuntimeError("Git still reports invalid refs: rolling back")
        manifest = {
            "original_refs": snapshot,
            "moves": [
                {"from": str(original), "to": str(dest), "sha256": item["sha256"]}
                for original, dest, item in moved
            ],
        }
        (backup / "manifest.json").write_text(
            json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )
        result.update(
            moved=[item["path"] for _, _, item in moved],
            backup=str(backup), status="PASS",
        )
        return result
    except BaseException:
        for original, dest, _ in reversed(moved):
            if dest.exists() and not original.exists():
                original.parent.mkdir(parents=True, exist_ok=True)
                shutil.move(str(dest), str(original))
        raise


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repair", action="store_true")
    parser.add_argument("--root", type=Path, default=Path.cwd())
    args = parser.parse_args(argv)
    try:
        result = rescue(args.root, args.repair)
    except (RuntimeError, OSError) as exc:
        print(f"{PREFIX}_ERROR={exc}", file=sys.stderr)
        return 2
    print(f"{PREFIX}_MODE={result['mode']}")
    print(f"{PREFIX}_HEAD={result['references_before']['HEAD']}")
    print(f"{PREFIX}_ORIGIN_DEVELOP={result['references_before']['refs/remotes/origin/develop']}")
    print(f"{PREFIX}_CANDIDATES={result['matched_count']}")
    for item in result["diagnostics"]["scans"]:
        print(f"{PREFIX}_SCANNED_DIR={item['directory']}")
        print(f"{PREFIX}_SCANNED_CANDIDATES={json.dumps(item['candidates'], ensure_ascii=False)}")
        print(f"{PREFIX}_ADJACENT={json.dumps(item['adjacent'], ensure_ascii=False)}")
        print(f"{PREFIX}_PACKED={json.dumps(item['packed_findings'], ensure_ascii=False)}")
    print(f"{PREFIX}_GIT_WARNINGS={json.dumps(result['diagnostics']['ref_enumeration_warnings'], ensure_ascii=False)}")
    print(f"{PREFIX}_STATUS={result['status']}")
    if result["backup"]:
        print(f"{PREFIX}_BACKUP={result['backup']}")
        print(f"{PREFIX}_MOVED={json.dumps(result['moved'], ensure_ascii=False)}")
    if result["status"] == "PASS":
        return 0
    if result["status"] in ("CANDIDATES_FOUND_DRY_RUN", "NO_CONFLICT_CANDIDATE_FOUND") and not args.repair:
        return 0
    return 3


if __name__ == "__main__":
    sys.exit(main())
