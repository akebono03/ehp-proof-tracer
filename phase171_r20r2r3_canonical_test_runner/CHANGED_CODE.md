# R20R2R3 — 変更コード全文

既存の本番コードおよび既存テストは変更しない。以下は新規ファイルの全文であり、省略はない。

## 追加位置

EHP Proof Tracer リポジトリのルート直下に `phase171_r20r2r3_canonical_test_runner/` を追加する。

## `anchored_pytest.py`（import・関数全文）

```python
"""Run existing focused pytest with the canonical ordered-citation module anchored.

The repository also contains an old module with the same basename inside the
historical test directory. Pytest's default prepend mode can import that old
module when it places the test directory at the front of sys.path. Preloading
the canonical root module prevents this accidental shadowing without changing
citation policy, source files, or existing tests.
"""
from __future__ import annotations

import argparse
import importlib
import sys
from pathlib import Path


PACKAGE_DIR = Path(__file__).resolve().parent
ROOT = PACKAGE_DIR.parent
CANONICAL_MODULE = "phase165_r52_r15_ordered_citation"
CANONICAL_FILE = ROOT / (CANONICAL_MODULE + ".py")
SEARCH_FILE = ROOT / "phase165_r3_recursive_search.py"
ORDERED_TEST = "phase165_r52_r15_ordered_citation/test_phase165_r52_r15_ordered_citation.py"
QUICK_TESTS = (
    ORDERED_TEST + "::test_ordered_reference_requires_only_prior_order",
    ORDERED_TEST + "::test_ordered_reference_integrates_with_backward_search",
)
FOCUSED_TESTS = (
    "phase171_r20r2_first_successful_search/tests/test_first_successful_search.py",
    "tests/test_phase165_r3_recursive_search.py",
    ORDERED_TEST,
    "phase165_r12_r33_proof_tree_dedup/test_phase165_r12_r33_proof_tree_dedup.py",
)


def check_canonical_import() -> None:
    """Pin the production module before pytest modifies import search paths."""
    if not CANONICAL_FILE.is_file():
        raise RuntimeError("canonical ordered-citation module not found")
    if not SEARCH_FILE.is_file():
        raise RuntimeError("recursive proof-search module not found")
    sys.path.insert(0, str(ROOT))
    module = importlib.import_module(CANONICAL_MODULE)
    module_path = Path(module.__file__).resolve()
    print("PHASE171_R20R2R3_CANONICAL_MODULE=" + str(module_path), flush=True)
    if module_path != CANONICAL_FILE.resolve():
        raise RuntimeError("wrong ordered-citation module; refusing pytest")
    function = getattr(module, "ordered_typed_reference_steps", None)
    if not callable(function):
        raise RuntimeError("canonical ordered-citation function missing")
    if Path(function.__code__.co_filename).resolve() != CANONICAL_FILE.resolve():
        raise RuntimeError("ordered-citation function originates from another file")
    required_globals = ("CitationDecision", "assess_citation", "AssertionOrigin")
    absent = tuple(name for name in required_globals if name not in function.__globals__)
    if absent:
        raise RuntimeError("unexpected canonical citation implementation: " + repr(absent))
    source = SEARCH_FILE.read_text(encoding="utf-8")
    if ("expected a verified registered derivation" not in source
            or "return accept(target, options[0])" not in source):
        raise RuntimeError("R20R2 First Successful Proof Search is not installed")
    print("PHASE171_R20R2R3_CANONICAL_ANCHOR=PASS", flush=True)
    print("PHASE171_R20R2R3_SOURCE_CHANGES=0", flush=True)


def main() -> int:
    """Validate the repository and execute only the existing focused tests."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--quick", action="store_true")
    args = parser.parse_args()
    try:
        check_canonical_import()
        selected = QUICK_TESTS if args.quick else FOCUSED_TESTS
        for node in selected:
            test_file = ROOT / node.split("::", 1)[0]
            if not test_file.is_file():
                raise RuntimeError("focused test not found: " + str(test_file))
        if args.dry_run:
            print("PHASE171_R20R2R3_DRY_RUN=PASS", flush=True)
            print("PHASE171_R20R2R3_TESTS=SKIPPED_DRY_RUN", flush=True)
            return 0
        import pytest
        mode = "quick" if args.quick else "focused"
        print("PHASE171_R20R2R3_TEST_MODE=" + mode, flush=True)
        result = int(pytest.main(["-q", "--tb=short", "-p", "no:cacheprovider", *selected]))
        print("PHASE171_R20R2R3_PYTEST_EXIT=" + str(result), flush=True)
        return result
    except (ImportError, OSError, RuntimeError, AttributeError) as exc:
        print("PHASE171_R20R2R3_PREFLIGHT=FAIL", flush=True)
        print("PHASE171_R20R2R3_REASON=" + str(exc), flush=True)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
```

## `run.ps1`（全文）

```powershell
param(
    [switch]$DryRun,
    [switch]$Quick
)

$ErrorActionPreference = 'Stop'
$Root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
$PreviousNoBytecode = $env:PYTHONDONTWRITEBYTECODE
Push-Location $Root
try {
    $Branch = (& git branch --show-current).Trim()
    $Head = (& git rev-parse HEAD).Trim()
    Write-Host ('PHASE171_R20R2R3_BRANCH=' + $Branch)
    Write-Host ('PHASE171_R20R2R3_HEAD=' + $Head)
    if ($Branch -ne 'develop') {
        throw 'Expected develop branch. No files were changed.'
    }
    $env:PYTHONDONTWRITEBYTECODE = '1'
    $Arguments = @('-B', '.\phase171_r20r2r3_canonical_test_runner\anchored_pytest.py')
    if ($DryRun) { $Arguments += '--dry-run' }
    if ($Quick) { $Arguments += '--quick' }
    & python @Arguments
    $PythonExit = $LASTEXITCODE
    if ($PythonExit -ne 0) {
        throw ('R20R2R3 check failed with exit code ' + $PythonExit)
    }
    if (-not $DryRun) {
        Write-Host 'PHASE171_R20R2R3_RESULT=PASS'
        & git status -sb
        & git diff --stat
    }
} finally {
    if ($null -eq $PreviousNoBytecode) {
        Remove-Item Env:PYTHONDONTWRITEBYTECODE -ErrorAction SilentlyContinue
    } else {
        $env:PYTHONDONTWRITEBYTECODE = $PreviousNoBytecode
    }
    Pop-Location
}
```

実行前後の既存 API や推論・引用資格判定は不変。テスト関数の追加・変更もない。
