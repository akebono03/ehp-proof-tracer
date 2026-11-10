"""Fail-closed correction of the R56 audit report directory Path expression.

Only the untracked R56 audit module is changed. All proof rules, proof search,
registered sources, and common rendering code are retained exactly.
"""
from __future__ import annotations

import argparse
import ast
import hashlib
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
AUDIT_FILE = ROOT / "phase174_r3_r7_r56_cyclic_generator_bridge" / "audit.py"
BASELINE_SHA256 = "240e88a7a404f0ecc5640fe1b3155fd55e6ac2c148f2c5760986afaa6d5940e3"
PATCHED_SHA256 = "e4c37f2ec99847682a2df52dfdf295ea6b2a3a18d2c01e482ddfc61d9a4124f5"
OLD_LINE = '    destination /= "EHPProofTracerAudit" / "phase174_r3_r7_r56"'
NEW_LINE = '    destination /= Path("EHPProofTracerAudit") / "phase174_r3_r7_r56"'


def _read_lf(raw: bytes) -> tuple[str, str]:
    """Allow LF or uniform CRLF, but reject mixed, partial, and BOM edits."""
    if raw.startswith(b"\xef\xbb\xbf") or b"\r" in raw.replace(b"\r\n", b""):
        raise RuntimeError("unreviewed encoding or CR-only line ending in R56 audit")
    if b"\r\n" in raw and raw.count(b"\n") != raw.count(b"\r\n"):
        raise RuntimeError("mixed line endings in R56 audit")
    style = "\r\n" if b"\r\n" in raw else "\n"
    return raw.decode("utf-8").replace("\r\n", "\n"), style


def _sha(normalized_text: str) -> str:
    return hashlib.sha256(normalized_text.encode("utf-8")).hexdigest()


def patch_source(source: str) -> str:
    """Replace only the verified invalid Path expression, never audit logic."""
    if source.count(OLD_LINE) != 1 or NEW_LINE in source:
        raise RuntimeError("R56 audit Path patch anchor is absent or ambiguous")
    updated = source.replace(OLD_LINE, NEW_LINE, 1)
    ast.parse(updated, filename=str(AUDIT_FILE))
    if _sha(source) != BASELINE_SHA256 or _sha(updated) != PATCHED_SHA256:
        raise RuntimeError("R56 audit content differs from reviewed ZIP baseline")
    return updated


def review() -> dict[str, object]:
    """Reuse R56 production Source Guard and verify the full original audit."""
    from phase174_r3_r7_r56_cyclic_generator_bridge.install import review as review_r56

    base = review_r56()
    if base["source_guard"] != "PASS":
        raise RuntimeError("R56 production Source Guard did not pass")
    if not AUDIT_FILE.is_file():
        raise RuntimeError("R56 audit module not found")
    raw = AUDIT_FILE.read_bytes()
    old, style = _read_lf(raw)
    current = _sha(old)
    if current == BASELINE_SHA256:
        updated = patch_source(old)
    elif current == PATCHED_SHA256:
        updated = old
        if updated.count(NEW_LINE) != 1 or OLD_LINE in updated:
            raise RuntimeError("R56 patched audit structure is invalid")
        ast.parse(updated, filename=str(AUDIT_FILE))
    else:
        raise RuntimeError("R56 audit was edited outside reviewed baseline; refusing overwrite")
    return {
        "local_head": base["local_head"],
        "source_guard": "PASS",
        "audit_source_sha256": current,
        "changed": current != PATCHED_SHA256,
        "raw": raw,
        "replacement": updated.replace("\n", style).encode("utf-8"),
    }


def install(dry_run: bool) -> dict[str, object]:
    state = review()
    if not dry_run and state["changed"]:
        AUDIT_FILE.write_bytes(state["replacement"])
        if _sha(_read_lf(AUDIT_FILE.read_bytes())[0]) != PATCHED_SHA256:
            raise RuntimeError("R56 audit post-install file check failed")
    return {
        "local_head": state["local_head"],
        "source_guard": state["source_guard"],
        "audit_source_sha256": state["audit_source_sha256"],
        "changed": state["changed"],
        "gate": ("PASS_R56R1_PREFLIGHT_ONLY" if dry_run
                 else "PASS_R56R1_AUDIT_REPORT_PATH_PATCHED"),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    state = install(args.dry_run)
    for key, value in state.items():
        print("PHASE174_R56R1_" + key.upper() + "=" + str(value))
    print("PHASE174_R56R1_NEW_GIVEN=0")
    print("PHASE174_R56R1_NEW_MATH_RULES=0")
    print("(END)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
