# Phase 174 R64R1 — 変更単位のコード全文

## 変更したテスト関数

対象ファイル：`phase174_r3_r7_r64_sentence_coverage_frontier_audit/tests/test_audit.py`

この関数の既存位置で全文置換。import は変更しません（既存の `from pathlib import Path`, `import pytest`, `source_guard`, `PINS` を使用）。

```python
def test_source_guard_rejects_tamper(tmp_path: Path) -> None:
    relative = next(iter(PINS))
    target = tmp_path / relative
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes(b"unreviewed")
    with pytest.raises(RuntimeError, match="R64_SOURCE_BLOB_MISMATCH"):
        source_guard(tmp_path)
```

## 新規追加ファイルと追加位置

`phase174_r3_r7_r64r1_pytest_tmp_path_fix/` を repository ルート直下に追加。

### install.py 全文

```python
"""Fix only R64's tmp_path mkdir precondition; all audited sources remain pinned."""
from __future__ import annotations

import argparse
import ast
from hashlib import sha1
from pathlib import Path
import subprocess

PACKAGE = "phase174_r3_r7_r64r1_pytest_tmp_path_fix"
TARGET = "phase174_r3_r7_r64_sentence_coverage_frontier_audit/tests/test_audit.py"
PINNED_UNCHANGED = {
    "phase174_r3_r7_r64_sentence_coverage_frontier_audit/audit.py": "639b2290aeb09ead23367d0ed8a02e8f64ad6d6f",
    "phase174_r3_r7_r64_sentence_coverage_frontier_audit/run.ps1": "3b3f31425f06213136fe88492fe8402ba90fb4c8",
}
EXPECTED_OLD_BLOB = "cd415c6f60f2a20ac2a49c9ccea8619afdae0e28"
EXPECTED_FIXED_BLOB = "3122053b18dd87c57e78c2d4385f01852b51c708"
ORIGINAL_FUNCTION = 'def test_source_guard_rejects_tamper(tmp_path: Path) -> None:\n    relative = next(iter(PINS))\n    target = tmp_path / relative\n    target.parent.mkdir(parents=True)\n    target.write_bytes(b"unreviewed")\n    with pytest.raises(RuntimeError, match="R64_SOURCE_BLOB_MISMATCH"):\n        source_guard(tmp_path)\n'
REPLACEMENT_FUNCTION = 'def test_source_guard_rejects_tamper(tmp_path: Path) -> None:\n    relative = next(iter(PINS))\n    target = tmp_path / relative\n    target.parent.mkdir(parents=True, exist_ok=True)\n    target.write_bytes(b"unreviewed")\n    with pytest.raises(RuntimeError, match="R64_SOURCE_BLOB_MISMATCH"):\n        source_guard(tmp_path)\n'


def git_blob_sha(data: bytes) -> str:
    """Hash the exact bytes as a Git blob."""
    return sha1(b"blob " + str(len(data)).encode("ascii") + b"\x00" + data).hexdigest()


def normalized_contents(data: bytes) -> tuple[str, bytes, str]:
    """Allow whole-file LF or CRLF, preserve a UTF-8 BOM, reject CR-only."""
    bom = b"\xef\xbb\xbf" if data.startswith(b"\xef\xbb\xbf") else b""
    remainder = data[len(bom):]
    if b"\r" in remainder.replace(b"\r\n", b""):
        raise RuntimeError("R64R1_UNEXPECTED_CR_ONLY")
    eol = "\r\n" if b"\r\n" in remainder else "\n"
    return remainder.decode("utf-8").replace("\r\n", "\n"), bom, eol


def patch_test(source: str) -> str:
    """Replace one fully verified function, not an arbitrary mkdir occurrence."""
    parsed = ast.parse(source)
    matches = [item for item in parsed.body
               if isinstance(item, ast.FunctionDef)
               and item.name == "test_source_guard_rejects_tamper"]
    if len(matches) != 1 or source.count(ORIGINAL_FUNCTION) != 1:
        raise RuntimeError("R64R1_UNREVIEWED_OR_AMBIGUOUS_FUNCTION")
    patched = source.replace(ORIGINAL_FUNCTION, REPLACEMENT_FUNCTION, 1)
    ast.parse(patched)
    if patched.replace(REPLACEMENT_FUNCTION, ORIGINAL_FUNCTION, 1) != source:
        raise RuntimeError("R64R1_PATCH_NOT_MINIMAL")
    return patched


def review(root: Path) -> tuple[str, bytes, bytes]:
    """Pin the original audit, test and runner independently of repository HEAD."""
    if not root.is_dir():
        raise RuntimeError("R64R1_REPOSITORY_DIRECTORY_MISSING")
    for relative, expected in PINNED_UNCHANGED.items():
        path = root / relative
        if not path.is_file():
            raise RuntimeError("R64R1_REQUIRED_FILE_MISSING: " + relative)
        content, _bom, _eol = normalized_contents(path.read_bytes())
        if git_blob_sha(content.encode("utf-8")) != expected:
            raise RuntimeError("R64R1_UNREVIEWED_SOURCE: " + relative)
    target = root / TARGET
    if not target.is_file():
        raise RuntimeError("R64R1_TEST_FILE_MISSING")
    original = target.read_bytes()
    content, bom, eol = normalized_contents(original)
    current_hash = git_blob_sha(content.encode("utf-8"))
    if current_hash == EXPECTED_OLD_BLOB:
        revised = patch_test(content)
        if git_blob_sha(revised.encode("utf-8")) != EXPECTED_FIXED_BLOB:
            raise RuntimeError("R64R1_UNEXPECTED_REPLACEMENT_BLOB")
        status = "PATCH_REQUIRED"
    elif current_hash == EXPECTED_FIXED_BLOB:
        if content.count(REPLACEMENT_FUNCTION) != 1:
            raise RuntimeError("R64R1_FIXED_FUNCTION_MISSING")
        revised = content
        status = "ALREADY_APPLIED"
    else:
        raise RuntimeError("R64R1_UNREVIEWED_TEST_BLOB: " + current_hash)
    after = bom + revised.replace("\n", eol).encode("utf-8")
    return status, original, after


def git_local_head(root: Path) -> str:
    result = subprocess.run(["git", "rev-parse", "HEAD"], cwd=root,
                            text=True, capture_output=True, check=False)
    if result.returncode:
        raise RuntimeError("R64R1_GIT_HEAD_UNAVAILABLE")
    return result.stdout.strip()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true")
    options = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    status, original, after = review(root)
    head = git_local_head(root)
    print("PHASE174_R64R1_SOURCE_GUARD=PASS")
    print("PHASE174_R64R1_SOURCE_PINS=3")
    print("PHASE174_R64R1_LOCAL_HEAD=" + head)
    print("PHASE174_R64R1_PATCH_STATUS=" + status)
    print("PHASE174_R64R1_PRODUCTION_CHANGES=0")
    print("PHASE174_R64R1_NEW_GIVEN=0")
    print("PHASE174_R64R1_NEW_MATHEMATICAL_RULES=0")
    if options.dry_run:
        print("PHASE174_R64R1_GATE=PASS_R64R1_READ_ONLY_DRYRUN")
        print("(END)")
        return 0
    if original != after:
        (root / TARGET).write_bytes(after)
        actual = (root / TARGET).read_bytes()
        if actual != after:
            raise RuntimeError("R64R1_INSTALL_VERIFY_FAILED")
    print("PHASE174_R64R1_GATE=PASS_R64R1_PATCH_APPLIED_OR_PRESENT")
    print("(END)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

### tests/test_install.py 全文

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


def create_review_fixture(tmp_path: Path, source: str = ORIGINAL_FUNCTION) -> Path:
    """Construct only the pinned inputs; do not mutate production or Git state."""
    from phase174_r3_r7_r64r1_pytest_tmp_path_fix.install import normalized_contents
    real_root = Path(__file__).resolve().parents[2]
    for relative in PINNED_UNCHANGED:
        original = real_root / relative
        destination = tmp_path / relative
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_bytes(original.read_bytes())
    real_source = (real_root / TARGET).read_bytes()
    actual, _bom, _eol = normalized_contents(real_source)
    fixed_or_original = actual.replace(REPLACEMENT_FUNCTION, ORIGINAL_FUNCTION)
    destination = tmp_path / TARGET
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(fixed_or_original if source == ORIGINAL_FUNCTION else source, encoding="utf-8")
    return tmp_path


def test_original_and_patched_hashes_match_contract(tmp_path: Path) -> None:
    create_review_fixture(tmp_path)
    source = (tmp_path / TARGET).read_text(encoding="utf-8")
    assert git_blob_sha(source.encode("utf-8")) == EXPECTED_OLD_BLOB
    patched = patch_test(source)
    assert git_blob_sha(patched.encode("utf-8")) == EXPECTED_FIXED_BLOB
    assert patched.replace(REPLACEMENT_FUNCTION, ORIGINAL_FUNCTION) == source
    assert patched.count(REPLACEMENT_FUNCTION) == 1


def test_review_accepts_original_then_patched_and_does_not_mutate(tmp_path: Path) -> None:
    create_review_fixture(tmp_path)
    status, original, after = review(tmp_path)
    assert status == "PATCH_REQUIRED"
    assert original != after
    assert (tmp_path / TARGET).read_bytes() == original
    (tmp_path / TARGET).write_bytes(after)
    status2, original2, after2 = review(tmp_path)
    assert status2 == "ALREADY_APPLIED"
    assert original2 == after2 == after


def test_patch_rejects_unrelated_or_modified_functions() -> None:
    for source in ("def unrelated():\n    pass\n",
                   ORIGINAL_FUNCTION.replace("target.write_bytes", "target.touch"),
                   ORIGINAL_FUNCTION + ORIGINAL_FUNCTION):
        with pytest.raises(RuntimeError):
            patch_test(source)


def test_review_rejects_unreviewed_test_blob(tmp_path: Path) -> None:
    create_review_fixture(tmp_path)
    target = tmp_path / TARGET
    target.write_bytes(target.read_bytes() + b"\n# unreviewed\n")
    with pytest.raises(RuntimeError, match="R64R1_UNREVIEWED_TEST_BLOB"):
        review(tmp_path)


def test_review_rejects_modified_audit_file(tmp_path: Path) -> None:
    create_review_fixture(tmp_path)
    relative = next(iter(PINNED_UNCHANGED))
    target = tmp_path / relative
    target.write_bytes(target.read_bytes() + b"\n# unreviewed\n")
    with pytest.raises(RuntimeError, match="R64R1_UNREVIEWED_SOURCE"):
        review(tmp_path)


def test_review_accepts_crlf_line_endings(tmp_path: Path) -> None:
    create_review_fixture(tmp_path)
    target = tmp_path / TARGET
    target.write_bytes(target.read_bytes().replace(b"\n", b"\r\n"))
    status, _original, after = review(tmp_path)
    assert status == "PATCH_REQUIRED"
    assert b"\r\n" in after
    target.write_bytes(after)
    assert review(tmp_path)[0] == "ALREADY_APPLIED"
```

