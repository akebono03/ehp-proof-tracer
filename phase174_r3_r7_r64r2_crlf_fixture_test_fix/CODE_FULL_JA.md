# Phase 174 R64R2 — 変更・追加コード全文

## 既存の対象テストファイル（変更後の関数全文）

ファイル: `phase174_r3_r7_r64r1_pytest_tmp_path_fix/tests/test_install.py`。既存 import は変更なし。

```python
def test_review_accepts_crlf_line_endings(tmp_path: Path) -> None:
    create_review_fixture(tmp_path)
    target = tmp_path / TARGET
    normalized = target.read_bytes().replace(b"\r\n", b"\n")
    target.write_bytes(normalized.replace(b"\n", b"\r\n"))
    status, _original, after = review(tmp_path)
    assert status == "PATCH_REQUIRED"
    assert b"\r\n" in after
    assert b"\r\r\n" not in after
    target.write_bytes(after)
    assert review(tmp_path)[0] == "ALREADY_APPLIED"
```

## 既存テストファイルの import 全文（変更なし）

```python
"""R64R1 isolated negative tests and exact one-function replacement."""
from __future__ import annotations

from pathlib import Path

import pytest

from phase174_r3_r7_r64r1_pytest_tmp_path_fix.install import (
    EXPECTED_FIXED_BLOB, EXPECTED_OLD_BLOB, ORIGINAL_FUNCTION,
    PINNED_UNCHANGED, REPLACEMENT_FUNCTION, TARGET, git_blob_sha,
    patch_test, review,
)
```

## 新規 `install.py`（全文、配置先：新規 R64R2 ディレクトリ）

