"""Review-guarded Phase 173 Phase 167 Reference test contract correction.

Only three historical test files are eligible for writes. All proof sources,
reference rules, and public Web rendering remain read-only.
"""
from __future__ import annotations

import argparse
import ast
import hashlib
import json
import shutil
import subprocess
from pathlib import Path


REVIEWED_BASE = "ac9149beaf91eeef382bc816234bd2d895398667"
BASE_BLOBS = {
    "tests/test_phase167_r2_range_dedup.py": "13fc81efe267083951d59c009cd10112985fd204",
    "tests/test_phase167_r2_shared_reference.py": "e8f69cffdc2b3cbf3c48bace6a4a83ad3cb00d0e",
    "tests/test_phase167_r2_unified_reference.py": "4ab72c4ff58f24643d0f20562491870dc667f6cf",
    "phase173_r4_r15r13_unified_presentation/layout.py": "aceec41320af5c2e1bafd1ee5fbc455d93851332",
    "web_group_proof_common.py": "0126fd71c66257fc2f4f498a5357d44a67a55884",
    "phase168_r3_5_model_renderer.py": "eb34d6fd4783ca943e07de6e6d9756d0e85ff9b8",
    "web_group_proof.py": "2c66da9c8e80a13812a63b6adda34c9414d8413c",
}
TEST_FILES = tuple(path for path in BASE_BLOBS if path.startswith("tests/"))


def git(repo: Path, *args: str, acceptable: tuple[int, ...] = (0,)) -> str:
    """Run read-only Git commands without mutating the index."""
    result = subprocess.run(
        ("git", "--no-pager", *args), cwd=repo, capture_output=True,
        text=True, encoding="utf-8", errors="replace", check=False,
    )
    if result.returncode not in acceptable:
        raise RuntimeError(
            "Git failed: " + " ".join(args) + ": " + result.stderr.strip()
        )
    return result.stdout.strip()


def normalized(text: str) -> str:
    """Ignore only line-ending differences, not Python source content."""
    return text.replace("\r\n", "\n").replace("\r", "\n")


def reviewed_snapshot(repo: Path, package: Path) -> dict[str, object]:
    """Reject unreviewed test/source changes while preserving unrelated work."""
    repo = repo.resolve(strict=True)
    package = package.resolve(strict=True)
    if package.parent != repo:
        raise RuntimeError("Extract the package at the repository root")
    git_root = Path(git(repo, "rev-parse", "--show-toplevel")).resolve(strict=True)
    if git_root != repo:
        raise RuntimeError("Repository root mismatch")
    if git(repo, "branch", "--show-current") != "develop":
        raise RuntimeError("Phase 173 final R1 requires develop")
    local = git(repo, "rev-parse", "HEAD")
    remote = git(repo, "rev-parse", "origin/develop")
    for head in (local, remote):
        git(repo, "merge-base", "--is-ancestor", REVIEWED_BASE, head)
    target_paths = tuple(BASE_BLOBS)
    remote_changes = git(
        repo, "diff", "--name-only", REVIEWED_BASE, remote, "--", *target_paths
    )
    if remote_changes:
        raise RuntimeError("Reviewed sources changed on origin/develop: " + remote_changes)
    staged = git(repo, "diff", "--cached", "--name-only", "--", *target_paths)
    if staged:
        raise RuntimeError("Staged changes to reviewed files: " + staged)
    for path, expected_blob in BASE_BLOBS.items():
        local_blob = git(repo, "rev-parse", "HEAD:" + path)
        remote_blob = git(repo, "rev-parse", "origin/develop:" + path)
        if local_blob != expected_blob or remote_blob != expected_blob:
            raise RuntimeError("Reviewed blob mismatch: " + path)
    for path in TEST_FILES:
        name = Path(path).name
        local_file = repo / path
        actual = normalized(local_file.read_text(encoding="utf-8-sig"))
        expected = normalized((package / "expected" / name).read_text(encoding="utf-8"))
        replacement = normalized((package / "replacement" / name).read_text(encoding="utf-8"))
        if actual not in (expected, replacement):
            raise RuntimeError("Unreviewed local changes to " + path)
    return {
        "head": local,
        "remote_head": remote,
        "reviewed_base": REVIEWED_BASE,
        "reviewed_blob_count": len(BASE_BLOBS),
        "git_index_tree": git(repo, "write-tree"),
    }


def _read_original_line_ending(path: Path) -> str:
    raw = path.read_bytes()
    if b"\r\n" in raw:
        return "\r\n"
    return "\n"


def _write_same_line_ending(path: Path, content: str, line_ending: str) -> None:
    text = normalized(content)
    if line_ending == "\r\n":
        text = text.replace("\n", "\r\n")
    path.write_bytes(text.encode("utf-8"))


