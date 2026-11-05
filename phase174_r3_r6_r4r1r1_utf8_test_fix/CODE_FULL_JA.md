# Phase 174 R3-R6-R4R1R1 コード全文

## 変更対象

`phase174_r3_r6_r4r1_cited_reference_link_fix/tests/test_r4r1_guard.py` の `test_source_formula_is_shared_between_two_reviewed_reference_paths()` の2箇所のみ。

- import 変更なし。
- 変更対象テスト関数全体：

```python
def test_source_formula_is_shared_between_two_reviewed_reference_paths() -> None:
    old = (ROOT / PACKAGE / "output"
           / "phase174_r3_r6_r4_common_reference__projection.py.BASELINE.py").read_text(encoding="utf-8")
    new = (ROOT / PACKAGE / "output"
           / "phase174_r3_r6_r4_common_reference__projection.py.FULL.py").read_text(encoding="utf-8")
    assert old.count(r"$\Delta(\iota_{2n-1})=0$") == 1
    assert new.count(r"$\Delta(\iota_{2n-1})=0$") == 1
    assert new.count(r"$n\ge5$ に対し, $2\nu_n=E^{n-3}\nu'$.") == 1
    assert "verify_extension_texts()" in new
    assert "step.rule is not ProofRule.GIVEN" in new
    assert "source_locator != locator" in new
    ast.parse(new)
```

## 置換対象のテストファイル全文

`output/test_r4r1_guard_FULL.py`（新 ZIP に収録）

## 新規 patch.py 全文

