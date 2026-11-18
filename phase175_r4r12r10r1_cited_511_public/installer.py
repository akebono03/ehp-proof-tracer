"""Only append citation registration/provider to two entire shared functions."""
from __future__ import annotations

import ast
import os
from pathlib import Path
import subprocess
import tempfile

TARGET = Path("phase165_r52_r9_shared_math.py")
COMMITTED_BLOB = "81d234c31e1af176457a35556045aed78d30b343"
REVIEWED_R9_COMMITTED_BLOB = "83f278ec98512a763cdfba2552c70f972b169eac"
BRIDGE_NAME = "build_shared_typed_bridge"
PROVIDER_NAME = "shared_expansion_provider"
BRIDGE_ANCHOR = '''        sources = sources + (build_cited_58_prop25_sources(),)
'''
BRIDGE_INSERT = '''        # Phase 175 R4R12R10R1: cite Toda (5.11) without re-proving it.
        from phase175_r4r12r10r1_cited_511_public.source import (
            build_cited_511_source,
        )
        sources = sources + (build_cited_511_source(),)
'''
PROVIDER_ANCHOR = '''    # Phase 175 R4R10: screened literature claims produce only open subgoals.
'''
PROVIDER_INSERT = '''    # Phase 175 R4R12R10R1: cited (5.11) becomes an inferred typed equality.
    from phase175_r4r12r10r1_cited_511_public.provider import (
        build_cited_511_provider,
    )
    extra_providers = (build_cited_511_provider(bridge),) + tuple(extra_providers)
'''


def git(root: Path, *args: str) -> str:
    process = subprocess.run(("git",) + args, cwd=root, capture_output=True,
                             text=True, encoding="utf-8", errors="replace")
    if process.returncode:
        raise RuntimeError("R10R1_GIT_FAILURE: " + process.stderr.strip())
    return process.stdout.strip()


def update_function(module: str, name: str, anchor: str, addition: str) -> tuple[str, str]:
    tree = ast.parse(module)
    nodes = [node for node in tree.body if isinstance(node, ast.FunctionDef) and node.name == name]
    if len(nodes) != 1:
        raise RuntimeError("R10R1_FUNCTION_NOT_UNIQUE " + name)
    node = nodes[0]
    lines = module.splitlines(keepends=True)
    before = "".join(lines[node.lineno - 1:node.end_lineno])
    if before.count(anchor) != 1 or before.count(addition) > 1:
        raise RuntimeError("R10R1_UNREVIEWED_FUNCTION " + name)
    after = before if addition in before else before.replace(anchor, anchor + addition, 1)
    updated = "".join(lines[:node.lineno - 1]) + after + "".join(lines[node.end_lineno:])
    ast.parse(updated)
    return updated, after


def plan(root: Path) -> tuple[bytes, bytes, dict[str, str]]:
    path = root / TARGET
    original = path.read_bytes()
    if b"\n" in original.replace(b"\r\n", b"") and b"\r\n" in original:
        raise RuntimeError("R10R1_MIXED_EOL_REQUIRES_REVIEW")
    committed = git(root, "rev-parse", "HEAD:" + TARGET.as_posix())
    if committed not in (COMMITTED_BLOB, REVIEWED_R9_COMMITTED_BLOB):
        raise RuntimeError("R10R1_UNREVIEWED_COMMITTED_PRODUCTION")
    normalized = original.replace(b"\r\n", b"\n").decode("utf-8")
    from phase175_r4r12r9_delta_generator_image_bridge.installer import replacement as r9_replacement
    r9_expected, _ = r9_replacement(normalized)
    if normalized != r9_expected:
        raise RuntimeError("R10R1_R9_NOT_INSTALLED")
    updated, bridge = update_function(normalized, BRIDGE_NAME, BRIDGE_ANCHOR, BRIDGE_INSERT)
    updated, provider = update_function(updated, PROVIDER_NAME, PROVIDER_ANCHOR, PROVIDER_INSERT)
    eol = b"\r\n" if b"\r\n" in original else b"\n"
    new = updated.encode("utf-8").replace(b"\n", eol) if eol == b"\r\n" else updated.encode("utf-8")
    return original, new, {BRIDGE_NAME: bridge, PROVIDER_NAME: provider}


def install(root: Path, *, dry_run: bool, output: Path) -> dict[str, object]:
    before, after, functions = plan(root)
    output.mkdir(parents=True, exist_ok=True)
    for name, function in functions.items():
        (output / (name + "_FULL_AFTER.py")).write_text(function, encoding="utf-8")
    (output / "phase165_r52_r9_shared_math_FULL_AFTER.py").write_bytes(after)
    if not dry_run and before != after:
        fd, name = tempfile.mkstemp(prefix="r10r1_", suffix=".py", dir=root)
        try:
            with os.fdopen(fd, "wb") as stream:
                stream.write(after)
            os.replace(name, root / TARGET)
        finally:
            if os.path.exists(name):
                os.unlink(name)
    return {"target": str(TARGET), "patch_required": before != after,
            "patch_applied": not dry_run and before != after,
            "whole_functions_exported": sorted(functions)}
