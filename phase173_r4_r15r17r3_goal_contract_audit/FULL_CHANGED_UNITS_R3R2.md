# Phase 173 R15R17-R3R2 complete changed units

`audit.py` retains its existing import block (shown unchanged below).
The new `count_canonical_reference_headings()` is inserted immediately before
`audit_real_cases()`. Both functions are shown in full, without omissions.

## Imports (`audit.py`, unchanged)

```python
"""Audit typed open-goal identities and historical public display contracts.

No proof states, proof steps, goals, citations, or production files are modified.
"""
from __future__ import annotations

import argparse
import ast
from hashlib import sha256
import json
from pathlib import Path
from typing import Any, Callable

```

## Full helper and complete `audit_real_cases()`

```python
def count_canonical_reference_headings(markdown: str, *, complete: bool) -> int:
    """Count the Reference heading emitted by the unchanged common renderer.

    Completed proof Markdown uses an undecorated heading, whereas incomplete
    proof Markdown uses a second-level Markdown heading. Do not mistake zero
    occurrences of the *wrong* heading for duplicate References.
    """
    if not isinstance(markdown, str):
        raise TypeError("rendered Markdown must be a string")
    if type(complete) is not bool:
        raise TypeError("complete must be a bool")
    expected = "使用する結果" if complete else "## 使用する結果"
    other = "## 使用する結果" if complete else "使用する結果"
    lines = tuple(line.strip() for line in markdown.splitlines())
    if other in lines:
        raise ValueError("unexpected Reference heading for the proof status")
    return lines.count(expected)


def audit_real_cases() -> None:
    from phase165_r52_partial_proof import ProofSearchStatus
    from phase165_r55_nk_only_goal import search_group_from_registered_goal
    from phase168_r3_3_proof_narrative_model import build_proof_narrative_model
    from phase168_r3_5_model_renderer import render_model_backed_narrative_markdown
    from phase169_r10e4_ordered_db_prior.db_prior import exact_prior_database_result
    from web_group_proof_common import _group_proof_statement_latex

    def display(goal: object) -> str:
        if isinstance(goal, str):
            return goal
        latex, fallback = _group_proof_statement_latex(goal)
        return f"${latex}$" if latex is not None and fallback is None else f"<{type(goal).__name__}>"

    for n, k in ((4, 8), (4, 9), (5, 3), (4, 4)):
        typed_goal = exact_prior_database_result(n, k)
        result = search_group_from_registered_goal(n=n, k=k, goal=typed_goal)
        model = build_proof_narrative_model(result)
        markdown = render_model_backed_narrative_markdown(result, model)
        if model.open_goals != result.open_goals or model.status is not result.status:
            raise RuntimeError("model changed the original goal/status state")
        if model.abstract_structure is not result.abstract_structure:
            raise RuntimeError("model lost certificate identity")
        if result.status is ProofSearchStatus.COMPLETE:
            if result.open_goals or model.root_index is None:
                raise RuntimeError("completed proof lost its certified root")
        elif result.conclusion is not None or not result.open_goals:
            raise RuntimeError("incomplete proof has an invalid named-goal status")
        if model.abstract_structure is not None:
            if not any(step is model.abstract_structure.proof_step for step in model.steps):
                raise RuntimeError("certified abstract root missing from unified model")
        if any("## " + old in markdown for old in OLD_HEADINGS):
            raise RuntimeError("obsolete separate public section in canonical renderer")
        reference_sections = count_canonical_reference_headings(
            markdown, complete=result.status is ProofSearchStatus.COMPLETE,
        )
        if reference_sections != 1:
            raise RuntimeError(
                f"canonical Reference heading count is {reference_sections} "
                f"for n={n}, k={k}, status={result.status.value}"
            )
        if result.abstract_structure is not None and "\\cong" not in markdown:
            raise RuntimeError("certified abstract result not displayed")
        pair_report = inspect_goal_pairs(result.open_goals, display)
        output = {
            "n": n, "k": k, "status": result.status.value,
            "proven_steps": len(result.proven_steps),
            "model_steps": len(model.steps),
            "citations": len(model.citations),
            "abstract_certificate": result.abstract_structure is not None,
            "has_named_conclusion": result.conclusion is not None,
            "reference_sections": reference_sections,
            "open_goals": pair_report,
        }
        print("R15R17R3_GOAL_CASE=" + json.dumps(output, ensure_ascii=False, sort_keys=True))
    print("R15R17R3_RUNTIME_AUDIT=PASS")

```

## New test module, complete

```python
"""R3R2: one canonical Reference heading for each renderer status.

These tests deliberately inspect the *existing* complete and partial heading
formats. They do not change proof states, renderer output, or cited steps.
"""
from __future__ import annotations

import pytest

from phase173_r4_r15r17r3_goal_contract_audit.audit import (
    count_canonical_reference_headings,
)


def test_incomplete_reference_heading_is_counted_once() -> None:
    markdown = "## 証明対象\n\n## 使用する結果\n\n**[R1] Lemma.**\n"
    assert count_canonical_reference_headings(markdown, complete=False) == 1


def test_completed_reference_heading_is_counted_once() -> None:
    markdown = "使用する結果\n\n**[R1] Lemma.**\n\n証明\n"
    assert count_canonical_reference_headings(markdown, complete=True) == 1


def test_two_reference_headings_are_detected_as_duplicates() -> None:
    markdown = "## 使用する結果\n\n## 使用する結果\n"
    assert count_canonical_reference_headings(markdown, complete=False) == 2


def test_missing_reference_heading_is_distinguished_from_duplicates() -> None:
    assert count_canonical_reference_headings("## 証明\n", complete=False) == 0


def test_unexpected_heading_for_proof_status_is_rejected() -> None:
    with pytest.raises(ValueError, match="unexpected Reference heading"):
        count_canonical_reference_headings("使用する結果", complete=False)
    with pytest.raises(ValueError, match="unexpected Reference heading"):
        count_canonical_reference_headings("## 使用する結果", complete=True)


def test_reference_heading_contract_rejects_invalid_arguments() -> None:
    with pytest.raises(TypeError, match="Markdown"):
        count_canonical_reference_headings(None, complete=True)
    with pytest.raises(TypeError, match="complete"):
        count_canonical_reference_headings("使用する結果", complete=1)

```

