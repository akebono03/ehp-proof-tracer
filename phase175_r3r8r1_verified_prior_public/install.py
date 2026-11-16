"""Guarded single-function installer for the R3R8 public proof-search route.

Only a fixed insertion into search_shared_group_goal is permitted. DryRun
never writes to the worktree, and a failed normal audit can restore its exact
original bytes; no Git staging, reset or commit is performed.
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
PINNED_GIT_BLOB = "9fa11b383812570fae1a26868c98992a5934a327"
ANCHOR = "    if citing_assertion_id is not None and expansion_provider is None:\n"
PUBLIC_INSERTION = (
    "    # R3R8R1: connect the R3R7 cited general EHP proof chain, not a saved result.\n"
    "    if n == 3 and k == 4 and expansion_provider is None:\n"
    "        from phase175_r3r8r1_verified_prior_public.route import (\n"
    "            prepare_pi73_public_connection,\n"
    "        )\n"
    "        pi73_connection = prepare_pi73_public_connection(\n"
    "            bridge=bridge, goal=goal, citing_assertion_id=citing_assertion_id,\n"
    "            prior_conclusions=tuple(item.root.conclusion for item in prior),\n"
    "        )\n"
    "        if pi73_connection is not None:\n"
    "            bridge, citing_assertion_id, expansion_provider = pi73_connection\n"
)


def git(root: Path, *args: str) -> str:
    """Only execute nonmutating Git commands."""
    if not args or args[0] not in {"rev-parse", "branch", "diff", "status"}:
        raise ValueError("R3R8 read-only Git operation required")
    process = subprocess.run(
        ["git", *args], cwd=root, capture_output=True, text=True,
        encoding="utf-8", errors="replace", check=False,
    )
    if process.returncode:
        raise RuntimeError("R3R8R1_GIT_QUERY_FAILED: " + " ".join(args))
    return process.stdout.rstrip("\r\n")


def find_function(text: str) -> tuple[int, int]:
    """Find exactly one complete top-level function using Python's AST."""
    parsed = ast.parse(text)
    matches = [node for node in parsed.body
               if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
               and node.name == "search_shared_group_goal"]
    if len(matches) != 1 or not isinstance(matches[0], ast.FunctionDef):
        raise RuntimeError("R3R8R1_SEARCH_FUNCTION_NOT_UNIQUE")
    node = matches[0]
    lines = text.splitlines(keepends=True)
    return (sum(len(line) for line in lines[:node.lineno - 1]),
            sum(len(line) for line in lines[:node.end_lineno]))


def preflight(root: Path = ROOT) -> dict[str, object]:
    """Verify exact tracked original, reviewed function contract and clean index."""
    root = Path(root).resolve()
    if Path(git(root, "rev-parse", "--show-toplevel")).resolve() != root:
        raise RuntimeError("R3R8R1_NOT_REPOSITORY_ROOT")
    if git(root, "branch", "--show-current") != "develop":
        raise RuntimeError("R3R8R1_WRONG_BRANCH")
    if git(root, "rev-parse", "HEAD:" + TARGET.as_posix()) != PINNED_GIT_BLOB:
        raise RuntimeError("R3R8R1_UNREVIEWED_PRODUCTION_BLOB")
    # The prior R3R7 handoff explicitly recorded a clean tracked worktree.
    # A later audited ZIP may replace files already committed at this HEAD.
    # Those changes are allowed only under the exact successor-file policy;
    # the production target itself must still be clean before installation.
    tracked_before = reviewed_tracked_snapshot(root)
    content = (root / TARGET).read_bytes()
    if content.startswith(b"\xef\xbb\xbf"):
        raise RuntimeError("R3R8R1_UNEXPECTED_BOM")
    original = content.decode("utf-8").replace("\r\n", "\n")
    start, end = find_function(original)
    original_function = original[start:end]
    if original_function.count(ANCHOR) != 1 or PUBLIC_INSERTION in original:
        raise RuntimeError("R3R8R1_UNREVIEWED_ROUTING_ANCHOR")
    template = (PACKAGE / "search_shared_group_goal_FULL.py.txt").read_text(encoding="utf-8")
    if template.count(PUBLIC_INSERTION) != 1:
        raise RuntimeError("R3R8R1_FULL_FUNCTION_TEMPLATE_INVALID")
    old_ast = ast.dump(ast.parse(original_function), include_attributes=False)
    source_ast = ast.dump(ast.parse(template.replace(PUBLIC_INSERTION, "")), include_attributes=False)
    if old_ast != source_ast:
        raise RuntimeError("R3R8R1_EXISTING_FUNCTION_CHANGED_SINCE_REVIEW")
    compiled = original[:start] + original_function.replace(
        ANCHOR, PUBLIC_INSERTION + ANCHOR, 1,
    ) + original[end:]
    compile(compiled, str(root / TARGET), "exec")
    worktree_text = content.decode("utf-8")
    newline = "\r\n" if "\r\n" in worktree_text else "\n"
    actual_anchor = ANCHOR.replace("\n", newline)
    actual_insertion = PUBLIC_INSERTION.replace("\n", newline)
    if worktree_text.count(actual_anchor) != 1:
        raise RuntimeError("R3R8R1_WORKTREE_EOL_ANCHOR_CHANGED")
    candidate_bytes = worktree_text.replace(
        actual_anchor, actual_insertion + actual_anchor, 1,
    ).encode("utf-8")
    return {
        "head": git(root, "rev-parse", "HEAD"),
        "original_git_blob": PINNED_GIT_BLOB,
        "original_sha256": sha256(content).hexdigest(),
        "candidate_sha256": sha256(candidate_bytes).hexdigest(),
        "function_name": "search_shared_group_goal",
        "modified_tracked_files": [TARGET.as_posix()],
        "reviewed_tracked_before": tracked_before,
        "new_specific_given": 0,
        "new_proof_replay": 0,
        "whole_pytest_executed": False,
    }


