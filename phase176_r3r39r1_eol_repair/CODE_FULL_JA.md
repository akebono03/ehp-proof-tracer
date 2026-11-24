# R3R39R1 追加・変更コード全文

既存の R3R39 ディレクトリの apply.py を置換する。R3R39 の CODE_FULL_JA.md も更新する。数学規則・Provider は変更しない。

## apply.py

```python
"""Idempotent, anchored R3R39 minimal shared-provider patch."""
from __future__ import annotations

import argparse
import ast
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TARGET = ROOT / "phase165_r52_r9_shared_math.py"
INSERT_AFTER_AVAILABLE = "    if not isinstance(prior_conclusions, tuple):\n"
INSERT_AFTER_HOPF = "        options.extend(expand_cited_composite_right_hopf(goal, tuple(available)))\n"
NEW_SETUP = (
    "    # Phase 176 R3R39: source-screened, six existing equality inferences.\n"
    "    from phase176_r3r39_public_equality_transport.source import (\n"
    "        build_public_right_hopf_transport_provider,\n"
    "    )\n"
    "    public_right_hopf_transport = build_public_right_hopf_transport_provider(\n"
    "        tuple(available),\n"
    "    )\n"
)
NEW_DISPATCH = (
    "        # All six transport steps stay visible in the ordinary Proof Tree.\n"
    "        options.extend(public_right_hopf_transport(goal))\n"
)


def updated_source(source: str) -> str:
    """Produce one exact shared-function update; fail on missing/changed hooks."""
    setup_count = source.count(NEW_SETUP)
    dispatch_count = source.count(NEW_DISPATCH)
    if setup_count == 1 and dispatch_count == 1:
        return source
    if setup_count != 0 or dispatch_count != 0:
        raise ValueError("PARTIAL_R3R39_PATCH_REFUSED")
    if (source.count(INSERT_AFTER_AVAILABLE) != 1
            or source.count(INSERT_AFTER_HOPF) != 1
            or source.count("options.extend(expand_composite_suspension_equality(goal))") != 1):
        raise ValueError("SHARED_PROVIDER_ANCHORS_CHANGED")
    return source.replace(
        INSERT_AFTER_AVAILABLE, NEW_SETUP + INSERT_AFTER_AVAILABLE, 1,
    ).replace(
        INSERT_AFTER_HOPF, INSERT_AFTER_HOPF + NEW_DISPATCH, 1,
    )


def normalized_source(raw: bytes) -> str:
    """Decode UTF-8 without treating the byte representation as source code."""
    return raw.decode("utf-8-sig").replace("\r\n", "\n").replace("\r", "\n")


def patched_bytes(baseline: bytes, current: bytes) -> bytes:
    """Only permit the exact R3R39 insertion; preserve baseline EOL and BOM."""
    original = normalized_source(baseline)
    proposed = updated_source(original)
    if normalized_source(current) not in (original, proposed):
        raise ValueError("UNRELATED_WORKTREE_CHANGE_REFUSED")
    without_crlf = baseline.replace(b"\r\n", b"")
    if b"\r" in without_crlf or (b"\r\n" in baseline and b"\n" in without_crlf):
        raise ValueError("MIXED_OR_UNSUPPORTED_BASELINE_EOL")
    eol = "\r\n" if b"\r\n" in baseline else "\n"
    encoding = "utf-8-sig" if baseline.startswith(b"\xef\xbb\xbf") else "utf-8"
    ast.parse(proposed, filename=str(TARGET))
    return proposed.replace("\n", eol).encode(encoding)


def tracked_baseline() -> bytes:
    """Reject staged changes; compare the index and HEAD as exact bytes."""
    relative = TARGET.relative_to(ROOT).as_posix()
    head = subprocess.check_output(["git", "show", "HEAD:" + relative], cwd=ROOT)
    index = subprocess.check_output(["git", "show", ":" + relative], cwd=ROOT)
    if head != index:
        raise ValueError("STAGED_TARGET_CHANGE_REFUSED")
    return index


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    for required in (
        ROOT / "phase176_r3r38_equality_transport_isolated/source.py",
        ROOT / "phase176_r3r34_composite_suspension_isolated/source.py",
        ROOT / "phase176_r3r36_composite_right_hopf_isolated/source.py",
    ):
        if not required.is_file():
            raise ValueError("MISSING_BASELINE:" + str(required.relative_to(ROOT)))
    current = TARGET.read_bytes()
    proposed = patched_bytes(tracked_baseline(), current)
    if not args.dry_run:
        if current != proposed:
            TARGET.write_bytes(proposed)
        if TARGET.read_bytes() != proposed:
            raise ValueError("BYTE_VERIFICATION_FAILED")
        text = normalized_source(proposed)
        start = text.index("def shared_expansion_provider(")
        end = text.index("\ndef search_shared_group_goal(", start)
        documented = (
            "# Phase 176 R3R39 — shared_expansion_provider() 全文\n\n"
            "既存実装を維持し、R3R39 のセットアップと呼び出しのみを追加したものです。\n\n"
            "```python\n" + text[start:end].rstrip() + "\n```\n"
        )
        (Path(__file__).resolve().parent / "SHARED_FUNCTION_FULL_JA.md").write_bytes(
            documented.encode("utf-8"),
        )
    print("PHASE176_R3R39_PATCH=" + ("DRY_RUN_PASS" if args.dry_run else "APPLIED_OR_ALREADY_PRESENT"))
    print("PHASE176_R3R39R1_EOL=" + ("DRY_RUN_PASS" if args.dry_run else "BYTE_VERIFIED"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

## test_eol.py

```python
import pytest

