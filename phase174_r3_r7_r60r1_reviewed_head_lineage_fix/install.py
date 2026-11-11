"""R60R1: exact one-line reviewed HEAD correction for the R60 read-only audit.

The six R60 production/audit source pins remain unchanged. In particular, no
Source Guard, reference projection, proof result, renderer, or inference rule
is bypassed or edited. The real install patches only the already-extracted
R60 audit module after checking original bytes and the reviewed Git commit.
"""
from __future__ import annotations

import argparse
from hashlib import sha256
import os
from pathlib import Path
import subprocess
import tempfile


PACKAGE = "phase174_r3_r7_r60r1_reviewed_head_lineage_fix"
TARGET = "phase174_r3_r7_r60_reference_ownership_audit/audit.py"
REVIEWED_HEAD = "17b96a63c1ee400d587c14c785c4c1e697334206"
PREVIOUS_HEAD = "82d725d8649cd6307c2abd67024e3ef4f3cddfe2"
BEFORE_SHA256 = "5409b0ab6f85a447db44c68c2b0c65d5fd2bb34453aa6473441f7ff01bc7e9dc"
AFTER_SHA256 = "1b2e51d4925b8d9cf8f559f9277883c95e9430f93a4417df450aa582906f05f0"
OLD_LINE = 'REVIEWED_HEAD = "' + PREVIOUS_HEAD + '"'
NEW_LINE = 'REVIEWED_HEAD = "' + REVIEWED_HEAD + '"'
EXPECTED_BLOB_PINS = {
    "phase168_r3_3_proof_narrative_model.py": "6a298aae5f7cbc8ec1be5b02a931b6b7a72e9d52",
    "phase168_r3_12_body_binding.py": "ad8797c141216e410e81bafae284507f7797c3e4",
    "phase168_r3_5_model_renderer.py": "cb6989871ea4ad3964f714bfc5ada2a5099424a0",
    "phase168_r3_37c_reference_projection.py": "3800dc72a2e09808f15b8ee78ae76d4d39c2eede",
    "phase174_r3_r7_r56_cyclic_generator_bridge/audit.py": "868e4dfad4d97bb3e5d5da462260bab3759d4af8",
    "phase174_r3_r7_r57_narrative_source_cleanup/audit.py": "7cc7e7ac7f63c4bf28142c1d84c5d8ddd249cc8a",
}


def sha256_bytes(data: bytes) -> str:
    return sha256(data).hexdigest()


def checked_patch(original: bytes) -> tuple[bytes, bool]:
    """Only the exact reviewed original or the exact already-applied file qualifies."""
    normalized = original.replace(b"\r\n", b"\n")
    digest = sha256_bytes(normalized)
    if digest == AFTER_SHA256:
        if normalized.count(NEW_LINE.encode("ascii")) != 1:
            raise RuntimeError("R60R1 patched HEAD declaration is ambiguous")
        return original, False
    if digest != BEFORE_SHA256:
        raise RuntimeError("R60R1_ORIGINAL_AUDIT_PIN_MISMATCH")
    before = OLD_LINE.encode("ascii")
    after = NEW_LINE.encode("ascii")
    if original.count(before) != 1 or after in original:
        raise RuntimeError("R60R1 reviewed-head anchor missing or duplicated")
    patched = original.replace(before, after)
    if sha256_bytes(patched.replace(b"\r\n", b"\n")) != AFTER_SHA256:
        raise RuntimeError("R60R1 patched content differs from the reviewed full file")
    return patched, True


def git_head(root: Path) -> str:
    result = subprocess.run(
        ("git", "rev-parse", "HEAD"), cwd=root,
        capture_output=True, text=True, check=False,
    )
    if result.returncode != 0:
        raise RuntimeError("R60R1 cannot read local Git HEAD")
    return result.stdout.strip()


def preflight(root: Path) -> tuple[Path, bytes, bool]:
    """Fail closed unless Git HEAD and all six reviewed files match."""
    head = git_head(root)
    if head != REVIEWED_HEAD:
        raise RuntimeError("R60R1_REVIEWED_HEAD_MISMATCH: " + head)
    from phase174_r3_r7_r60_reference_ownership_audit.audit import (
        PINS, source_guard,
    )
    if PINS != EXPECTED_BLOB_PINS:
        raise RuntimeError("R60R1 source pin registry changed")
    if len(source_guard(root)) != 6:
        raise RuntimeError("R60R1 six-source guard failed")
    path = root / TARGET
    if not path.is_file():
        raise RuntimeError("R60R1 original R60 ZIP must be extracted first")
    updated, needs_write = checked_patch(path.read_bytes())
    return path, updated, needs_write


def atomic_write(path: Path, data: bytes) -> None:
    """Replace only the validated audit file, leaving other files and Git untouched."""
    descriptor, name = tempfile.mkstemp(prefix=".r60r1_", dir=str(path.parent))
    try:
        with os.fdopen(descriptor, "wb") as stream:
            stream.write(data)
        os.chmod(name, path.stat().st_mode)
        os.replace(name, path)
    finally:
        if os.path.exists(name):
            os.unlink(name)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    opts = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    path, updated, needs_write = preflight(root)
    print("PHASE174_R60R1_SOURCE_GUARD=PASS")
    print("PHASE174_R60R1_SOURCE_PINS=6")
    print("PHASE174_R60R1_LOCAL_HEAD=" + REVIEWED_HEAD)
    print("PHASE174_R60R1_PATCH_REQUIRED=" + str(needs_write))
    if opts.dry_run:
        print("PHASE174_R60R1_GATE=PASS_R60R1_READ_ONLY_DRYRUN")
        print("(END)")
        return 0
    if needs_write:
        atomic_write(path, updated)
    final_bytes = path.read_bytes()
    if sha256_bytes(final_bytes.replace(b"\r\n", b"\n")) != AFTER_SHA256:
        raise RuntimeError("R60R1 final audit file SHA mismatch")
    print("PHASE174_R60R1_PATCH_STATUS=" + ("APPLIED" if needs_write else "ALREADY_APPLIED"))
    print("PHASE174_R60R1_PRODUCTION_CHANGES=0")
    print("PHASE174_R60R1_NEW_GIVEN=0")
    print("PHASE174_R60R1_NEW_MATHEMATICAL_RULES=0")
    print("PHASE174_R60R1_GATE=PASS_R60R1_REVIEWED_HEAD_PATCH")
    print("(END)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
