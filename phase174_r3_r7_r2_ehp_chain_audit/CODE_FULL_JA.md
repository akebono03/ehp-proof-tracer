# Phase 174 R3-R7-R2R1 変更コード全文

変更対象は `phase174_r3_r7_r2_ehp_chain_audit/` 内に限定する。既存本体・他 Phase のテストは変更しない。

## 変更ファイル・関数

- `run.ps1`：ファイル全文置換。
- `audit.py`：定数 `PREVIOUS_AUDIT_HEAD`、`REVIEWED_HEAD`、関数 `validate_sources()` と `validate_previous_report()`。他の import・関数・クラスには変更なし。
- `tests/test_contract.py`：import の全文、`previous_snapshot()`、新規 `test_r2_guard_uses_new_head_but_r1_report_retains_old_head()`。
- `tests/test_runner_import_mode.py`：新規。`tests/test_repo.py` と既存の Phase165 / Phase173 テストは変更しない。
- `README.md`：ファイル全文。英語で記載。

追加位置は新規 `tests/test_runner_import_mode.py` と `test_contract.py` 末尾の新規テストである。

## run.ps1 （全文）

```powershell
param(
    [switch]$DryRun
)

$ErrorActionPreference = 'Stop'
$RepoRoot = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
$PreviousPythonPath = $env:PYTHONPATH
$PreviousNoBytecode = $env:PYTHONDONTWRITEBYTECODE

Push-Location -LiteralPath $RepoRoot
try {
    $env:PYTHONPATH = $RepoRoot
    $env:PYTHONDONTWRITEBYTECODE = '1'

    $FocusedTests = @(
        'phase174_r3_r7_r2_ehp_chain_audit/tests/test_contract.py',
        'phase174_r3_r7_r2_ehp_chain_audit/tests/test_repo.py',
        'phase174_r3_r7_r2_ehp_chain_audit/tests/test_runner_import_mode.py',
        'phase174_r3_r7_r1_zero_root_audit/tests/test_audit.py',
        'phase165_r12_r11_prop42_unified/tests/test_phase165_r12_r11_prop42_unified.py',
        'phase165_r12_r12_ehp_consequences/tests/test_phase165_r12_r12_ehp_consequences.py',
        'phase165_r14_r6_generic_iso/test_phase165_r14_r6_generic_iso.py',
        'phase173_r4_r11_zero_public_connection/tests/test_route.py'
    )
    foreach ($TestFile in $FocusedTests) {
        if (-not (Test-Path -LiteralPath $TestFile)) {
            throw "Missing focused test: $TestFile"
        }
    }

    # importlib would insert namespace packages for sibling directories named
    # like phase165_r12_r11_prop42_unified.py, shadowing actual source modules.
    # prepend imports those test files as modules without the namespace collision.
    Write-Output 'PHASE174_R3R7R2_FOCUSED_PYTEST_START'
    & python -B -m pytest -q --import-mode=prepend -p no:cacheprovider @FocusedTests
    if ($LASTEXITCODE -ne 0) {
        throw 'Phase 174 R3-R7-R2 focused pytest failed'
    }
    Write-Output 'PHASE174_R3R7R2_FOCUSED_PYTEST=PASS'

    if ($DryRun) {
        & python -B -m phase174_r3_r7_r2_ehp_chain_audit.audit --dry-run
    } else {
        & python -B -m phase174_r3_r7_r2_ehp_chain_audit.audit
    }
    if ($LASTEXITCODE -ne 0) {
        throw 'Phase 174 R3-R7-R2 audit failed'
    }
}
finally {
    $env:PYTHONPATH = $PreviousPythonPath
    $env:PYTHONDONTWRITEBYTECODE = $PreviousNoBytecode
    Pop-Location
}
```

## audit.py 変更後の定数

```python
PREVIOUS_AUDIT_HEAD = "992975395195a0e49955617ba1ae772127036dde"
REVIEWED_HEAD = "c055e8ddddaee2c0d0552bbdcc3e3afc62b6ff9c"
```

## audit.py — validate_sources() 全文

