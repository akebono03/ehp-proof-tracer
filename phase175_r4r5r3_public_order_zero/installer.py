"""Pinned whole-function replacement for shared_expansion_provider only.

No regex-based partial edits or changes to the module-level imports.
The full replacement function is emitted to output/ on actual installation.
"""
from __future__ import annotations

import ast
from pathlib import Path
import subprocess
import tempfile

TARGET_RELATIVE = Path("phase165_r52_r9_shared_math.py")
TARGET_FUNCTION = "shared_expansion_provider"
PINNED_GIT_BLOB = "ee1efa2d91df479168b7b964d24e814e0f516449"
INSERTION = '''
    # Phase 175 R4R5R3: reusable finite-cyclic summand order-to-zero rule.
    # All proof steps are resolved by the ordinary citation/DB-prior gate.
    from phase175_r4r5r3_public_order_zero.provider import (
        build_public_order_zero_provider,
    )
    extra_providers = (
        build_public_order_zero_provider(
            bridge=bridge, proof_target=proof_target,
            prior_conclusions=prior_conclusions,
        ),
    ) + tuple(extra_providers)
'''
ANCHOR = '''    if not isinstance(prior_conclusions, tuple):
        raise TypeError("prior_conclusions must be a tuple")
'''


def git_blob(root: Path, reference: str) -> str:
    result = subprocess.run(
        ["git", "rev-parse", reference], cwd=root, text=True,
        capture_output=True, check=True,
    )
    return result.stdout.strip()


def function_replacement(original: str) -> tuple[str, str]:
    """Replace a complete AST-defined function while keeping other bytes.

    Both the existing and new source parse as Python. Reject unusual source
    shapes or multiple anchors rather than silently patching another function.
    """
    syntax = ast.parse(original)
    functions = [node for node in syntax.body if isinstance(node, ast.FunctionDef)
                 and node.name == TARGET_FUNCTION]
    if len(functions) != 1:
        raise RuntimeError("R4R5R3_FUNCTION_NOT_UNIQUE")
    function = functions[0]
    lines = original.splitlines(keepends=True)
    start, end = function.lineno - 1, function.end_lineno
    before = "".join(lines[start:end])
    if before.count(ANCHOR) != 1 or INSERTION.strip() in before:
        raise RuntimeError("R4R5R3_INSERTION_ANCHOR_CHANGED")
    after = before.replace(ANCHOR, ANCHOR + INSERTION, 1)
    whole = "".join(lines[:start]) + after + "".join(lines[end:])
    ast.parse(whole)
    return whole, after


def plan(root: Path) -> tuple[Path, bytes, bytes, str]:
    """Return a full-file, full-function replacement guarded by Git blob SHA."""
    path = root / TARGET_RELATIVE
    data = path.read_bytes()
    if b"\r\n" in data:
        normalized = data.decode("utf-8").replace("\r\n", "\n")
        eol = "\r\n"
    else:
        normalized = data.decode("utf-8")
        eol = "\n"
    committed = git_blob(root, "HEAD:" + TARGET_RELATIVE.as_posix())
    if committed != PINNED_GIT_BLOB:
        raise RuntimeError("R4R5R3_PRODUCTION_SOURCE_BLOB_CHANGED")
    # --path applies Git's checkout clean filters (including Windows CRLF).
    working = subprocess.run(
        ["git", "hash-object", "--path", TARGET_RELATIVE.as_posix(), str(path)],
        cwd=root, text=True, check=True, capture_output=True,
    ).stdout.strip()
    if working != PINNED_GIT_BLOB:
        raise RuntimeError("R4R5R3_PRODUCTION_SOURCE_BLOB_CHANGED")
    replaced, full_function = function_replacement(normalized)
    return path, data, replaced.replace("\n", eol).encode("utf-8"), full_function


def install(root: Path, *, dry_run: bool, output: Path) -> dict[str, object]:
    path, old, new, full_function = plan(root)
    output.mkdir(parents=True, exist_ok=True)
    # Whole function, not a diff. This is the exact post-install replacement.
    (output / "shared_expansion_provider_FULL.py").write_text(
        full_function, encoding="utf-8",
    )
    if not dry_run:
        with tempfile.NamedTemporaryFile(mode="wb", delete=False,
                                         dir=path.parent, prefix=".r4r5r3_") as stream:
            temporary = Path(stream.name)
            stream.write(new)
        try:
            temporary.replace(path)
        finally:
            temporary.unlink(missing_ok=True)
        if path.read_bytes() != new:
            raise RuntimeError("R4R5R3_REPLACEMENT_MISMATCH")
    return {
        "target": TARGET_RELATIVE.as_posix(),
        "class_changes": [],
        "changed_function": TARGET_FUNCTION,
        "module_imports_changed": False,
        "other_functions_unchanged": True,
        "dry_run": dry_run,
        "full_replacement_path": str(output / "shared_expansion_provider_FULL.py"),
        "original_size": len(old),
        "replacement_size": len(new),
    }