No other existing classes, functions or imports change. `README.md` (English)
and `design.md` (Japanese) are included as complete files.

## Complete modified PowerShell `run.ps1`

The same safety guards, `git fetch` (read-only with respect to the worktree),
R2 integrity checks and index preservation remain unchanged. Only the
focused test command now includes the new six tests.

```powershell
param([switch]$DryRun)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'
$env:GIT_PAGER = 'cat'
$env:PAGER = 'cat'
$env:PYTHONDONTWRITEBYTECODE = '1'
$Root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
$ExpectedHead = 'aa25a9930d36b61e7588d1ef8e5916a766b569e6'

function Invoke-CheckedGit {
    param([string[]]$Arguments)
    $result = & git --no-pager @Arguments
    if ($LASTEXITCODE -ne 0) {
        throw ('Git command failed: git ' + ($Arguments -join ' '))
    }
    return $result
}

Push-Location $Root
try {
    $GitRoot = (Invoke-CheckedGit -Arguments @('rev-parse', '--show-toplevel')).Trim()
    $CanonicalGitRoot = [System.IO.Path]::GetFullPath($GitRoot)
    $CanonicalScriptRoot = [System.IO.Path]::GetFullPath($Root)
    if (-not [string]::Equals(
        $CanonicalGitRoot,
        $CanonicalScriptRoot,
        [System.StringComparison]::OrdinalIgnoreCase
    )) {
        throw 'Extract the R15R17-R3 audit ZIP at the Git repository root'
    }
    $Branch = (Invoke-CheckedGit -Arguments @('branch', '--show-current')).Trim()
    $Head = (Invoke-CheckedGit -Arguments @('rev-parse', 'HEAD')).Trim()
    if ($Branch -ne 'develop' -or $Head -ne $ExpectedHead) {
        throw ('R15R17-R3 requires develop at reviewed HEAD ' + $ExpectedHead + '; current branch=' + $Branch + '; current HEAD=' + $Head)
    }
    Write-Output ('R15R17R3_LOCAL_HEAD=' + $Head)
    Write-Output ('R15R17R3_REVIEWED_HEAD=' + $ExpectedHead)
    Write-Output 'R15R17R3_SCOPE=READ_ONLY_GOAL_AND_CONTRACT_AUDIT'
    Write-Output 'R15R17R3_PRODUCTION_WRITES=NONE'
    Write-Output 'R15R17R3_GIT_STAGE_RESET_CLEAN_COMMIT=NONE'
    Write-Output 'R15R17R3_FULL_PYTEST=False'

    $IndexBefore = (Invoke-CheckedGit -Arguments @('write-tree')).Trim()
    Invoke-CheckedGit -Arguments @('fetch', 'origin', 'develop') | Out-Null
    $Remote = (Invoke-CheckedGit -Arguments @('rev-parse', 'origin/develop')).Trim()
    Write-Output ('R15R17R3_REMOTE_HEAD=' + $Remote)
    if ($Remote -ne $ExpectedHead) {
        throw 'GitHub develop advanced; inspect changes before continuing'
    }

    Write-Output '=== R15R17-R3 FOCUSED CONTRACT TESTS ==='
    & python -B -m pytest -q -p no:cacheprovider `
      phase173_r4_r15r17r3_goal_contract_audit/tests/test_audit_helpers.py `
      phase173_r4_r15r17r3_goal_contract_audit/tests/test_head_guard.py `
      phase173_r4_r15r17r3_goal_contract_audit/tests/test_reference_heading_contract.py
    if ($LASTEXITCODE -ne 0) {
        throw 'R15R17-R3 focused contract tests failed'
    }
    Write-Output 'R15R17R3_FOCUSED_PYTEST=PASS'

    if ($DryRun) {
        & python -B -m phase173_r4_r15r17r3_goal_contract_audit.audit --dry-run
    }
    else {
        & python -B -m phase173_r4_r15r17r3_goal_contract_audit.audit
    }
    if ($LASTEXITCODE -ne 0) {
        throw 'R15R17-R3 audit program failed'
    }
    $IndexAfter = (Invoke-CheckedGit -Arguments @('write-tree')).Trim()
    if ($IndexBefore -ne $IndexAfter) {
        throw 'Git index was changed during R15R17-R3 audit'
    }
    Write-Output 'R15R17R3_GIT_INDEX_PRESERVED=PASS'
    if ($DryRun) {
        Write-Output 'R15R17R3_DRY_RUN=PASS'
    }
    else {
        Write-Output 'R15R17R3_AUDIT_COMPLETE=PASS'
    }
    Invoke-CheckedGit -Arguments @('status', '-sb')
}
finally {
    Pop-Location
}

```