```python
def validate_sources(root: Path = ROOT) -> dict[str, Any]:
    actual_root = Path(command("git", "rev-parse", "--show-toplevel", cwd=root)).resolve()
    if actual_root != root.resolve():
        raise RuntimeError("Audit package must be directly beneath the repository root")
    branch = command("git", "branch", "--show-current", cwd=root)
    local_head = command("git", "rev-parse", "HEAD", cwd=root)
    remote_line = command("git", "ls-remote", "origin", "refs/heads/develop", cwd=root)
    remote_head = remote_line.split()[0] if remote_line else ""
    if branch != "develop" or remote_head != REVIEWED_HEAD:
        raise RuntimeError("Git develop HEAD changed or is not at the reviewed baseline")
    if local_head not in (PREVIOUS_AUDIT_HEAD, REVIEWED_HEAD):
        raise RuntimeError("Local HEAD is outside the audited two-commit lineage")
    ancestor = command(
        "git", "merge-base", PREVIOUS_AUDIT_HEAD, REVIEWED_HEAD, cwd=root
    )
    if ancestor != PREVIOUS_AUDIT_HEAD:
        raise RuntimeError("The prior R1 audit baseline is not an ancestor")
    changed_paths = command(
        "git", "diff", "--name-only", PREVIOUS_AUDIT_HEAD, REVIEWED_HEAD,
        cwd=root,
    ).splitlines()
    if not changed_paths or any(
        not path.startswith("phase174_r3_r7_r1_zero_root_audit/")
        for path in changed_paths
    ):
        raise RuntimeError("Unexpected changes in reviewed Git HEAD lineage")
    staged = command("git", "diff", "--cached", "--name-only", cwd=root)
    if staged:
        raise RuntimeError("Staged changes require a separate review")
    for relative, sha in SOURCE_BLOBS.items():
        file = root / relative
        if not file.is_file() or not matches_git_blob(file.read_bytes(), sha):
            raise RuntimeError("Source Guard failed for " + relative)
    return {
        "branch": branch,
        "local_head": local_head,
        "remote_head": remote_head,
        "previous_audit_head": PREVIOUS_AUDIT_HEAD,
        "reviewed_lineage_paths": changed_paths,
        "source_guard_files": len(SOURCE_BLOBS),
        "staged_changes": [],
        "working_tree_status": command(
            "git", "status", "--porcelain=v1", "--untracked-files=normal", cwd=root
        ).splitlines(),
    }
```

## audit.py — validate_previous_report() 全文

```python
def validate_previous_report(report: dict[str, Any]) -> dict[str, Any]:
    if report.get("phase") != "174-R3-R7-R1":
        raise RuntimeError("Wrong prior audit phase")
    if report.get("gate") != "PASS_READ_ONLY_ZERO_ROOT_DIAGNOSTIC":
        raise RuntimeError("Prior zero-root audit did not pass")
    state = report.get("git_state", {})
    if state.get("remote_head") != PREVIOUS_AUDIT_HEAD or state.get("local_head") != PREVIOUS_AUDIT_HEAD:
        raise RuntimeError("Prior zero-root audit HEAD differs")
    live = report.get("live_zero_root") or {}
    zero = live.get("zero_root") or {}
    if (zero.get("proposal_count") != 0
            or live.get("preceding_group") != "pi_11^6"
            or live.get("preceding_group_status") != "search_failed"
            or live.get("zero_search_status") != "search_failed"
            or live.get("direct_zero_target_given") is not False):
        raise RuntimeError("R3-R7-R1 measured zero-root/prior state differs")
    if report.get("new_inference_rules") != 0 or report.get("new_group_given") != 0:
        raise RuntimeError("Prior audit has new rules or GIVENs")
    return {
        "prior_gate": report["gate"],
        "zero_root_proposal_count": 0,
        "precursor": "pi_11^6",
        "precursor_status": "search_failed",
        "source_context": live.get("screening_path"),
    }
```

## tests/test_contract.py — import 全文

```python
"""Pure, repository-independent contracts for R3-R7-R2 read-only audit."""
from __future__ import annotations

import ast
import json
from pathlib import Path

import pytest

from phase174_r3_r7_r2_ehp_chain_audit.audit import (
    REVIEWED_HEAD,
    PREVIOUS_AUDIT_HEAD,
    SOURCE_BLOBS,
    SOURCE_EXCERPTS,
    classify_proposals,
    ehp_chain_dimensions,
    git_blob_sha,
    matches_git_blob,
    validate_previous_report,
    verify_toda_transcription,
)
```

## tests/test_contract.py — previous_snapshot() 全文

```python
def previous_snapshot() -> dict:
    return {
        "phase": "174-R3-R7-R1",
        "gate": "PASS_READ_ONLY_ZERO_ROOT_DIAGNOSTIC",
        "git_state": {
            "remote_head": PREVIOUS_AUDIT_HEAD,
            "local_head": PREVIOUS_AUDIT_HEAD,
        },
        "live_zero_root": {
            "zero_root": {"proposal_count": 0},
            "preceding_group": "pi_11^6",
            "preceding_group_status": "search_failed",
            "zero_search_status": "search_failed",
            "direct_zero_target_given": False,
            "screening_path": "independent_source_screened_shared_provider",
        },
        "new_group_given": 0,
        "new_inference_rules": 0,
    }
```

## tests/test_contract.py — 新規テスト全文

```python
def test_r2_guard_uses_new_head_but_r1_report_retains_old_head() -> None:
    assert PREVIOUS_AUDIT_HEAD == "992975395195a0e49955617ba1ae772127036dde"
    assert REVIEWED_HEAD == "c055e8ddddaee2c0d0552bbdcc3e3afc62b6ff9c"
    assert PREVIOUS_AUDIT_HEAD != REVIEWED_HEAD
    prior = validate_previous_report(previous_snapshot())
    assert prior["prior_gate"] == "PASS_READ_ONLY_ZERO_ROOT_DIAGNOSTIC"
```

## tests/test_runner_import_mode.py — 全文