def prepare_full_units(package: Path) -> None:
    """Output entire replacement test files, including their complete imports."""
    output = package / "full_changed_tests"
    output.mkdir(parents=True, exist_ok=True)
    pages = [
        "# Phase 173 final R1: full replacement test files",
        "",
        "Only three historical test files are changed. Every import and test",
        "function is included below without abbreviated code.",
        "",
    ]
    for path in TEST_FILES:
        name = Path(path).name
        replacement = (package / "replacement" / name).read_text(encoding="utf-8")
        ast.parse(replacement, filename=path)
        (output / name).write_text(replacement, encoding="utf-8")
        pages.extend(("## `" + path + "`", "", "```python", replacement.rstrip(), "```", ""))
    (package / "FULL_CHANGED_UNITS.md").write_text("\n".join(pages), encoding="utf-8")


def _digest(content: bytes) -> str:
    return hashlib.sha256(content).hexdigest()


def apply_tests(repo: Path, package: Path) -> bool:
    """Install only the three reviewed test files and keep exact local backups."""
    snapshot = reviewed_snapshot(repo, package)
    prepare_full_units(package)
    original_status = []
    for path in TEST_FILES:
        name = Path(path).name
        current = normalized((repo / path).read_text(encoding="utf-8-sig"))
        expected = normalized((package / "expected" / name).read_text(encoding="utf-8"))
        replacement = normalized((package / "replacement" / name).read_text(encoding="utf-8"))
        original_status.append("original" if current == expected else "installed")
        if current not in (expected, replacement):
            raise RuntimeError("Unreviewed worktree content: " + path)
    if all(value == "installed" for value in original_status):
        print("PHASE173_FINAL_R1_ALREADY_INSTALLED=PASS")
        return False
    if any(value != "original" for value in original_status):
        raise RuntimeError("Partially applied test contract requires manual review")

    backup_root = package / "original_backups" / "tests"
    backup_root.mkdir(parents=True, exist_ok=True)
    for path in TEST_FILES:
        backup = backup_root / Path(path).name
        if backup.exists():
            if backup.read_bytes() != (repo / path).read_bytes():
                raise RuntimeError("Existing backup does not match current source: " + path)
        else:
            shutil.copyfile(repo / path, backup)

    manifest = {
        "head": snapshot["head"],
        "git_index_tree": snapshot["git_index_tree"],
        "files": {
            path: _digest((repo / path).read_bytes()) for path in TEST_FILES
        },
    }
    (package / "original_backups" / "manifest.json").write_text(
        json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    installed = []
    try:
        for path in TEST_FILES:
            name = Path(path).name
            source = repo / path
            eol = _read_original_line_ending(source)
            replacement = (package / "replacement" / name).read_text(encoding="utf-8")
            _write_same_line_ending(source, replacement, eol)
            installed.append(path)
    except BaseException:
        for path in installed:
            shutil.copyfile(backup_root / Path(path).name, repo / path)
        raise
    print("PHASE173_FINAL_R1_INSTALL=PASS")
    return True


def rollback_tests(repo: Path, package: Path) -> None:
    """Restore only files installed by this package, without invoking Git restore."""
    manifest_file = package / "original_backups" / "manifest.json"
    if not manifest_file.is_file():
        raise RuntimeError("No installation manifest to roll back")
    manifest = json.loads(manifest_file.read_text(encoding="utf-8"))
    backup_root = package / "original_backups" / "tests"
    for path in TEST_FILES:
        name = Path(path).name
        replacement = normalized((package / "replacement" / name).read_text(encoding="utf-8"))
        actual = normalized((repo / path).read_text(encoding="utf-8-sig"))
        if actual != replacement:
            raise RuntimeError("Refusing to overwrite post-install edits in " + path)
        backup = backup_root / name
        if _digest(backup.read_bytes()) != manifest["files"][path]:
            raise RuntimeError("Backup checksum mismatch for " + path)
    for path in TEST_FILES:
        shutil.copyfile(backup_root / Path(path).name, repo / path)
    print("PHASE173_FINAL_R1_ROLLBACK=PASS")


def main() -> int:
    parser = argparse.ArgumentParser(description="Repair old Phase 167 reference-section tests")
    parser.add_argument("action", choices=("dry-run", "apply", "rollback"))
    parser.add_argument("--repo", required=True, type=Path)
    parser.add_argument("--package", required=True, type=Path)
    args = parser.parse_args()
    repo, package = args.repo.resolve(strict=True), args.package.resolve(strict=True)
    if args.action == "rollback":
        rollback_tests(repo, package)
        return 0
    snapshot = reviewed_snapshot(repo, package)
    prepare_full_units(package)
    print("PHASE173_FINAL_R1_LOCAL_HEAD=" + str(snapshot["head"]))
    print("PHASE173_FINAL_R1_REMOTE_HEAD=" + str(snapshot["remote_head"]))
    print("PHASE173_FINAL_R1_REVIEWED_BLOBS=" + str(snapshot["reviewed_blob_count"]))
    print("PHASE173_FINAL_R1_SOURCE_GUARD=PASS")
    if args.action == "dry-run":
        print("PHASE173_FINAL_R1_PRODUCTION_WRITES=NONE")
        print("PHASE173_FINAL_R1_DRY_RUN=PASS")
    else:
        apply_tests(repo, package)
    after = git(repo, "write-tree")
    if after != snapshot["git_index_tree"]:
        raise RuntimeError("Git index changed during Phase 173 final R1")
    print("PHASE173_FINAL_R1_GIT_INDEX_PRESERVED=PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