def apply(root: Path, backup_folder: Path) -> dict[str, object]:
    """Replace one function only; preserve the input bytes for rollback."""
    evidence = preflight(root)
    root = Path(root).resolve()
    path = root / TARGET
    before = path.read_bytes()
    original = before.decode("utf-8")
    newline = "\r\n" if "\r\n" in original else "\n"
    anchor = ANCHOR.replace("\n", newline)
    insertion = PUBLIC_INSERTION.replace("\n", newline)
    if original.count(anchor) != 1:
        raise RuntimeError("R3R8R1_SOURCE_ANCHOR_DRIFT")
    final = original.replace(anchor, insertion + anchor, 1).encode("utf-8")
    if sha256(final).hexdigest() != evidence["candidate_sha256"]:
        raise RuntimeError("R3R8R1_CANDIDATE_HASH_CHANGED")
    backup_folder.mkdir(parents=True, exist_ok=True)
    (backup_folder / "phase165_r52_r9_shared_math.py.before").write_bytes(before)
    path.write_bytes(final)
    actual = path.read_bytes()
    if actual != final:
        raise RuntimeError("R3R8R1_WRITE_VERIFICATION_FAILED")
    return {**evidence, "installed_sha256": sha256(actual).hexdigest()}


def verify_postflight(root: Path, evidence: dict[str, object]) -> None:
    """After success, only the one reviewed public function may be dirty."""
    actual = (Path(root) / TARGET).read_bytes()
    if sha256(actual).hexdigest() != evidence["installed_sha256"]:
        raise RuntimeError("R3R8R1_PATCH_MUTATED_AFTER_INSTALL")
    snapshot = reviewed_tracked_snapshot(root, allow_public_target=True)
    public_sha = snapshot.pop(TARGET.as_posix(), None)
    if public_sha != evidence["installed_sha256"]:
        raise RuntimeError("R3R8R1R2_PUBLIC_PATCH_NOT_ONLY_REVIEWED_TARGET")
    if snapshot != evidence["reviewed_tracked_before"]:
        raise RuntimeError("R3R8R1R2_REVIEWED_WORKTREE_CHANGED_DURING_RUN")


def rollback(root: Path, backup_folder: Path) -> None:
    """Restore byte-identical clean original on failed installation or audit."""
    original = (backup_folder / "phase165_r52_r9_shared_math.py.before").read_bytes()
    (Path(root) / TARGET).write_bytes(original)
    if (Path(root) / TARGET).read_bytes() != original:
        raise RuntimeError("R3R8R1_ROLLBACK_VERIFICATION_FAILED")