from phase176_r3r39_public_equality_transport.apply import (
    INSERT_AFTER_AVAILABLE, INSERT_AFTER_HOPF, normalized_source,
    patched_bytes, updated_source,
)


def baseline_text():
    return (
        "def f(prior_conclusions, goal, available):\n"
        + INSERT_AFTER_AVAILABLE + "        pass\n"
        + "    if True:\n"
        + "        options.extend(expand_composite_suspension_equality(goal))\n"
        + INSERT_AFTER_HOPF
    )


@pytest.mark.parametrize("eol", ["\n", "\r\n"])
@pytest.mark.parametrize("bom", [b"", b"\xef\xbb\xbf"])
def test_exact_patch_and_repair_preserve_baseline_bytes(eol, bom):
    original = baseline_text()
    expected_text = updated_source(original)
    baseline = bom + original.replace("\n", eol).encode("utf-8")
    expected = bom + expected_text.replace("\n", eol).encode("utf-8")
    wrong = expected_text.replace("\n", "\r\n" if eol == "\n" else "\n").encode("utf-8")
    assert patched_bytes(baseline, baseline) == expected
    assert patched_bytes(baseline, wrong) == expected
    assert patched_bytes(baseline, expected) == expected
    assert normalized_source(expected) == expected_text


def test_unrelated_change_is_refused():
    original = baseline_text().encode("utf-8")
    with pytest.raises(ValueError, match="UNRELATED_WORKTREE_CHANGE_REFUSED"):
        patched_bytes(original, original + b"# unrelated\n")


def test_mixed_baseline_is_refused():
    original = baseline_text().encode("utf-8")
    mixed = original.replace(b"\n", b"\r\n", 1)
    with pytest.raises(ValueError, match="MIXED_OR_UNSUPPORTED_BASELINE_EOL"):
        patched_bytes(mixed, original)
```

## run.ps1

```powershell
param([switch]$DryRun)
$ErrorActionPreference = 'Stop'
$root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Push-Location $root
try {
    $argsForPatch = @()
    if ($DryRun) { $argsForPatch += '--dry-run' }
    & python -B -m phase176_r3r39_public_equality_transport.apply @argsForPatch
    if ($LASTEXITCODE -ne 0) { throw 'R3R39R1 byte repair failed' }
    if ($DryRun) {
        Write-Host 'PHASE176_R3R39R1_GATE=PASS_R3R39R1_DRYRUN'
        return
    }
    & git diff --check
    if ($LASTEXITCODE -ne 0) { throw 'git diff check failed' }
    $stat = @(& git diff --numstat -- phase165_r52_r9_shared_math.py)
    if ($LASTEXITCODE -ne 0) { throw 'git diff numstat failed' }
    if ($stat.Count -ne 1 -or $stat[0] -notmatch '^9\t0\tphase165_r52_r9_shared_math\.py$') {
        throw ('Unexpected target diff: ' + ($stat -join '; '))
    }
    & python -B -m pytest -q -p no:cacheprovider --import-mode=importlib .\phase176_r3r39r1_eol_repair\test_eol.py
    if ($LASTEXITCODE -ne 0) { throw 'EOL tests failed' }
    & powershell -NoProfile -ExecutionPolicy Bypass -File .\phase176_r3r39_public_equality_transport\run.ps1
    if ($LASTEXITCODE -ne 0) { throw 'R3R39 regression failed' }
    Write-Host 'PHASE176_R3R39R1_GATE=PASS_R3R39R1_MINIMAL_DIFF_FOCUSED_TESTS'
    Write-Host 'PHASE176_R3R39R1_FULL_PYTEST=NOT_RUN'
} finally {
    Pop-Location
}
```
