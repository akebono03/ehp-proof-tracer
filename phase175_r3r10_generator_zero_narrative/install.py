"""Guarded function-level installation of the Phase 175 R3R10 display fix."""
from __future__ import annotations

import ast
from dataclasses import dataclass
import os
from pathlib import Path
import tempfile

PACKAGE = Path(__file__).resolve().parent
TARGET_RELATIVE = Path("phase168_r3_27_typed_statement_projection.py")
BASE_FILE = PACKAGE / "full_functions" / "typed_sentence_BASE.py"
REPLACEMENT_FILE = PACKAGE / "full_functions" / "typed_sentence_FULL.py"
PINNED_HEAD_BLOB = "9ce32b5db34a3981649b9b9f2c5ff897eb8de831"


@dataclass(frozen=True)
class PatchPlan:
    status: str
    old_bytes: bytes
    new_bytes: bytes
    expected_function: str
    replacement_function: str


def _function_span(content: str, function_name: str) -> tuple[int, int]:
    """Use Python syntax to identify an entire, top-level function safely."""
    tree = ast.parse(content)
    matches = [
        node for node in tree.body
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
        and node.name == function_name
    ]
    if len(matches) != 1:
        raise RuntimeError("R3R10_TYPED_SENTENCE_FUNCTION_NOT_UNIQUE")
    node = matches[0]
    if node.decorator_list:
        raise RuntimeError("R3R10_UNEXPECTED_FUNCTION_DECORATOR")
    return node.lineno - 1, node.end_lineno


def _normalized_function(content: str) -> str:
    """Normalize line endings, not source code or import semantics."""
    normalized = content.replace("\r\n", "\n")
    first, last = _function_span(normalized, "typed_sentence")
    return "".join(normalized.splitlines(keepends=True)[first:last]).rstrip("\n") + "\n"


def plan_patch(root: Path) -> PatchPlan:
    target = Path(root) / TARGET_RELATIVE
    if not target.is_file():
        raise RuntimeError("R3R10_TARGET_FILE_MISSING")
    original = target.read_bytes()
    if original.startswith(b"\xef\xbb\xbf"):
        raise RuntimeError("R3R10_UNEXPECTED_UTF8_BOM")
    original_text = original.decode("utf-8")
    baseline = _normalized_function(BASE_FILE.read_text(encoding="utf-8"))
    replacement = _normalized_function(REPLACEMENT_FILE.read_text(encoding="utf-8"))
    observed = _normalized_function(original_text)
    if observed == replacement:
        return PatchPlan("ALREADY_APPLIED", original, original, baseline, replacement)
    if observed != baseline:
        raise RuntimeError("R3R10_CURRENT_TYPED_SENTENCE_DIFFERS_FROM_REVIEWED_BASELINE")
    lines = original_text.splitlines(keepends=True)
    first, last = _function_span(original_text, "typed_sentence")
    eol = "\r\n" if b"\r\n" in original else "\n"
    output = "".join(lines[:first]) + replacement.replace("\n", eol) + "".join(lines[last:])
    return PatchPlan("PATCH_REQUIRED", original, output.encode("utf-8"), baseline, replacement)


def apply_patch(root: Path, plan: PatchPlan) -> None:
    """Install one reviewed function while preserving all other source bytes."""
    target = Path(root) / TARGET_RELATIVE
    if target.read_bytes() != plan.old_bytes:
        raise RuntimeError("R3R10_TARGET_CHANGED_AFTER_PREFLIGHT")
    if plan.status == "ALREADY_APPLIED":
        return
    if plan.status != "PATCH_REQUIRED":
        raise RuntimeError("R3R10_UNSUPPORTED_PATCH_STATUS")
    with tempfile.NamedTemporaryFile(
        mode="wb", dir=target.parent, prefix=".r3r10_", delete=False,
    ) as stream:
        staged = Path(stream.name)
        stream.write(plan.new_bytes)
    try:
        os.replace(staged, target)
    finally:
        if staged.exists():
            staged.unlink()
    if _normalized_function(target.read_text(encoding="utf-8")) != plan.replacement_function:
        raise RuntimeError("R3R10_POST_INSTALL_FUNCTION_MISMATCH")
