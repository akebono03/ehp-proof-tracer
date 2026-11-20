"""Guarded installer: edit exactly two existing full function bodies via anchors."""
from __future__ import annotations

import argparse
import hashlib
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
TARGET = ROOT / "phase165_r52_r9_shared_math.py"
EXPECTED_BLOB = "f276170b3a3832ee9a9489becfbc5bbf2120727b"
SOURCE_ANCHOR = "        sources = sources + (build_cited_511_source(),)\n"
SOURCE_ADD = """        # Phase 176 R3R16: cited particular clause, not a direct image GIVEN.
        from phase175_r3r9_lemma57_explicit_public.source import (
            build_explicit_lemma57_source,
        )
        sources = sources + (
            build_explicit_lemma57_source(Path(__file__).resolve().parent),
        )
"""
PROVIDER_ANCHOR = """    # Phase 175 R4R12R13R4: retain H=0 as a verified intermediate ProofStep.
"""
PROVIDER_ADD = """    # Phase 176 R3R16: source-screened Lemma 5.7 and generic typed
    # right-composition zero-image inference; both remain open DFS subgoals.
    from phase176_r3r16_public_connection.provider import (
        build_public_lemma57_right_provider,
    )
    extra_providers = (
        build_public_lemma57_right_provider(bridge),
    ) + tuple(extra_providers)
"""


def git(*args: str) -> str:
    p = subprocess.run(("git",) + args, cwd=ROOT, text=True,
                       encoding="utf-8", errors="replace", capture_output=True)
    if p.returncode:
        raise RuntimeError("git " + " ".join(args) + ": " + p.stderr.strip())
    return p.stdout.strip()


def preflight() -> tuple[str, str]:
    if Path(git("rev-parse", "--show-toplevel")).resolve() != ROOT.resolve():
        raise RuntimeError("WRONG_REPO")
    if git("branch", "--show-current") != "develop":
        raise RuntimeError("DEVELOP_REQUIRED")
    old = TARGET.read_bytes().decode("utf-8")
    normalized = old.replace("\r\n", "\n")
    if SOURCE_ADD in normalized and PROVIDER_ADD in normalized:
        return old, "ALREADY_INSTALLED"
    if SOURCE_ADD in normalized or PROVIDER_ADD in normalized:
        raise RuntimeError("PARTIAL_INSTALLATION")
    blob = git("hash-object", "--", str(TARGET.relative_to(ROOT)))
    if blob != EXPECTED_BLOB:
        raise RuntimeError("SOURCE_BLOB_DRIFT: " + blob)
    for label, anchor in (("source", SOURCE_ANCHOR), ("provider", PROVIDER_ANCHOR)):
        if normalized.count(anchor) != 1:
            raise RuntimeError("ANCHOR_DRIFT_" + label)
    if "def build_shared_typed_bridge(" not in old or "def shared_expansion_provider(" not in old:
        raise RuntimeError("FUNCTIONS_MISSING")
    return old, "READY"


def install(dry_run: bool) -> str:
    original, status = preflight()
    if dry_run or status == "ALREADY_INSTALLED":
        return status
    newline = "\r\n" if "\r\n" in original else "\n"
    updated = original.replace("\r\n", "\n").replace(SOURCE_ANCHOR, SOURCE_ANCHOR + SOURCE_ADD)
    updated = updated.replace(PROVIDER_ANCHOR, PROVIDER_ADD + PROVIDER_ANCHOR)
    if newline != "\n":
        updated = updated.replace("\n", newline)
    compile(updated, str(TARGET), "exec")
    TARGET.write_bytes(updated.encode("utf-8"))
    return "INSTALLED"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    try:
        status = install(args.dry_run)
        print("PHASE176_R3R16_INSTALL=" + status)
        print("PHASE176_R3R16_NEW_DIRECT_GROUP_GIVEN=0")
        print("PHASE176_R3R16_FULL_PYTEST=NOT_RUN")
        return 0
    except Exception as exc:
        print("PHASE176_R3R16_INSTALL_ERROR=" + str(exc), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
