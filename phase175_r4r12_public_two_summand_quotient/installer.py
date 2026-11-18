"""Full-function, guarded R4R12 installation after verified R4R11 wiring.

No mathematical module is edited. Only shared_expansion_provider() changes.
The installer exports the complete updated function and complete updated file.
"""
from __future__ import annotations

import ast
from hashlib import sha1
import os
from pathlib import Path
import subprocess
import tempfile

from phase175_r4r11_signed_eta_torsion_public import installer as previous

TARGET = Path("phase165_r52_r9_shared_math.py")
HEAD = "344fc101fdfcce49ec80f867f80a0614d96c214e"
FUNCTION = "shared_expansion_provider"
ANCHOR = (
    "    extra_providers = (build_signed_eta_torsion_provider(bridge),) "
    "+ tuple(extra_providers)\n"
)
ADDITION = '''    # Phase 175 R4R12: propose the already-audited generic EHP quotient.
    # All six independent proof obligations remain mandatory.
    from phase175_r4r12_public_two_summand_quotient.provider import (
        build_public_two_summand_quotient_provider,
    )
    extra_providers = (
        build_public_two_summand_quotient_provider(proof_target=proof_target),
    ) + tuple(extra_providers)
'''


def git(root: Path, *args: str) -> str:
    result = subprocess.run(
        ["git", *args], cwd=root, capture_output=True,
        text=True, encoding="utf-8", errors="replace", check=False,
    )
    if result.returncode:
        raise RuntimeError("R4R12_GIT_ERROR: " + " ".join(args)
                           + ": " + result.stderr.strip())
    return result.stdout.strip()


def git_blob_sha(data: bytes) -> str:
    return sha1(b"blob " + str(len(data)).encode("ascii") + b"\x00" + data).hexdigest()


def function_replacement(original: str) -> tuple[str, str, str]:
    """Recheck the complete R4R11 module before changing a single function."""
    parsed = ast.parse(original)
    functions = [node for node in parsed.body
                 if isinstance(node, ast.FunctionDef) and node.name == FUNCTION]
    if len(functions) != 1:
        raise RuntimeError("R4R12_SHARED_FUNCTION_NOT_UNIQUE")
    fn = functions[0]
    lines = original.splitlines(keepends=True)
    before = "".join(lines[fn.lineno - 1:fn.end_lineno])
    if before.count(ANCHOR) != 1 or before.count(ADDITION) > 1:
        raise RuntimeError("R4R12_ANCHOR_OR_ADDITION_DRIFT")
    # Remove only our own exact addition; R4R11 validates ALL remaining code.
    baseline = original.replace(ADDITION, "", 1) if ADDITION in before else original
    validated, _, _ = previous.function_replacement(baseline)
    if validated != baseline:
        raise RuntimeError("R4R12_R4R11_NOT_INSTALLED")
    after_fn = before if ADDITION in before else before.replace(
        ANCHOR, ANCHOR + ADDITION, 1,
    )
    updated = "".join(lines[:fn.lineno - 1]) + after_fn + "".join(lines[fn.end_lineno:])
    ast.parse(updated)
    return updated, after_fn, baseline


def plan(root: Path) -> tuple[Path, bytes, bytes, str]:
    """Preserve the checked-out EOL style and refuse unreviewed committed code."""
    file = root / TARGET
    if not file.is_file():
        raise RuntimeError("R4R12_PRODUCTION_SOURCE_MISSING")
    if git(root, "rev-parse", "HEAD") != HEAD:
        raise RuntimeError("R4R12_UNREVIEWED_HEAD")
    if git(root, "rev-parse", "HEAD:" + TARGET.as_posix()) != '725d2227caa3544aad9288309231a8f7e33619f0':
        raise RuntimeError("R4R12_UNREVIEWED_BASE_PRODUCTION")
    original = file.read_bytes()
    normalized = original.replace(b"\r\n", b"\n").decode("utf-8")
    after, entire_fn, _ = function_replacement(normalized)
    payload = after.encode("utf-8")
    if b"\r\n" in original:
        payload = payload.replace(b"\n", b"\r\n")
    return file, original, payload, entire_fn


def install(root: Path, *, dry_run: bool, output: Path) -> dict[str, object]:
    file, before, after, whole_fn = plan(root)
    output.mkdir(parents=True, exist_ok=True)
    (output / "shared_expansion_provider_FULL_AFTER.py").write_text(
        whole_fn, encoding="utf-8",
    )
    (output / "phase165_r52_r9_shared_math_FULL_AFTER.py").write_bytes(after)
    if before != after and not dry_run:
        descriptor, temp_name = tempfile.mkstemp(prefix="r4r12_", suffix=".py", dir=file.parent)
        try:
            with os.fdopen(descriptor, "wb") as stream:
                stream.write(after)
            os.replace(temp_name, file)
        finally:
            if os.path.exists(temp_name):
                os.unlink(temp_name)
    return {
        "production_path": TARGET.as_posix(),
        "patch_required": before != after,
        "patch_applied": before != after and not dry_run,
        "after_git_blob": git_blob_sha(after.replace(b"\r\n", b"\n")),
        "full_function_exported": True,
        "complete_module_exported": True,
    }
