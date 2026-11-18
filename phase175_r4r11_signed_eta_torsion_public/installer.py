"""Pinned full-function installation of the R4R11 shared inference provider.

Only shared_expansion_provider() is modified. The full replacement is
always exported for review, even on DryRun. No module import changes.
"""
from __future__ import annotations

import ast
from hashlib import sha1
import os
from pathlib import Path
import subprocess
import tempfile

TARGET = Path("phase165_r52_r9_shared_math.py")
BASE_WORKING_BLOB = "900d670dff839d484d14dccb37fb79471b39902e"
REVIEWED_COMMITTED_BLOBS = (
    "df4e0f834e9bc321f338ec10b363c79d82623457",
    BASE_WORKING_BLOB,
)
FUNCTION = "shared_expansion_provider"
ANCHOR = '''    extra_providers = (build_cited_58_prop25_provider(bridge),) + tuple(extra_providers)
'''
ADDITION = '''    # Phase 175 R4R11: signed two-torsion normalization is conditional.
    # It requires verified Prop 2.5, order-two and eta-family premises.
    from phase175_r4r11_signed_eta_torsion_public.provider import (
        build_signed_eta_torsion_provider,
    )
    extra_providers = (build_signed_eta_torsion_provider(bridge),) + tuple(extra_providers)
'''


def git(root: Path, *args: str) -> str:
    result = subprocess.run(
        ["git", *args], cwd=root, capture_output=True,
        encoding="utf-8", errors="replace", text=True, check=False,
    )
    if result.returncode:
        raise RuntimeError("R4R11_GIT_ERROR: " + " ".join(args) + ": " + result.stderr)
    return result.stdout.strip()


def git_blob_sha(value: bytes) -> str:
    return sha1(b"blob " + str(len(value)).encode("ascii") + b"\x00" + value).hexdigest()


def function_replacement(original: str) -> tuple[str, str, str]:
    """Return whole module and full function, refusing unreviewed text."""
    syntax = ast.parse(original)
    functions = [node for node in syntax.body if isinstance(node, ast.FunctionDef)
                 and node.name == FUNCTION]
    if len(functions) != 1:
        raise RuntimeError("R4R11_FUNCTION_NOT_UNIQUE")
    fn = functions[0]
    lines = original.splitlines(keepends=True)
    before = "".join(lines[fn.lineno - 1:fn.end_lineno])
    if before.count(ANCHOR) != 1:
        raise RuntimeError("R4R11_ANCHOR_CHANGED")
    if before.count(ADDITION) > 1:
        raise RuntimeError("R4R11_DUPLICATED_INSERTION")
    original_without_addition = original
    if ADDITION in before:
        original_without_addition = original.replace(ADDITION, "", 1)
    if git_blob_sha(original_without_addition.encode("utf-8")) != BASE_WORKING_BLOB:
        raise RuntimeError("R4R11_UNREVIEWED_BASE_SOURCE")
    after_function = before if ADDITION in before else before.replace(
        ANCHOR, ANCHOR + ADDITION, 1,
    )
    updated = "".join(lines[:fn.lineno - 1]) + after_function + "".join(lines[fn.end_lineno:])
    ast.parse(updated)
    return updated, after_function, original_without_addition


def plan(root: Path) -> tuple[Path, bytes, bytes, str]:
    """Work with both reviewed R4R10 HEADs and LF/CRLF checkouts."""
    path = root / TARGET
    if not path.is_file():
        raise RuntimeError("R4R11_PRODUCTION_FILE_MISSING")
    committed = git(root, "rev-parse", "HEAD:" + TARGET.as_posix())
    if committed not in REVIEWED_COMMITTED_BLOBS:
        raise RuntimeError("R4R11_UNREVIEWED_COMMITTED_PRODUCTION")
    current = path.read_bytes()
    normalized = current.replace(b"\r\n", b"\n").decode("utf-8")
    new_content, whole_function, _ = function_replacement(normalized)
    eol = b"\r\n" if b"\r\n" in current else b"\n"
    new_data = new_content.encode("utf-8")
    if eol == b"\r\n":
        new_data = new_data.replace(b"\n", b"\r\n")
    return path, current, new_data, whole_function


def install(root: Path, *, dry_run: bool, output: Path) -> dict[str, object]:
    path, before, after, full_function = plan(root)
    output.mkdir(parents=True, exist_ok=True)
    (output / "shared_expansion_provider_FULL_AFTER.py").write_text(
        full_function, encoding="utf-8",
    )
    (output / "phase165_r52_r9_shared_math_FULL_AFTER.py").write_bytes(after)
    if before != after and not dry_run:
        descriptor, temp = tempfile.mkstemp(prefix="r4r11_", suffix=".py", dir=path.parent)
        try:
            with os.fdopen(descriptor, "wb") as stream:
                stream.write(after)
            os.replace(temp, path)
        finally:
            if os.path.exists(temp):
                os.unlink(temp)
    return {
        "production_path": TARGET.as_posix(),
        "patch_required": before != after,
        "patch_applied": before != after and not dry_run,
        "after_git_blob": git_blob_sha(after.replace(b"\r\n", b"\n")),
        "full_function_exported": True,
    }
