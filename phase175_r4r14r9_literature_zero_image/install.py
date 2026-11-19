"""Guarded overlay installer for Phase 175 R4R14R9; run from its own folder."""
from __future__ import annotations

import argparse
import subprocess
from pathlib import Path

MODULE = "phase175_r4r14r9_literature_zero_image"
EXPECTED_HEAD = "e83d5a45f52bf6b755f46e8574de1208247c7ba8"
ANCHOR = "    # R41: retain DB-prior provenance and the actual cited source boundary."
INJECTION = '''    # Phase 175 R4R14R9: independently cited finite-cyclic zero image.\n    # The R41 DB-specific verification remains unchanged.\n    from phase175_r4r14r9_literature_zero_image.provider import (\n        build_literature_zero_image_provider,\n    )\n    extra_providers = (\n        build_literature_zero_image_provider(\n            bridge=bridge, proof_target=proof_target,\n        ),\n    ) + tuple(extra_providers)\n'''


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    source = Path(__file__).resolve().parent
    root = source.parent
    target = root / "phase165_r52_r9_shared_math.py"
    if not target.is_file():
        raise SystemExit("Repository root or shared_math file not found")
    head = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=root, text=True).strip()
    if head != EXPECTED_HEAD:
        raise SystemExit(f"HEAD mismatch: expected {EXPECTED_HEAD}, actual {head}")
    current = target.read_bytes()
    newline = "\r\n" if b"\r\n" in current else "\n"
    content = current.decode("utf-8")
    if content.count(ANCHOR) != 1:
        raise SystemExit("Expected exactly one R41 shared-provider anchor")
    if INJECTION.splitlines()[0] in content:
        print("R4R14R9_ALREADY_INSTALLED=YES")
        return
    if not args.dry_run:
        replacement = INJECTION.replace("\n", newline) + ANCHOR
        target.write_bytes(content.replace(ANCHOR, replacement, 1).encode("utf-8"))
    print("R4R14R9_HEAD=" + head)
    print("R4R14R9_PATCH=" + ("DRY_RUN" if args.dry_run else "INSTALLED"))
    print("R4R14R9_NEW_GIVEN=0")
    print("(END)")


if __name__ == "__main__":
    main()
