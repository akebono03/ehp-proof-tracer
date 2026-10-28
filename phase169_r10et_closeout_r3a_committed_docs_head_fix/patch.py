"""Exact-source, fail-closed R3-only audit patch."""
from __future__ import annotations

import hashlib
from pathlib import Path

TARGET = "phase169_r10et_closeout_r3_final_readonly_audit/audit.py"
OLD_SHA256 = "d3d3c9aba424a43ae6110abe093e2e095f00e56f45dc571793eb3e63c00ad2fd"
PREVIOUS_HEAD = "a759c12fbcc0a7fc64c578fcd8a4dd86ac94b3c5"
CURRENT_HEAD = "6e5d6bbed186dd4da706b54c308f94041a32e6d7"
REPLACEMENTS = (
    (
        'REVIEWED_HEAD = "' + PREVIOUS_HEAD + '"',
        'REVIEWED_HEAD = "' + CURRENT_HEAD + '"\nR2A_MANIFEST_HEAD = "' + PREVIOUS_HEAD + '"',
    ),
    (
        'manifest.get("head") != REVIEWED_HEAD',
        'manifest.get("head") != R2A_MANIFEST_HEAD',
    ),
    (
        '    if set(baseline[1].splitlines()) != set(DOCUMENT_BLOBS):\n'
        '        raise RuntimeError("Tracked unstaged changes must be exactly the five documents")',
        '    if baseline[1]:\n'
        '        raise RuntimeError("Tracked unstaged changes are not allowed after document commit")',
    ),
)

def patch_bytes(original: bytes) -> bytes:
    if hashlib.sha256(original).hexdigest() != OLD_SHA256:
        raise RuntimeError("Unreviewed R3 audit.py: refusing to overwrite")
    result = original.decode("utf-8")
    for before, after in REPLACEMENTS:
        if result.count(before) != 1:
            raise RuntimeError("R3 patch anchor missing or duplicated")
        result = result.replace(before, after, 1)
    updated = result.encode("utf-8")
    from ast import parse
    parse(result)
    return updated

def reviewed_patch(root: Path, package: Path) -> bytes:
    source = (root / TARGET).read_bytes()
    modified = patch_bytes(source)
    expected = (package / "reviewed_sources" / "r3_audit_AFTER_FULL.py").read_bytes()
    if modified != expected:
        raise RuntimeError("R3 full reviewed source does not match patch")
    return modified
