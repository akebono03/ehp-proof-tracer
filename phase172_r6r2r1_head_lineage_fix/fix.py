"""Guarded R6R2 head-lineage correction; then reuse the original doc runner.

No mathematical proof, Renderer, source citations, or Phase 172 full test gate is
changed or run. On failure the previously supplied installer is restored.
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import os
from pathlib import Path
import subprocess
import sys
import tempfile

PACKAGE = Path(__file__).resolve().parent
ROOT = PACKAGE.parent
TARGET = ROOT / "phase172_r6r2_document_closeout" / "install.py"
PAYLOAD = PACKAGE / "payload" / "install.py"
ORIGINAL_SHA256 = "457a1e68d0c35592293946933de3d0f32f8214ae8cde952a7783751997775d4f"
CORRECTED_SHA256 = "83cd837d58b8204347c5cecbc3b1c33f182e4d85dab7f1d3020231c43d00a281"
R6_REPORT = "phase172_r6_20261031_144642_024616Z"


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def command(*args: str, timeout: int = 120) -> subprocess.CompletedProcess[str]:
    return subprocess.run(args, cwd=ROOT, check=False, stdout=subprocess.PIPE,
                          stderr=subprocess.PIPE, text=True, encoding="utf-8",
                          errors="replace", timeout=timeout)


def run_checked(*args: str, timeout: int = 120) -> str:
    result = command(*args, timeout=timeout)
    output = result.stdout + "\n" + result.stderr
    print(output, end="\n" if not output.endswith("\n") else "", flush=True)
    if result.returncode:
        raise RuntimeError(f"command failed ({result.returncode}): {args!r}")
    return output


def candidate_module():
    """Import complete corrected source for preflight without installing it."""
    spec = importlib.util.spec_from_file_location(
        "phase172_r6r2_document_closeout._reviewed_candidate", PAYLOAD,
    )
    if spec is None or spec.loader is None:
        raise RuntimeError("corrected installer cannot be loaded")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    module.ROOT = ROOT
    return module


def checked_payload() -> tuple[bytes, bytes]:
    if not TARGET.is_file() or not PAYLOAD.is_file():
        raise RuntimeError("original or corrected installer file is missing")
    old, revised = TARGET.read_bytes(), PAYLOAD.read_bytes()
    if digest(old) != ORIGINAL_SHA256:
        raise RuntimeError("installer does not match reviewed original; no changes")
    if digest(revised) != CORRECTED_SHA256:
        raise RuntimeError("corrected payload does not match reviewed bytes")
    return old, revised


def atomic_write(target: Path, data: bytes) -> None:
    """Replace complete source, never a fragment; preserve restoration bytes."""
    with tempfile.NamedTemporaryFile(
        mode="wb", dir=target.parent, delete=False,
        prefix=".phase172_r6r2r1_", suffix=".tmp",
    ) as stream:
        stream.write(data)
        temp = Path(stream.name)
    try:
        os.replace(temp, target)
    finally:
        temp.unlink(missing_ok=True)


def report_dir() -> Path:
    appdata = Path(os.environ.get("LOCALAPPDATA") or Path.home())
    return appdata / "EHPProofTracerRecovery" / R6_REPORT


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--apply", action="store_true")
    args = parser.parse_args()
    if args.dry_run == args.apply:
        parser.error("select exactly one of --dry-run and --apply")
    original, revised = checked_payload()
    candidate = candidate_module()
    state = candidate.preflight(report_dir())
    print("PHASE172_R6R2R1_BRANCH=" + state["branch"], flush=True)
    print("PHASE172_R6R2R1_HEAD=" + state["head"], flush=True)
    print("PHASE172_R6R2R1_R6_AUDIT_FILES=" + state["r6_audit_additions"], flush=True)
    print("PHASE172_R6R2R1_REVIEWED_R6_EVIDENCE=PASS", flush=True)
    print("PHASE172_R6R2R1_PAYLOAD_GUARD=PASS", flush=True)
    if args.dry_run:
        print("PHASE172_R6R2R1_SOURCE_CHANGES=0", flush=True)
        print("PHASE172_R6R2R1_DRY_RUN=PASS", flush=True)
        return 0
    atomic_write(TARGET, revised)
    try:
        if digest(TARGET.read_bytes()) != CORRECTED_SHA256:
            raise RuntimeError("installer replacement not byte-for-byte exact")
        run_checked(
            sys.executable, "-B", "-m", "pytest", "-q", "--tb=short",
            "-p", "no:cacheprovider",
            "phase172_r6r2r1_head_lineage_fix/tests/test_fix.py",
            timeout=120,
        )
        print("PHASE172_R6R2R1_FOCUSED_TESTS=PASS", flush=True)
        # The original guarded full-document installer writes full replacement
        # documents and its output backup; it runs only document-only pytest.
        run_checked(
            sys.executable, "-B", "-m",
            "phase172_r6r2_document_closeout.install", "--apply",
            timeout=180,
        )
    except BaseException:
        atomic_write(TARGET, original)
        if digest(TARGET.read_bytes()) != ORIGINAL_SHA256:
            raise RuntimeError("unable to restore original installer after failure")
        print("PHASE172_R6R2R1_RESTORED_INSTALLER=PASS", flush=True)
        raise
    print("PHASE172_R6R2R1_FULL_SUITE_EXECUTED=NO", flush=True)
    print("PHASE172_R6R2R1_RESULT=PASS_DOCUMENT_CLOSEOUT_CORRECTED", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
