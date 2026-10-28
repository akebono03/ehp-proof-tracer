"""Byte-guarded R10EN patch; edit only the two reviewed citation sections."""
from __future__ import annotations

import ast
import hashlib
from pathlib import Path

PACKAGE = Path(__file__).resolve().parent
FILES = (
    (
        "phase169_r10a_verified_stable_chain_projection/projection.py",
        "r10a_before.py.FULL",
        "r10a_after.py.FULL",
    ),
    (
        "phase169_r10ec_direct_sum_narrative_projection/projection.py",
        "r10ec_before.py.FULL",
        "r10ec_after.py.FULL",
    ),
)


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def checked_change(relative: str, current: bytes) -> bytes:
    """Reject unreviewed local bytes; return the whole new file, never a diff."""
    found = [entry for entry in FILES if entry[0] == relative]
    if len(found) != 1:
        raise ValueError("not an R10EN reviewed target")
    _, before_name, after_name = found[0]
    before = (PACKAGE / before_name).read_bytes()
    after = (PACKAGE / after_name).read_bytes()
    if current != before:
        raise ValueError(f"R10EN source mismatch: {relative}")
    ast.parse(after.decode("utf-8"))
    if before == after:
        raise ValueError("R10EN did not change the cited function")
    original_tree = ast.parse(before.decode("utf-8"))
    updated_tree = ast.parse(after.decode("utf-8"))
    function_name = (
        "project_verified_stable_image_chain"
        if "r10a_" in relative
        else "project_verified_direct_sum_transport"
    )
    original_tree.body = [
        node for node in original_tree.body
        if not isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
        or node.name != function_name
    ]
    updated_tree.body = [
        node for node in updated_tree.body
        if not isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
        or node.name != function_name
    ]
    if ast.dump(original_tree) != ast.dump(updated_tree):
        raise ValueError("R10EN changes more than its reviewed function")
    return after


def apply(repo: Path, output: Path) -> list[str]:
    """Validate both targets before touching either; save byte-exact backups."""
    output.mkdir(parents=True, exist_ok=True)
    proposed: list[tuple[Path, bytes, bytes]] = []
    for relative, _, _ in FILES:
        target = repo / relative
        previous = target.read_bytes()
        replacement = checked_change(relative, previous)
        proposed.append((target, previous, replacement))
    updated: list[tuple[Path, bytes]] = []
    try:
        for target, previous, replacement in proposed:
            backup = output / f"{target.parent.name}_{target.name}.before"
            backup.write_bytes(previous)
            target.write_bytes(replacement)
            updated.append((target, previous))
            print("R10EN_PATCHED=" + str(target), flush=True)
        return [str(path) for path, _ in updated]
    except BaseException:
        for target, previous in reversed(updated):
            target.write_bytes(previous)
        raise