### run.ps1 全文

```powershell
[CmdletBinding()]
param([switch]$DryRun)

$ErrorActionPreference = 'Stop'
$Root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Push-Location $Root
try {
    $module = 'phase174_r3_r7_r64r1_pytest_tmp_path_fix.install'
    if ($DryRun) {
        python -B -m $module --dry-run
        if ($LASTEXITCODE -ne 0) { throw 'R64R1 source guard failed' }
        python -B -m phase174_r3_r7_r64_sentence_coverage_frontier_audit.audit --dry-run
        if ($LASTEXITCODE -ne 0) { throw 'R64 preflight after R64R1 failed' }
        Write-Output 'PHASE174_R64R1_GATE=PASS_R64R1_DRYRUN'
        Write-Output '(END)'
    } else {
        python -B -m $module
        if ($LASTEXITCODE -ne 0) { throw 'R64R1 installer failed' }
        python -B -m phase174_r3_r7_r64_sentence_coverage_frontier_audit.audit
        if ($LASTEXITCODE -ne 0) { throw 'R64 public coverage audit failed' }
        python -B -m pytest -q -o addopts= -p no:cacheprovider --import-mode=importlib `
            'phase174_r3_r7_r64r1_pytest_tmp_path_fix/tests/test_install.py' `
            'phase174_r3_r7_r64_sentence_coverage_frontier_audit/tests/test_audit.py' `
            'phase174_r3_r7_r63_sentence_witness_audit/tests/test_audit.py'
        if ($LASTEXITCODE -ne 0) { throw 'R64R1 focused pytest failed' }
        Write-Output 'PHASE174_R64R1_GATE=PASS_R64R1_FOCUSED_AND_R64_COVERAGE_FRONTIER'
        Write-Output '(END)'
    }
}
finally {
    Pop-Location
}
```
