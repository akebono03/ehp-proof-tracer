"""Verify the previously applied common-renderer patch without applying it again.

The R3R1 implementation succeeded before pytest collection failed.  This
module verifies the exact reviewed function bodies and module imports while
allowing unrelated, non-target local changes.  It never edits production code.
"""
from __future__ import annotations

import hashlib
from pathlib import Path

from phase174_r3_r6_r3_common_narrative import patch as original_patch
from phase174_r3_r6_r3r1_scoped_guard_fix import patch as scoped_patch

ROOT = Path(__file__).resolve().parents[1]
SOURCE_SHA256 = {
    "phase174_r3_r6_r3_common_narrative/patch.py": (
        "6b79153c208724c179ae6c57fea2fb79507875d3c22f09dc822f25272a1fe01b"
    ),
    "phase174_r3_r6_r3_common_narrative/projection.py": (
        "28f629b1b163ecd55402f0e4d3a71b1d0640b029c59c8a739b5800e3741af995"
    ),
}


def inspect_installed_renderer(root: Path = ROOT) -> tuple[str, ...]:
    """Reject unreviewed target-function/import changes; perform no writes."""
    if not isinstance(root, Path):
        raise TypeError("root must be a Path")
    for relative, expected_hash in SOURCE_SHA256.items():
        source_path = root / relative
        if not source_path.is_file():
            raise ValueError("Missing original reviewed source: " + relative)
        observed_hash = hashlib.sha256(source_path.read_bytes()).hexdigest()
        if observed_hash != expected_hash:
            raise ValueError("Original source has unreviewed changes: " + relative)

    verified = []
    for path, function_name, transform in scoped_patch.TARGETS:
        original_bytes = scoped_patch.git_head_file(root, path)
        if scoped_patch.git_blob_sha(original_bytes) != original_patch.REVIEWED_BLOBS[path]:
            raise ValueError("Unreviewed Git HEAD source: " + path)
        baseline = scoped_patch.normalize_text(original_bytes)
        expected = transform(baseline)
        local_path = root / path
        if not local_path.is_file():
            raise ValueError("Missing applied source: " + path)
        observed = scoped_patch.normalize_text(local_path.read_bytes())
        expected_ast, expected_imports = scoped_patch.statement_ast(
            expected, function_name
        )
        observed_ast, observed_imports = scoped_patch.statement_ast(
            observed, function_name
        )
        if observed_ast != expected_ast or observed_imports != expected_imports:
            raise ValueError(
                "Applied renderer differs from reviewed R3R1 transformation: " + path
            )
        verified.append(path)
    return tuple(verified)


def main() -> int:
    verified = inspect_installed_renderer()
    print("PHASE174_R3R6R3R2_INSTALLED_RENDERER_GUARD=PASS")
    print("PHASE174_R3R6R3R2_VERIFIED_TARGETS=" + str(len(verified)))
    print("PHASE174_R3R6R3R2_PRODUCTION_WRITES=0")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
