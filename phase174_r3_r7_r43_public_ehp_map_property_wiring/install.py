"""Guarded atomic installation of two existing generic EHP providers."""
from __future__ import annotations

import argparse
import os
from pathlib import Path
import tempfile

from phase174_r3_r7_r43_public_ehp_map_property_wiring.source_guard import (
    ROOT, TARGET, expected_replacement, git_bytes, normalize, verify_checkout,
)

PACKAGE = Path(__file__).resolve().parent


def full_changed_function(source: str) -> str:
    """Emit a complete replaceable function rather than an abbreviated diff."""
    marker = "def shared_expansion_provider("
    if source.count(marker) != 1:
        raise RuntimeError("Unexpected shared_expansion_provider definition count")
    start = source.index(marker)
    next_def = source.find("\ndef ", start + len(marker))
    return (source[start:] if next_def < 0 else source[start:next_def]).rstrip() + "\n"


def install(*, dry_run: bool) -> dict[str, object]:
    state = verify_checkout()
    if dry_run:
        state["mode"] = "DRYRUN"
        return state
    target = ROOT / TARGET
    expected = expected_replacement(git_bytes("show", "HEAD:" + TARGET))
    if state["shared_math_mode"] == "BASELINE":
        original = target.read_bytes()
        chosen = expected.replace(b"\n", b"\r\n") if b"\r\n" in original else expected
        temp_path = None
        try:
            with tempfile.NamedTemporaryFile(
                mode="wb", dir=target.parent, prefix="r43_", suffix=".tmp",
                delete=False,
            ) as out:
                temp_path = out.name
                out.write(chosen)
            os.replace(temp_path, target)
        finally:
            if temp_path is not None and os.path.exists(temp_path):
                os.unlink(temp_path)
    after = verify_checkout()
    if after["shared_math_mode"] != "INSTALLED":
        raise RuntimeError("R43 provider installation could not be verified")
    updated = normalize(target.read_bytes()).decode("utf-8")
    # Documentation artifacts generated from the exact validated replacement.
    (PACKAGE / "CHANGED_FUNCTION_FULL.py").write_text(
        full_changed_function(updated), encoding="utf-8",
    )
    (PACKAGE / "IMPORTS_FULL.txt").write_text(
        updated.split("def shared_expansion_provider(", 1)[0], encoding="utf-8",
    )
    after["mode"] = "INSTALLED"
    after["full_function_emitted"] = True
    return after


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()
    state = install(dry_run=args.dry_run)
    for key, value in state.items():
        print("PHASE174_R3R7R43_" + key.upper() + "=" + str(value))
    print("PHASE174_R3R7R43_GATE=PASS_R43_GUARDED_GENERIC_EHP_PROVIDER_INSTALL")
    print("(END)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
