"""R57R1: repair the R57 preflight HEAD check, preserving all source pins."""
from __future__ import annotations

import argparse
import ast
import hashlib
import os
from pathlib import Path
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[1]
PACKAGE = Path(__file__).resolve().parent
TARGET = ROOT / "phase174_r3_r7_r57_narrative_source_cleanup" / "install.py"
EXPECTED_BEFORE_SHA256 = "f14d6930e236bdd97b85cc23a77f15fe17bc71cf7c087f1becd132ccf4b9ccf2"
EXPECTED_AFTER_SHA256 = "6a4df3c77edd7a0abd902d28782d12a63ebb6bd69f8c7d03e8efff601cd1e32e"
ORIGINAL = """    if git('rev-parse','HEAD') != HEAD:
        raise RuntimeError('unreviewed HEAD (R57 pinned to 0a5be29a)')
"""
REPLACEMENT = """    # The reviewed base commit may be followed by R56's own release commit.
    # A descendant is allowed ONLY when every reviewed target blob and each
    # local R56 rule/test source still matches its independently pinned hash.
    lineage = subprocess.run(
        ('git', 'merge-base', '--is-ancestor', HEAD, 'HEAD'),
        cwd=ROOT, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
    )
    if lineage.returncode != 0:
        raise RuntimeError('unreviewed HEAD lineage (R57 reviewed base not an ancestor): '
                           + lineage.stderr.decode('utf-8', 'replace'))
"""


def hash_data(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def patch_candidate(source: str) -> str:
    if source.count(ORIGINAL) != 1:
        raise ValueError("R57 HEAD guard has changed; no unreviewed patch permitted")
    after = source.replace(ORIGINAL, REPLACEMENT, 1)
    ast.parse(after)
    return after


def review() -> tuple[bytes, bytes, bool]:
    """Require a reviewed R57 file and rerun its complete strict source review.

    The altered R57 review still requires develop, no staged changes,
    exact Git blob pins for 3 renderer files, reviewed R56 rule/test hashes,
    and an unambiguous AST patch for each target. Only the HEAD criterion is
    broadened from exact equality to descendant-of-reviewed-base.
    """
    if not TARGET.is_file():
        raise RuntimeError("R57 original installer not found: " + str(TARGET))
    raw = TARGET.read_bytes()
    digest = hash_data(raw)
    if digest == EXPECTED_BEFORE_SHA256:
        text = raw.decode("utf-8")
        patched = patch_candidate(text).encode("utf-8")
        if hash_data(patched) != EXPECTED_AFTER_SHA256:
            raise RuntimeError("R57 patched installer failed reviewed SHA-256 pin")
        needs_patch = True
    elif digest == EXPECTED_AFTER_SHA256:
        patched = raw
        needs_patch = False
    else:
        raise RuntimeError("unreviewed R57 install.py: " + digest)
    if not (ROOT / ".git").exists():
        raise RuntimeError("extract directly into the Git repository root")
    scope = {"__name__": "_r57r1_reviewed_preflight", "__file__": str(TARGET)}
    exec(compile(patched.decode("utf-8"), str(TARGET), "exec"), scope)
    if scope["ROOT"].resolve() != ROOT.resolve():
        raise RuntimeError("R57 repository root mismatch")
    # R57's existing pins and staged-file guard are not waived.
    scope["review"](True)
    return raw, patched, needs_patch


def run(dry_run: bool) -> None:
    before, after, needs_patch = review()
    print("PHASE174_R57R1_SOURCE_GUARD=PASS")
    print("PHASE174_R57R1_OLD_INSTALL_SHA256=" + EXPECTED_BEFORE_SHA256)
    print("PHASE174_R57R1_NEW_INSTALL_SHA256=" + EXPECTED_AFTER_SHA256)
    print("PHASE174_R57R1_NEEDS_PATCH=" + str(needs_patch))
    print("PHASE174_R57R1_NEW_GIVEN=0")
    print("PHASE174_R57R1_NEW_MATH_RULES=0")
    if dry_run:
        print("PHASE174_R57R1_GATE=PASS_PREFLIGHT_ONLY")
        return
    if needs_patch:
        descriptor, temporary_name = tempfile.mkstemp(
            prefix=".r57r1_", suffix=".tmp", dir=str(TARGET.parent)
        )
        try:
            with os.fdopen(descriptor, "wb") as temp:
                temp.write(after)
            if TARGET.read_bytes() != before:
                raise RuntimeError("R57 installer changed during guarded install")
            os.replace(temporary_name, TARGET)
        finally:
            if os.path.exists(temporary_name):
                os.unlink(temporary_name)
    if hash_data(TARGET.read_bytes()) != EXPECTED_AFTER_SHA256:
        raise RuntimeError("R57 HEAD-lineage correction not applied")
    print("PHASE174_R57R1_GATE=PASS_R57R1_HEAD_LINEAGE_GUARD_PATCHED")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    run(args.dry_run)
    print("(END)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
