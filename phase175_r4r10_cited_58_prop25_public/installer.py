"""Pinned two-complete-function installation in the shared production path.

Never edits imports or unrelated functions. Writes a complete full-function
replacement to the report folder, allowing independent human inspection.
"""
from __future__ import annotations

import ast
from hashlib import sha1
import os
from pathlib import Path
import subprocess
import tempfile

TARGET = Path("phase165_r52_r9_shared_math.py")
EXPECTED_COMMITTED_BLOB = "df4e0f834e9bc321f338ec10b363c79d82623457"
BRIDGE_FUNCTION = "build_shared_typed_bridge"
PROVIDER_FUNCTION = "shared_expansion_provider"

BRIDGE_ANCHOR = '''        sources = sources + (
            build_cited_lower_delta_sources(Path(__file__).resolve().parent),
        )
'''
BRIDGE_ADDITION = '''        # Phase 175 R4R10: source-only (5.8) and universal Proposition 2.5.
        from phase175_r4r10_cited_58_prop25_public.source import (
            build_cited_58_prop25_sources,
        )
        sources = sources + (build_cited_58_prop25_sources(),)
'''
PROVIDER_ANCHOR = '''    if not isinstance(bridge, RegistryBridgeResult):
        raise TypeError("bridge must be RegistryBridgeResult")
'''
PROVIDER_ADDITION = '''    # Phase 175 R4R10: screened literature claims produce only open subgoals.
    from phase175_r4r10_cited_58_prop25_public.provider import (
        build_cited_58_prop25_provider,
    )
    extra_providers = (build_cited_58_prop25_provider(bridge),) + tuple(extra_providers)
'''


def git(root: Path, *args: str) -> str:
    result = subprocess.run(
        ["git", *args], cwd=root, capture_output=True,
        text=True, encoding="utf-8", errors="replace", check=False,
    )
    if result.returncode:
        raise RuntimeError("R4R10_GIT_FAILED: " + " ".join(args) + " " + result.stderr)
    return result.stdout.strip()


def git_blob_sha(data: bytes) -> str:
    return sha1(b"blob " + str(len(data)).encode("ascii") + b"\x00" + data).hexdigest()


def replace_full_function(
    original: str, function_name: str, anchor: str, addition: str,
) -> tuple[str, str]:
    """Replace one entire AST function; refuse moved anchors or duplicates."""
    tree = ast.parse(original)
    found = [node for node in tree.body
             if isinstance(node, ast.FunctionDef) and node.name == function_name]
    if len(found) != 1:
        raise RuntimeError("R4R10_FUNCTION_NOT_UNIQUE: " + function_name)
    fn = found[0]
    lines = original.splitlines(keepends=True)
    before = "".join(lines[fn.lineno - 1:fn.end_lineno])
    if addition in before:
        if before.count(addition) != 1:
            raise RuntimeError("R4R10_INSERTION_DUPLICATE: " + function_name)
        return original, before
    if before.count(anchor) != 1:
        raise RuntimeError("R4R10_ANCHOR_CHANGED: " + function_name)
    after = before.replace(anchor, anchor + addition, 1)
    updated = "".join(lines[:fn.lineno - 1]) + after + "".join(lines[fn.end_lineno:])
    ast.parse(updated)
    return updated, after


def plan(root: Path) -> tuple[Path, bytes, bytes, dict[str, str]]:
    """Compute the two full functions with Git pin and EOL preservation."""
    path = root / TARGET
    if not path.is_file():
        raise RuntimeError("R4R10_PRODUCTION_FILE_MISSING")
    if git(root, "rev-parse", "HEAD:" + TARGET.as_posix()) != EXPECTED_COMMITTED_BLOB:
        raise RuntimeError("R4R10_UNREVIEWED_PRODUCTION_COMMIT")
    current_bytes = path.read_bytes()
    normalized = current_bytes.replace(b"\r\n", b"\n")
    original = normalized.decode("utf-8")
    after_bridge, whole_bridge = replace_full_function(
        original, BRIDGE_FUNCTION, BRIDGE_ANCHOR, BRIDGE_ADDITION,
    )
    after_both, whole_provider = replace_full_function(
        after_bridge, PROVIDER_FUNCTION, PROVIDER_ANCHOR, PROVIDER_ADDITION,
    )
    eol = b"\r\n" if b"\r\n" in current_bytes else b"\n"
    result = after_both.encode("utf-8")
    if eol == b"\r\n":
        result = result.replace(b"\n", b"\r\n")
    # Only unchanged committed source or an exactly identical completed patch.
    if (git_blob_sha(normalized) != EXPECTED_COMMITTED_BLOB
            and current_bytes != result):
        raise RuntimeError("R4R10_UNREVIEWED_LOCAL_PRODUCTION_CHANGE")
    return path, current_bytes, result, {
        BRIDGE_FUNCTION: whole_bridge,
        PROVIDER_FUNCTION: whole_provider,
    }


def install(root: Path, *, dry_run: bool, output: Path) -> dict[str, object]:
    if not isinstance(root, Path) or not isinstance(output, Path):
        raise TypeError("root and output must be pathlib.Path")
    path, before, after, functions = plan(root)
    output.mkdir(parents=True, exist_ok=True)
    (output / "build_shared_typed_bridge_FULL_AFTER.py").write_text(
        functions[BRIDGE_FUNCTION], encoding="utf-8",
    )
    (output / "shared_expansion_provider_FULL_AFTER.py").write_text(
        functions[PROVIDER_FUNCTION], encoding="utf-8",
    )
    (output / "phase165_r52_r9_shared_math_FULL_AFTER.py").write_bytes(after)
    changed = before != after
    if not dry_run and changed:
        fd, temp_name = tempfile.mkstemp(prefix="r4r10_", suffix=".py", dir=path.parent)
        try:
            with os.fdopen(fd, "wb") as stream:
                stream.write(after)
            os.replace(temp_name, path)
        finally:
            if os.path.exists(temp_name):
                os.unlink(temp_name)
    return {
        "production_path": TARGET.as_posix(),
        "patch_required": changed,
        "patch_applied": changed and not dry_run,
        "after_git_blob": git_blob_sha(after),
        "two_full_functions_exported": True,
    }
