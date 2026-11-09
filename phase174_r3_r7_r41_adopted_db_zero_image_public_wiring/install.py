"""Install only the reviewed R41 shared-provider connection, atomically."""
from __future__ import annotations

import argparse
import os
from pathlib import Path
import tempfile

from phase174_r3_r7_r41_adopted_db_zero_image_public_wiring.source_guard import (
    ROOT, TARGET, expected_replacement, git_bytes, normalized, verified_state,
)

PACKAGE = Path(__file__).resolve().parent


def full_changed_function(source: str) -> str:
    """Extract the whole modified callable for user inspection, never snippets."""
    anchor = "def shared_expansion_provider("
    if source.count(anchor) != 1:
        raise RuntimeError("Unexpected shared_expansion_provider definition count")
    start = source.index(anchor)
    next_def = source.find("\ndef ", start + len(anchor))
    return (source[start:] if next_def < 0 else source[start:next_def]).rstrip() + "\n"


def install(*, dry_run: bool) -> dict[str, object]:
    state = verified_state()
    if dry_run:
        state["mode"] = "DRYRUN"
        return state
    target = ROOT / TARGET
    baseline = git_bytes("show", "HEAD:" + TARGET)
    expected = expected_replacement(baseline)
    if state["shared_math_mode"] == "BASELINE":
        old = target.read_bytes()
        update = expected.replace(b"\n", b"\r\n") if b"\r\n" in old else expected
        temp_path = None
        try:
            with tempfile.NamedTemporaryFile(mode="wb", dir=target.parent,
                                             prefix="r41_", suffix=".tmp",
                                             delete=False) as stream:
                temp_path = stream.name
                stream.write(update)
            os.replace(temp_path, target)
        finally:
            if temp_path is not None and os.path.exists(temp_path):
                os.unlink(temp_path)
    after = verified_state()
    if after["shared_math_mode"] != "INSTALLED":
        raise RuntimeError("R41 shared provider patch did not verify")
    # Produce the complete replacement function and import section on disk.
    # This is documentation-only; not imported as another production module.
    source = normalized(target.read_bytes()).decode("utf-8")
    whole = full_changed_function(source)
    (PACKAGE / "CHANGED_FUNCTION_FULL.py").write_text(whole, encoding="utf-8")
    before_function = source.split("def shared_expansion_provider(", 1)[0]
    (PACKAGE / "IMPORTS_FULL.txt").write_text(before_function, encoding="utf-8")
    after["mode"] = "INSTALLED"
    after["full_function_emitted"] = True
    return after


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    state = install(dry_run=args.dry_run)
    for key, value in state.items():
        print("PHASE174_R3R7R41_" + key.upper() + "=" + str(value))
    print("PHASE174_R3R7R41_GATE=PASS_R41_SOURCE_GUARD_AND_PROVIDER_WIRING")
    print("(END)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