```python
"""R64R2: correct only the CRLF fixture in one existing R64R1 pytest function.

No production code, proof, source, reference, or mathematical rule changes.
The existing R64R1 installer and R64 audit are separately pinned.
"""
from __future__ import annotations

import argparse
import ast
from hashlib import sha1
from pathlib import Path
import subprocess

PACKAGE = "phase174_r3_r7_r64r2_crlf_fixture_test_fix"
TARGET = "phase174_r3_r7_r64r1_pytest_tmp_path_fix/tests/test_install.py"
PINNED_UNCHANGED = {
    "phase174_r3_r7_r64r1_pytest_tmp_path_fix/install.py": "a7990fd025580d0c7de7cb5e917865aeef48545e",
    "phase174_r3_r7_r64_sentence_coverage_frontier_audit/audit.py": "639b2290aeb09ead23367d0ed8a02e8f64ad6d6f",
    "phase174_r3_r7_r64_sentence_coverage_frontier_audit/tests/test_audit.py": "3122053b18dd87c57e78c2d4385f01852b51c708",
}
EXPECTED_OLD_BLOB = "ae6d1f0e8266fad222e607fc9548ab60061e14d5"
EXPECTED_FIXED_BLOB = "bde087fa884eccab7138eb67b8015690558b6a27"
ORIGINAL_FUNCTION = 'def test_review_accepts_crlf_line_endings(tmp_path: Path) -> None:\n    create_review_fixture(tmp_path)\n    target = tmp_path / TARGET\n    target.write_bytes(target.read_bytes().replace(b"\\n", b"\\r\\n"))\n    status, _original, after = review(tmp_path)\n    assert status == "PATCH_REQUIRED"\n    assert b"\\r\\n" in after\n    target.write_bytes(after)\n    assert review(tmp_path)[0] == "ALREADY_APPLIED"\n'
REPLACEMENT_FUNCTION = 'def test_review_accepts_crlf_line_endings(tmp_path: Path) -> None:\n    create_review_fixture(tmp_path)\n    target = tmp_path / TARGET\n    normalized = target.read_bytes().replace(b"\\r\\n", b"\\n")\n    target.write_bytes(normalized.replace(b"\\n", b"\\r\\n"))\n    status, _original, after = review(tmp_path)\n    assert status == "PATCH_REQUIRED"\n    assert b"\\r\\n" in after\n    assert b"\\r\\r\\n" not in after\n    target.write_bytes(after)\n    assert review(tmp_path)[0] == "ALREADY_APPLIED"\n'


def git_blob_sha(data: bytes) -> str:
    """Return the Git blob hash for exact file bytes."""
    return sha1(b"blob " + str(len(data)).encode("ascii") + b"\x00" + data).hexdigest()


def normalized_contents(data: bytes) -> tuple[str, bytes, str]:
    """Accept LF/CRLF, reject stray CR, and retain the file's BOM and EOL."""
    bom = b"\xef\xbb\xbf" if data.startswith(b"\xef\xbb\xbf") else b""
    remainder = data[len(bom):]
    if b"\r" in remainder.replace(b"\r\n", b""):
        raise RuntimeError("R64R2_UNEXPECTED_CR_ONLY_OR_DOUBLE_CR")
    eol = "\r\n" if b"\r\n" in remainder else "\n"
    return remainder.decode("utf-8").replace("\r\n", "\n"), bom, eol


def patch_test(source: str) -> str:
    """Replace precisely the reviewed test function, leaving every other byte alone."""
    tree = ast.parse(source)
    matches = tuple(node for node in tree.body
                    if isinstance(node, ast.FunctionDef)
                    and node.name == "test_review_accepts_crlf_line_endings")
    if len(matches) != 1 or source.count(ORIGINAL_FUNCTION) != 1:
        raise RuntimeError("R64R2_UNREVIEWED_OR_AMBIGUOUS_FUNCTION")
    result = source.replace(ORIGINAL_FUNCTION, REPLACEMENT_FUNCTION, 1)
    ast.parse(result)
    if result.replace(REPLACEMENT_FUNCTION, ORIGINAL_FUNCTION, 1) != source:
        raise RuntimeError("R64R2_NONMINIMAL_PATCH")
    return result


def review(root: Path) -> tuple[str, bytes, bytes]:
    """Verify existing installer/audit, then plan exactly one pytest-only edit."""
    if not root.is_dir():
        raise RuntimeError("R64R2_REPOSITORY_MISSING")
    for relative, expected in PINNED_UNCHANGED.items():
        path = root / relative
        if not path.is_file():
            raise RuntimeError("R64R2_REQUIRED_FILE_MISSING: " + relative)
        contents, _bom, _eol = normalized_contents(path.read_bytes())
        if git_blob_sha(contents.encode("utf-8")) != expected:
            raise RuntimeError("R64R2_REVIEWED_SOURCE_MISMATCH: " + relative)
    path = root / TARGET
    if not path.is_file():
        raise RuntimeError("R64R2_TARGET_MISSING")
    original = path.read_bytes()
    content, bom, eol = normalized_contents(original)
    current_hash = git_blob_sha(content.encode("utf-8"))
    if current_hash == EXPECTED_OLD_BLOB:
        revised = patch_test(content)
        if git_blob_sha(revised.encode("utf-8")) != EXPECTED_FIXED_BLOB:
            raise RuntimeError("R64R2_UNEXPECTED_REPLACEMENT_BLOB")
        status = "PATCH_REQUIRED"
    elif current_hash == EXPECTED_FIXED_BLOB:
        if content.count(REPLACEMENT_FUNCTION) != 1:
            raise RuntimeError("R64R2_FIXED_FUNCTION_MISSING")
        revised = content
        status = "ALREADY_APPLIED"
    else:
        raise RuntimeError("R64R2_UNREVIEWED_TARGET_BLOB: " + current_hash)
    after = bom + revised.replace("\n", eol).encode("utf-8")
    return status, original, after


def local_git_head(root: Path) -> str:
    """Report HEAD without requiring an obsolete fixed SHA."""
    result = subprocess.run(["git", "rev-parse", "HEAD"], cwd=root,
                            capture_output=True, text=True, check=False)
    if result.returncode != 0:
        raise RuntimeError("R64R2_GIT_HEAD_UNAVAILABLE")
    return result.stdout.strip()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true")
    opts = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    status, original, after = review(root)
    print("PHASE174_R64R2_SOURCE_GUARD=PASS")
    print("PHASE174_R64R2_SOURCE_PINS=4")
    print("PHASE174_R64R2_LOCAL_HEAD=" + local_git_head(root))
    print("PHASE174_R64R2_PATCH_STATUS=" + status)
    print("PHASE174_R64R2_PRODUCTION_CHANGES=0")
    print("PHASE174_R64R2_NEW_GIVEN=0")
    print("PHASE174_R64R2_NEW_MATHEMATICAL_RULES=0")
    if opts.dry_run:
        print("PHASE174_R64R2_GATE=PASS_R64R2_READ_ONLY_DRYRUN")
        print("(END)")
        return 0
    if original != after:
        (root / TARGET).write_bytes(after)
        if (root / TARGET).read_bytes() != after:
            raise RuntimeError("R64R2_WRITE_VERIFY_FAILED")
    print("PHASE174_R64R2_GATE=PASS_R64R2_PATCH_APPLIED_OR_PRESENT")
    print("(END)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

## 新規 `tests/test_install.py`（全文、配置先：新規 R64R2/tests）

```python
"""R64R2 focused, fail-closed EOL fixture regression tests."""
from __future__ import annotations