```python
"""Apply a one-function UTF-8 test correction without changing production code."""
from __future__ import annotations

import argparse
import ast
from hashlib import sha256
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[1]
PACKAGE = Path(__file__).resolve().parent
TARGET = Path("phase174_r3_r6_r4r1_cited_reference_link_fix/tests/test_r4r1_guard.py")
REVIEWED_HEAD = "f2e148afefb11eb0b0ca31da67c65ec1ffe9e1e9"
BEFORE_SHA256 = "e343d31878ce0c643e8c13f928adb2549816cd63e3ff6574cb0065300c1b406d"
AFTER_SHA256 = "586f1944642b69797989ba3191999bb88e905c395c74a5c90f08d7bd28627f2d"
PRODUCTION = {
    "phase168_r3_37c_reference_projection.py": "a58da77164fbc344b5a5c8fafb4a22081122d003abc62f905b5652e32fb29b9a",
    "phase174_r3_r6_r4_common_reference/projection.py": "bde402ac49186f63645a559558c9e1bbaa465447d65c999e25d3ac29a749aba9",
}


def git(*args: str) -> str:
    result = subprocess.run(("git",) + args, cwd=ROOT, capture_output=True, check=False)
    if result.returncode != 0:
        raise ValueError("git failed: " + " ".join(args) + ": "
                         + result.stderr.decode("utf-8", errors="replace"))
    return result.stdout.decode("utf-8").strip()


def normalized(raw: bytes) -> bytes:
    content = raw[3:] if raw.startswith(b"\xef\xbb\xbf") else raw
    if b"\r\n" in content:
        remaining = content.replace(b"\r\n", b"")
        if b"\n" in remaining or b"\r" in remaining:
            raise ValueError("Mixed newline style is not approved")
    elif b"\r" in content:
        raise ValueError("CR-only newline style is not approved")
    return content.replace(b"\r\n", b"\n")


def digest(raw: bytes) -> str:
    return sha256(normalized(raw)).hexdigest()


def restore_format(original: bytes, lf_bytes: bytes) -> bytes:
    bom = b"\xef\xbb\xbf" if original.startswith(b"\xef\xbb\xbf") else b""
    normalized(original)
    content = original[len(bom):]
    return bom + (lf_bytes.replace(b"\n", b"\r\n")
                  if b"\r\n" in content else lf_bytes)


def review_patch(before: bytes) -> bytes:
    """Change exactly two UTF-8 reads within one reviewed test function."""
    if digest(before) == AFTER_SHA256:
        return before
    if digest(before) != BEFORE_SHA256:
        raise ValueError("Unreviewed test content: refusing to overwrite")
    source = normalized(before).decode("utf-8")
    tree = ast.parse(source)
    functions = [node for node in tree.body if isinstance(node, ast.FunctionDef)
                 and node.name == "test_source_formula_is_shared_between_two_reviewed_reference_paths"]
    if len(functions) != 1:
        raise ValueError("Target test function missing or duplicated")
    node = functions[0]
    lines = source.splitlines(keepends=True)
    segment = "".join(lines[node.lineno - 1:node.end_lineno])
    if segment.count(".read_text()") != 2:
        raise ValueError("Expected exactly two implicit-encoding reads")
    changed = segment.replace(".read_text()", '.read_text(encoding="utf-8")')
    candidate = "".join(lines[:node.lineno - 1]) + changed + "".join(lines[node.end_lineno:])
    ast.parse(candidate)
    encoded = candidate.encode("utf-8")
    if sha256(encoded).hexdigest() != AFTER_SHA256:
        raise ValueError("Generated test does not match reviewed replacement")
    packaged = (PACKAGE / "output" / "test_r4r1_guard_FULL.py").read_bytes()
    if sha256(packaged).hexdigest() != AFTER_SHA256 or packaged != encoded:
        raise ValueError("Packaged full test differs from reviewed replacement")
    return restore_format(before, encoded)


def preflight() -> tuple[bytes, bool]:
    branch, local, remote = git("branch", "--show-current"), git("rev-parse", "HEAD"), git("rev-parse", "origin/develop")
    print("PHASE174_R4R1R1_BRANCH=" + branch)
    print("PHASE174_R4R1R1_LOCAL_HEAD=" + local)
    print("PHASE174_R4R1R1_REMOTE_HEAD=" + remote)
    if branch != "develop" or local != REVIEWED_HEAD or remote != REVIEWED_HEAD:
        raise ValueError("Unknown develop HEAD; refusing changes")
    if git("diff", "--cached", "--name-only", "--", TARGET.as_posix()):
        raise ValueError("Test has staged changes requiring review")
    for path, expected in PRODUCTION.items():
        current = (ROOT / path).read_bytes()
        if digest(current) != expected:
            raise ValueError("Production patch missing or unreviewed: " + path)
    original = (ROOT / TARGET).read_bytes()
    candidate = review_patch(original)
    return candidate, candidate == original


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    candidate, installed = preflight()
    print("PHASE174_R4R1R1_PRODUCTION_GUARD=PASS")
    print("PHASE174_R4R1R1_TEST_ALREADY_CORRECTED=" + str(installed))
    print("PHASE174_R4R1R1_PRODUCTION_WRITES=0")
    if args.dry_run:
        print("PHASE174_R4R1R1_DRY_RUN=PASS")
        return 0
    if not installed:
        (ROOT / TARGET).write_bytes(candidate)
    print("PHASE174_R4R1R1_TEST_FIX_APPLIED=PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

```

## 新規テスト全文（importを含む）

```python
"""Isolated guard tests for the UTF-8-only regression fix."""
from __future__ import annotations

import ast
from pathlib import Path

import pytest

from phase174_r3_r6_r4r1r1_utf8_test_fix.patch import (
    AFTER_SHA256,
    BEFORE_SHA256,
    PACKAGE,
    digest,
    restore_format,
    review_patch,
)


def _baseline() -> bytes:
    reviewed = PACKAGE.parent / "phase174_r3_r6_r4r1_cited_reference_link_fix"
    return (reviewed / "tests" / "test_r4r1_guard.py").read_bytes()


def test_only_implicit_encoding_reads_changed_in_one_function() -> None:
    original = (PACKAGE / "output" / "test_r4r1_guard_FULL.py").read_text(encoding="utf-8")
    tree = ast.parse(original)
    functions = {node.name: node for node in tree.body if isinstance(node, ast.FunctionDef)}
    assert "test_source_formula_is_shared_between_two_reviewed_reference_paths" in functions
    assert original.count('.read_text(encoding="utf-8")') == 4
    assert ".read_text()" not in original


def test_reviewed_hash_and_idempotency() -> None:
    candidate = (PACKAGE / "output" / "test_r4r1_guard_FULL.py").read_bytes()
    assert digest(candidate) == AFTER_SHA256
    assert review_patch(candidate) == candidate
    assert AFTER_SHA256 != BEFORE_SHA256


def test_rejects_unreviewed_edited_test() -> None:
    candidate = (PACKAGE / "output" / "test_r4r1_guard_FULL.py").read_bytes()
    with pytest.raises(ValueError, match="Unreviewed test content"):
        review_patch(candidate + b"# unreviewed local note\n")


def test_retains_windows_crlf_bom() -> None:
    sample = b"\xef\xbb\xbf" + b"first\r\nsecond\r\n"
    assert restore_format(sample, b"first\nthird\n") == b"\xef\xbb\xbffirst\r\nthird\r\n"


def test_imported_test_module_uses_explicit_utf8_only() -> None:
    target = (PACKAGE / "output" / "test_r4r1_guard_FULL.py").read_text(encoding="utf-8")
    tree = ast.parse(target)
    fn = next(node for node in tree.body if isinstance(node, ast.FunctionDef)
              and node.name == "test_source_formula_is_shared_between_two_reviewed_reference_paths")
    segment = "\n".join(target.splitlines()[fn.lineno - 1:fn.end_lineno])
    assert segment.count('.read_text(encoding="utf-8")') == 2
    assert '.read_text()' not in segment

```

