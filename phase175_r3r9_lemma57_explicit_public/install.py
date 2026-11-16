"""Replace exactly one reviewed public routing function with bytewise rollback.

The input is the audited R3R8R1R2 public-route function already committed to
develop; the only change is its Phase 175 pi73 route import and comment.
No top-level imports, mathematical rules or unrelated functions are modified.
"""
from __future__ import annotations

import ast
from hashlib import sha256
from pathlib import Path
import subprocess

from phase175_r3r8r1_verified_prior_public.worktree_guard import (
    reviewed_tracked_snapshot,
)

ROOT = Path(__file__).resolve().parents[1]
PACKAGE = Path(__file__).resolve().parent
TARGET = Path("phase165_r52_r9_shared_math.py")
PINNED_GIT_BLOB = "3426b223f94e839e77972801977d58a4ca182767"
PINNED_HEAD_ANCESTOR = "7171af968ba510291f87b8bb484d8718a3cef204"
OLD_ROUTE = (
    "    # R3R8R1: connect the R3R7 cited general EHP proof chain, not a saved result.\n"
    "    if n == 3 and k == 4 and expansion_provider is None:\n"
    "        from phase175_r3r8r1_verified_prior_public.route import (\n"
)
NEW_ROUTE = (
    "    # R3R9: cite the explicit nu-prime consequence of Lemma 5.7.\n"
    "    if n == 3 and k == 4 and expansion_provider is None:\n"
    "        from phase175_r3r9_lemma57_explicit_public.route import (\n"
)


def git(root: Path, *args: str) -> str:
    """Read Git metadata; never stage, reset, check out or commit."""
    if not args or args[0] not in {"rev-parse", "branch"}:
        raise ValueError("R3R9_GIT_READ_ONLY_OPERATION_REQUIRED")
    result = subprocess.run(
        ["git", *args], cwd=root, capture_output=True, text=True,
        encoding="utf-8", errors="replace", check=False,
    )
    if result.returncode:
        raise RuntimeError("R3R9_GIT_READ_FAILED: " + " ".join(args))
    return result.stdout.strip()


def find_function(text: str) -> tuple[int, int]:
    """Get exact offsets for the sole top-level public search function."""
    try:
        tree = ast.parse(text)
    except SyntaxError as exc:
        raise RuntimeError("R3R9_INVALID_REVIEWED_CODE_AST") from exc
    matches = [node for node in tree.body
               if isinstance(node, ast.FunctionDef)
               and node.name == "search_shared_group_goal"]
    if len(matches) != 1:
        raise RuntimeError("R3R9_SEARCH_FUNCTION_NOT_UNIQUE")
    lines = text.splitlines(keepends=True)
    node = matches[0]
    return (
        sum(len(line) for line in lines[:node.lineno - 1]),
        sum(len(line) for line in lines[:node.end_lineno]),
    )


def replace_function_bytes(before: bytes, *, require_exact_template: bool = True) -> bytes:
    """Preserve all bytes outside one AST-reviewed function, including CRLF."""
    if before.startswith(b"\xef\xbb\xbf"):
        raise RuntimeError("R3R9_UNEXPECTED_UTF8_BOM")
    original = before.decode("utf-8")
    newline = "\r\n" if "\r\n" in original else "\n"
    if "\r\n" in original and "\n" in original.replace("\r\n", ""):
        raise RuntimeError("R3R9_MIXED_NEWLINES")
    normalized = original.replace("\r\n", "\n")
    start, end = find_function(normalized)
    function = normalized[start:end]
    old_template = (PACKAGE / "search_shared_group_goal_BEFORE.py.txt").read_text(
        encoding="utf-8",
    )
    new_template = (PACKAGE / "search_shared_group_goal_FULL.py.txt").read_text(
        encoding="utf-8",
    )
    if (
        old_template.count(OLD_ROUTE) != 1
        or old_template.replace(OLD_ROUTE, NEW_ROUTE, 1) != new_template
        or new_template.count(NEW_ROUTE) != 1
    ):
        raise RuntimeError("R3R9_TEMPLATE_HAS_UNREVIEWED_EDIT")
    if require_exact_template and ast.dump(
        ast.parse(function), include_attributes=False,
    ) != ast.dump(ast.parse(old_template), include_attributes=False):
        raise RuntimeError("R3R9_SOURCE_FUNCTION_CHANGED_SINCE_REVIEW")
    if function.count(OLD_ROUTE) != 1:
        raise RuntimeError("R3R9_OLD_ROUTE_NOT_UNIQUE")
    candidate = normalized[:start] + new_template + normalized[end:]
    compile(candidate, str(TARGET), "exec")
    actual_old = OLD_ROUTE.replace("\n", newline)
    actual_new = NEW_ROUTE.replace("\n", newline)
    if original.count(actual_old) != 1:
        raise RuntimeError("R3R9_EOL_ANCHOR_CHANGED")
    return original.replace(actual_old, actual_new, 1).encode("utf-8")


