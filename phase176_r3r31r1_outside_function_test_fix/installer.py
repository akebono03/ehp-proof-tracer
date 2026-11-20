"""Replace exactly one incorrect R3R31 test function; no production edits."""
from __future__ import annotations

import argparse
import ast
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parent.parent
TARGET = ROOT / "phase176_r3r31_generic_hopf_public_connection" / "tests" / "test_installer.py"
OLD_FUNCTION = 'def test_patch_rejects_outside_function() -> None:\n    incorrect = "def shared_expansion_provider():\\n    return None\\n" + MARKER + "\\n"\n    with pytest.raises(ValueError, match="OUTSIDE"):\n        proposed_code(incorrect)\n\n'
NEW_FUNCTION = 'def test_patch_rejects_outside_function() -> None:\n    incorrect = (\n        "def shared_expansion_provider():\\n"\n        "    return None\\n"\n        "\\n"\n        "def unrelated():\\n"\n        "    if True:\\n"\n        + MARKER + "\\n"\n        "    return None\\n"\n    )\n    with pytest.raises(ValueError, match="ANCHOR_OUTSIDE_SHARED_PROVIDER"):\n        proposed_code(incorrect)\n\n'


def replace_test(source: str) -> str:
    if source.count(OLD_FUNCTION) == 1 and NEW_FUNCTION not in source:
        revised = source.replace(OLD_FUNCTION, NEW_FUNCTION, 1)
        ast.parse(revised)
        return revised
    if source.count(NEW_FUNCTION) == 1 and OLD_FUNCTION not in source:
        ast.parse(source)
        return source
    raise ValueError("R3R31_TEST_BASELINE_MISMATCH")


def run(dry_run: bool) -> int:
    branch = subprocess.run(
        ["git", "branch", "--show-current"], cwd=ROOT,
        text=True, capture_output=True,
    )
    if branch.returncode or branch.stdout.strip() != "develop":
        raise RuntimeError("DEVELOP_REQUIRED")
    if not TARGET.is_file():
        raise FileNotFoundError(TARGET)
    original = TARGET.read_bytes()
    eol = "\r\n" if b"\r\n" in original else "\n"
    encoding = "utf-8-sig" if original.startswith(b"\xef\xbb\xbf") else "utf-8"
    text = original.decode(encoding)
    normalized = text.replace("\r\n", "\n")
    revised = replace_test(normalized)
    if not dry_run and revised != normalized:
        TARGET.write_bytes(revised.replace("\n", eol).encode(encoding))
    print("PHASE176_R3R31R1_GATE=" + (
        "PASS_R3R31R1_DRYRUN" if dry_run else "PASS_R3R31R1_TEST_FIXED"
    ))
    print("PHASE176_R3R31R1_PRODUCTION_CHANGES=0")
    print("PHASE176_R3R31R1_FULL_PYTEST=NOT_RUN")
    print("(END)")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    try:
        return run(args.dry_run)
    except (OSError, ValueError, RuntimeError, SyntaxError) as error:
        print("PHASE176_R3R31R1_GATE=FAIL_R3R31R1")
        print("PHASE176_R3R31R1_ERROR=" + str(error))
        return 1


if __name__ == "__main__":
    sys.exit(main())