## 新規 run.ps1 全文

```powershell
param([switch]$DryRun)

$ErrorActionPreference = 'Stop'
Set-StrictMode -Version Latest

$Repo = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Set-Location -LiteralPath $Repo

& git fetch origin develop
if ($LASTEXITCODE -ne 0) { throw 'R4R1R1 cannot refresh GitHub develop.' }

$Tests = @(
    'phase174_r3_r6_r4r1r1_utf8_test_fix/tests/test_r4r1r1_utf8.py',
    'phase174_r3_r6_r4r1_cited_reference_link_fix/tests/test_r4r1_guard.py',
    'phase174_r3_r6_r4r1_cited_reference_link_fix/tests/test_r4r1_live_binding.py',
    'phase174_r3_r6_r4_common_reference/tests/test_r3r4_patch.py',
    'phase174_r3_r6_r4_common_reference/tests/test_r3r4_reference_bodies.py',
    'phase174_r3_r6_r3r2_pytest_importmode_fix/tests/test_r3r2_importmode.py',
    'phase174_r3_r6_r3r1_scoped_guard_fix/tests/test_patch.py',
    'phase174_r3_r6_r3_common_narrative/tests/test_projection.py',
    'phase174_r3_r5_finite_cyclic_extension/tests/test_rule.py',
    'phase174_r3_r6_source_extension/tests/test_source.py',
    'phase174_r3_r6_r2_prop44_lemma54/tests/test_source.py',
    'phase172_r5_prior_reference_display/tests/test_projection.py'
)

& python -m phase174_r3_r6_r4r1r1_utf8_test_fix.patch --dry-run
if ($LASTEXITCODE -ne 0) { throw 'R4R1R1 review guard failed.' }

if ($DryRun) {
    Write-Output 'PHASE174_R4R1R1_COLLECTION_START'
    & python -m pytest --import-mode=importlib -p no:cacheprovider --collect-only -q @Tests
    if ($LASTEXITCODE -ne 0) { throw 'R4R1R1 collection failed.' }
    Write-Output 'PHASE174_R4R1R1_COLLECTION=PASS'
    Write-Output 'PHASE174_R4R1R1_DRYRUN_GATE=PASS'
} else {
    & python -m phase174_r3_r6_r4r1r1_utf8_test_fix.patch
    if ($LASTEXITCODE -ne 0) { throw 'R4R1R1 test correction failed.' }
    Write-Output 'PHASE174_R4R1R1_FOCUSED_PYTEST_START'
    & python -m pytest --import-mode=importlib -p no:cacheprovider -q @Tests
    if ($LASTEXITCODE -ne 0) { throw 'R4R1R1 focused pytest failed.' }
    Write-Output 'PHASE174_R4R1R1_FOCUSED_PYTEST=PASS'
    & python -m phase174_r3_r6_r4_common_reference.audit
    if ($LASTEXITCODE -ne 0) { throw 'R4R1R1 public Reference audit failed.' }
    Write-Output 'PHASE174_R4R1R1_AUDIT=PASS'
    Write-Output 'PHASE174_R4R1R1_GATE=PASS'
}
Write-Output '(END)'

```