```python
"""Regression: pytest must not shadow same-name production Python modules."""
from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path


def _create_collision_fixture(root: Path) -> Path:
    module = root / "phase165_r12_r11_prop42_unified.py"
    module.write_text("GENERAL_ASSERTION_ID = 'present'\n", encoding="utf-8")
    sibling = root / "phase165_r12_r11_prop42_unified" / "tests"
    sibling.mkdir(parents=True)
    test = sibling / "test_source_module.py"
    test.write_text(
        "from phase165_r12_r11_prop42_unified import GENERAL_ASSERTION_ID\n"
        "def test_import():\n"
        "    assert GENERAL_ASSERTION_ID == 'present'\n",
        encoding="utf-8",
    )
    return test


def _run_fixture(root: Path, test: Path, import_mode: str) -> subprocess.CompletedProcess[str]:
    env = dict(os.environ)
    env["PYTHONPATH"] = str(root)
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    return subprocess.run(
        (
            sys.executable, "-B", "-m", "pytest", "-q",
            "--import-mode=" + import_mode, "-p", "no:cacheprovider",
            str(test),
        ),
        cwd=root,
        env=env,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        check=False,
    )


def test_same_named_directory_causes_importlib_collection_error(tmp_path: Path) -> None:
    test = _create_collision_fixture(tmp_path)
    result = _run_fixture(tmp_path, test, "importlib")
    assert result.returncode != 0
    assert "cannot import name" in result.stdout or "cannot import name" in result.stderr


def test_prepend_recovers_source_module_import(tmp_path: Path) -> None:
    test = _create_collision_fixture(tmp_path)
    result = _run_fixture(tmp_path, test, "prepend")
    assert result.returncode == 0, result.stdout + "\n" + result.stderr
    assert "1 passed" in result.stdout


def test_powershell_runner_selects_safe_import_mode() -> None:
    runner = Path(__file__).resolve().parents[1] / "run.ps1"
    contents = runner.read_text(encoding="utf-8")
    assert "--import-mode=prepend" in contents
    assert "--import-mode=importlib" not in contents
    assert "-p no:cacheprovider" in contents
    assert "'phase165_r12_r11_prop42_unified/tests/test_phase165_r12_r11_prop42_unified.py'" in contents
    assert "'phase165_r12_r12_ehp_consequences/tests/test_phase165_r12_r12_ehp_consequences.py'" in contents
    assert "'phase165_r14_r6_generic_iso/test_phase165_r14_r6_generic_iso.py'" in contents
```

## README.md — 全文（英語）

```markdown
# Phase 174 R3-R7-R2R1 — pytest collection and head-lineage repair

This repair addresses a test-collection failure, not a mathematical proof failure. Several historical Phase 165 test directories have the same import name as a root-level Python source module. Under pytest `--import-mode=importlib`, that test-directory namespace may shadow the module. The focused test runner now selects `--import-mode=prepend` and keeps bytecode/cache output disabled. The same focused test files are preserved and an import-mode regression test is added.

## Reviewed Git lineage

The R3-R7-R1 report records commit `992975395195a0e49955617ba1ae772127036dde`. GitHub `develop` advanced to `c055e8ddddaee2c0d0552bbdcc3e3afc62b6ff9c` solely by adding the R3-R7-R1 audit package. The R2 report guard checks that exact commit ancestry and that all intervening paths belong to that audit package, in addition to checking nine unchanged mathematical source blobs. Both baseline local HEAD values are accepted; no checkout or commit is performed. Newer GitHub commits require a new review and are not silently accepted.

## Scope

Only files within `phase174_r3_r7_r2_ehp_chain_audit/` are replaced or added: `run.ps1`, `audit.py`, `tests/test_contract.py`, `tests/test_runner_import_mode.py`, `README.md`, and `CODE_FULL_JA.md`. Other R2 audit files are preserved identically in the bundled replacement. Existing production modules, historical test files, mathematical rules, literature assertions, and common renderer are not changed.

## Run

Unzip from the repository root, then invoke `run.ps1 -DryRun` followed by `run.ps1`. Both modes run focused pytest before the read-only audit. The saved R3-R7-R1 report is required. The R2 report is written outside the Git repository under `%LOCALAPPDATA%\EHPProofTracerAudit\phase174_r3_r7_r2\ehp_chain_audit.json`. No full pytest suite is run.

## Completion

Focused pytest and both audit modes must pass. The live report must list exactness, Delta-map and predecessor proof obligations without claiming candidates are completed proofs or adding target-specific GIVENs. The following R3-R7-R3 phase may consider new general inference only after inspecting the measured evidence and source ancestry.
```

## 限定 pytest と完了条件

`run.ps1` 内の `$FocusedTests` に限定した pytest を `--import-mode=prepend -p no:cacheprovider` で実行する。DryRun、本監査、Source Guard の PASS と Root 候補・未解決 Goal の JSON 出力を確認する。Phase 174 完了まで全体 pytest は行わない。R3-R7-R3 の新推論規則は先取りしない。