from pathlib import Path

import pytest

from phase174_r3_r7_r64r2_crlf_fixture_test_fix.install import (
    EXPECTED_FIXED_BLOB,
    EXPECTED_OLD_BLOB,
    ORIGINAL_FUNCTION,
    PINNED_UNCHANGED,
    REPLACEMENT_FUNCTION,
    TARGET,
    git_blob_sha,
    normalized_contents,
    patch_test,
    review,
)


def fixture_root(tmp_path: Path, *, eol: str = "lf") -> Path:
    """Copy reviewed sources, simulate the pre-fix R64R1 test on either OS."""
    source_root = Path(__file__).resolve().parents[2]
    for relative in (*PINNED_UNCHANGED, TARGET):
        src = source_root / relative
        dst = tmp_path / relative
        dst.parent.mkdir(parents=True, exist_ok=True)
        dst.write_bytes(src.read_bytes())
    target = tmp_path / TARGET
    original, _bom, _current_eol = normalized_contents(target.read_bytes())
    original = original.replace(REPLACEMENT_FUNCTION, ORIGINAL_FUNCTION)
    assert git_blob_sha(original.encode("utf-8")) == EXPECTED_OLD_BLOB
    if eol == "crlf":
        target.write_bytes(original.replace("\n", "\r\n").encode("utf-8"))
    elif eol == "lf":
        target.write_bytes(original.encode("utf-8"))
    else:
        raise ValueError("unknown fixture EOL")
    return tmp_path


def test_actual_repo_reviewed_and_already_applied() -> None:
    root = Path(__file__).resolve().parents[2]
    status, original, after = review(root)
    assert status == "ALREADY_APPLIED"
    assert original == after


def test_patch_is_exact_and_only_one_function() -> None:
    assert ORIGINAL_FUNCTION != REPLACEMENT_FUNCTION
    assert "target.read_bytes().replace" in ORIGINAL_FUNCTION
    assert "normalized = target.read_bytes().replace" in REPLACEMENT_FUNCTION
    replacement = patch_test(ORIGINAL_FUNCTION)
    assert replacement == REPLACEMENT_FUNCTION
    assert "not in after" in replacement


@pytest.mark.parametrize("starting_eol", ("lf", "crlf"))
def test_review_fixes_fixture_for_both_line_endings(
    tmp_path: Path, starting_eol: str,
) -> None:
    root = fixture_root(tmp_path, eol=starting_eol)
    target = root / TARGET
    initial = target.read_bytes()
    status, original, after = review(root)
    assert status == "PATCH_REQUIRED"
    assert original == initial
    assert after != initial
    assert b"\r\r\n" not in after
    if starting_eol == "crlf":
        assert b"\r\n" in after
    else:
        assert b"\r\n" not in after
    target.write_bytes(after)
    status2, current, after2 = review(root)
    assert status2 == "ALREADY_APPLIED"
    assert current == after2 == after


