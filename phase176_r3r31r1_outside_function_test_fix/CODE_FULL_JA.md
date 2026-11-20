# R3R31R1 変更コード全文

## 置換対象テスト関数

```python
def test_patch_rejects_outside_function() -> None:
    incorrect = (
        "def shared_expansion_provider():\n"
        "    return None\n"
        "\n"
        "def unrelated():\n"
        "    if True:\n"
        + MARKER + "\n"
        "    return None\n"
    )
    with pytest.raises(ValueError, match="ANCHOR_OUTSIDE_SHARED_PROVIDER"):
        proposed_code(incorrect)

```

## 変更後のテストファイル全文

```python
"""Focused public hookup guardrails."""
from __future__ import annotations

import pytest

from phase176_r3r31_generic_hopf_public_connection.installer import (
    MARKER, NEW_LINES, proposed_code, changed_function_text,
)


def baseline():
    return (
        "def shared_expansion_provider():\n"
        "    def expand(goal):\n"
        "        options = []\n"
        + MARKER + "\n"
        "        return options\n"
        "    return expand\n"
    )


def test_additive_patch_inserts_once() -> None:
    proposed = proposed_code(baseline())
    assert proposed.count("expand_generic_hopf_substitution(goal, tuple(available))") == 1
    assert MARKER in proposed
    assert "def shared_expansion_provider" in changed_function_text(proposed)


def test_patch_rejects_repeated_insertion() -> None:
    with pytest.raises(ValueError, match="ALREADY_APPLIED"):
        proposed_code(proposed_code(baseline()))


def test_patch_rejects_missing_anchor() -> None:
    with pytest.raises(ValueError, match="EXPECTED_SINGLE"):
        proposed_code("def shared_expansion_provider():\n    return None\n")


def test_patch_rejects_outside_function() -> None:
    incorrect = (
        "def shared_expansion_provider():\n"
        "    return None\n"
        "\n"
        "def unrelated():\n"
        "    if True:\n"
        + MARKER + "\n"
        "    return None\n"
    )
    with pytest.raises(ValueError, match="ANCHOR_OUTSIDE_SHARED_PROVIDER"):
        proposed_code(incorrect)


def test_patch_keeps_existing_code_unchanged() -> None:
    initial = baseline()
    result = proposed_code(initial)
    assert result.replace(NEW_LINES, "") == initial
```

## installer.py 全文

```python
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
```

## run.ps1 全文

```powershell
param([switch]$DryRun)
$ErrorActionPreference = 'Stop'
Push-Location (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
try {
    if ($DryRun) {
        python -B -m phase176_r3r31r1_outside_function_test_fix.installer --dry-run
        if ($LASTEXITCODE -ne 0) { throw 'R3R31R1 DryRun failed' }
    } else {
        python -B -m phase176_r3r31r1_outside_function_test_fix.installer
        if ($LASTEXITCODE -ne 0) { throw 'R3R31R1 install failed' }
        python -B -m pytest -q -p no:cacheprovider `
            .\phase176_r3r31r1_outside_function_test_fix\tests `
            .\phase176_r3r31_generic_hopf_public_connection\tests `
            .\phase176_r3r30_generic_hopf_substitution_isolated\tests `
            .\phase171_r2h_prop22_cited_hopf\tests\test_cited_formula.py
        if ($LASTEXITCODE -ne 0) { throw 'R3R31R1 focused tests failed' }
        Write-Host 'PHASE176_R3R31R1_GATE=PASS_R3R31R1_FOCUSED_TESTS'
        Write-Host 'PHASE176_R3R31R1_FULL_PYTEST=NOT_RUN'
        Write-Host '(END)'
    }
} finally {
    Pop-Location
}
```