def preflight(root: Path = ROOT) -> dict[str, object]:
    """Require committed reviewed baseline and no unrelated tracked edits."""
    root = Path(root).resolve()
    if Path(git(root, "rev-parse", "--show-toplevel")).resolve() != root:
        raise RuntimeError("R3R9_NOT_REPOSITORY_ROOT")
    if git(root, "branch", "--show-current") != "develop":
        raise RuntimeError("R3R9_WRONG_BRANCH")
    if git(root, "rev-parse", "HEAD:" + TARGET.as_posix()) != PINNED_GIT_BLOB:
        raise RuntimeError("R3R9_BASE_PRODUCTION_BLOB_NOT_COMMITTED")
    # Prior package's guard allows its own known docs but NOT the production
    # target. This also rejects staging, unknown edits and dirty core files.
    prior_snapshot = reviewed_tracked_snapshot(root, allow_public_target=False)
    before = (root / TARGET).read_bytes()
    candidate = replace_function_bytes(before)
    return {
        "head": git(root, "rev-parse", "HEAD"),
        "pinned_blob": PINNED_GIT_BLOB,
        "before_sha256": sha256(before).hexdigest(),
        "candidate_sha256": sha256(candidate).hexdigest(),
        "reviewed_tracked_before": prior_snapshot,
        "function_name": "search_shared_group_goal",
        "new_group_given": 0,
        "full_pytest": False,
    }


def apply(root: Path, backup_folder: Path) -> dict[str, object]:
    """Install one whole function after backing up the complete original file."""
    evidence = preflight(root)
    path = Path(root) / TARGET
    before = path.read_bytes()
    if sha256(before).hexdigest() != evidence["before_sha256"]:
        raise RuntimeError("R3R9_INPUT_CHANGED_BETWEEN_PREFLIGHT_AND_APPLY")
    after = replace_function_bytes(before)
    if sha256(after).hexdigest() != evidence["candidate_sha256"]:
        raise RuntimeError("R3R9_REWRITTEN_HASH_MISMATCH")
    backup_folder.mkdir(parents=True, exist_ok=True)
    (backup_folder / "phase165_r52_r9_shared_math.py.before").write_bytes(before)
    try:
        path.write_bytes(after)
        if path.read_bytes() != after:
            raise RuntimeError("R3R9_POST_WRITE_MISMATCH")
    except Exception:
        # If the installer fails after writing but before returning, the
        # caller has not yet set its installed flag. Restore locally here.
        path.write_bytes(before)
        if path.read_bytes() != before:
            raise RuntimeError("R3R9_INSTALLER_LOCAL_ROLLBACK_FAILED")
        raise
    return {**evidence, "installed_sha256": sha256(after).hexdigest()}


def verify_postflight(root: Path, evidence: dict[str, object]) -> None:
    """Allow exactly the installed production patch, not any other drift."""
    if sha256((Path(root) / TARGET).read_bytes()).hexdigest() != evidence["installed_sha256"]:
        raise RuntimeError("R3R9_INSTALL_MUTATED")
    status = reviewed_tracked_snapshot(root, allow_public_target=True)
    public = status.pop(TARGET.as_posix(), None)
    if public != evidence["installed_sha256"]:
        raise RuntimeError("R3R9_PUBLIC_PATCH_NOT_TRACKED")
    if status != evidence["reviewed_tracked_before"]:
        raise RuntimeError("R3R9_UNRELATED_TRACKED_CHANGE_AFTER_INSTALL")


def rollback(root: Path, backup_folder: Path) -> None:
    """Restore exact bytes, without invoking Git commands."""
    path = Path(root) / TARGET
    old = (backup_folder / "phase165_r52_r9_shared_math.py.before").read_bytes()
    path.write_bytes(old)
    if path.read_bytes() != old:
        raise RuntimeError("R3R9_ROLLBACK_FAILED")