def test_pins_match_exact_reviewed_code(tmp_path: Path) -> None:
    root = fixture_root(tmp_path)
    for relative, expected in PINNED_UNCHANGED.items():
        text, _bom, _eol = normalized_contents((root / relative).read_bytes())
        assert git_blob_sha(text.encode("utf-8")) == expected
    _, original, after = review(root)
    before_text, _bom, _eol = normalized_contents(original)
    after_text, _bom2, _eol2 = normalized_contents(after)
    assert git_blob_sha(before_text.encode("utf-8")) == EXPECTED_OLD_BLOB
    assert git_blob_sha(after_text.encode("utf-8")) == EXPECTED_FIXED_BLOB


def test_rejects_unreviewed_fixture_test(tmp_path: Path) -> None:
    root = fixture_root(tmp_path)
    target = root / TARGET
    target.write_bytes(target.read_bytes() + b"\n# tampering\n")
    with pytest.raises(RuntimeError, match="R64R2_UNREVIEWED_TARGET_BLOB"):
        review(root)


def test_rejects_modified_audit_source(tmp_path: Path) -> None:
    root = fixture_root(tmp_path)
    target = root / next(iter(PINNED_UNCHANGED))
    target.write_bytes(target.read_bytes() + b"\n# tampering\n")
    with pytest.raises(RuntimeError, match="R64R2_REVIEWED_SOURCE_MISMATCH"):
        review(root)


def test_rejects_double_crlf(tmp_path: Path) -> None:
    root = fixture_root(tmp_path, eol="crlf")
    target = root / TARGET
    target.write_bytes(target.read_bytes().replace(b"\n", b"\r\n"))
    with pytest.raises(RuntimeError, match="R64R2_UNEXPECTED_CR_ONLY_OR_DOUBLE_CR"):
        review(root)


def test_rejects_unrelated_function() -> None:
    with pytest.raises(RuntimeError, match="R64R2_UNREVIEWED_OR_AMBIGUOUS_FUNCTION"):
        patch_test("def unrelated():\n    pass\n")
```

## 新規 `run.ps1`（全文）

```powershell
[CmdletBinding()]
param([switch]$DryRun)

$ErrorActionPreference = 'Stop'
$Root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Push-Location $Root
try {
    $module = 'phase174_r3_r7_r64r2_crlf_fixture_test_fix.install'
    if ($DryRun) {
        python -B -m $module --dry-run
        if ($LASTEXITCODE -ne 0) { throw 'R64R2 source guard failed' }
        python -B -m phase174_r3_r7_r64_sentence_coverage_frontier_audit.audit --dry-run
        if ($LASTEXITCODE -ne 0) { throw 'R64 preflight after R64R2 failed' }
        Write-Output 'PHASE174_R64R2_GATE=PASS_R64R2_DRYRUN'
        Write-Output '(END)'
    } else {
        python -B -m $module
        if ($LASTEXITCODE -ne 0) { throw 'R64R2 installer failed' }
        python -B -m phase174_r3_r7_r64_sentence_coverage_frontier_audit.audit
        if ($LASTEXITCODE -ne 0) { throw 'R64 coverage audit failed' }
        python -B -m pytest -q -o addopts= -p no:cacheprovider --import-mode=importlib `
            'phase174_r3_r7_r64r2_crlf_fixture_test_fix/tests/test_install.py' `
            'phase174_r3_r7_r64r1_pytest_tmp_path_fix/tests/test_install.py' `
            'phase174_r3_r7_r64_sentence_coverage_frontier_audit/tests/test_audit.py' `
            'phase174_r3_r7_r63_sentence_witness_audit/tests/test_audit.py'
        if ($LASTEXITCODE -ne 0) { throw 'R64R2 focused pytest failed' }
        Write-Output 'PHASE174_R64R2_GATE=PASS_R64R2_FOCUSED_AND_R64_COVERAGE_FRONTIER'
        Write-Output '(END)'
    }
}
finally {
    Pop-Location
}
```
