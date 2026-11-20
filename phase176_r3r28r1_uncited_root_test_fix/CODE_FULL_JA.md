# Phase 176 R3R28R1 コード全文

## 変更後のテストファイル全文

```python
"""Phase 176 R3R28 focused contracts for source-first public wiring."""
from __future__ import annotations

from pathlib import Path

import pytest

from phase176_r3r28_toda55_quadruple_public import install
from phase176_r3r27r1_toda55_quadruple_isolated.source import (
    Toda55UniversalQuadrupleStatement,
    canonical_quadruple_goal,
)
from proof import ProofRule


def test_patch_both_functions_and_idempotent() -> None:
    current = install.TARGET.read_text(encoding="utf-8-sig")
    result = install.proposed(current.replace("\r\n", "\n"))
    functions = install.functions_in(result)
    assert "build_cited_toda55_quadruple_source" in functions["build_shared_typed_bridge"]
    assert "expand_public_toda55_quadruple" in functions["shared_expansion_provider"]
    assert install.proposed(result) == result


def test_partial_patch_fails_closed() -> None:
    current = install.TARGET.read_text(encoding="utf-8-sig").replace("\r\n", "\n")
    without = current.replace(install.PROVIDER_PATCH, "")
    if install.SOURCE_PATCH in without:
        with pytest.raises(RuntimeError, match="PARTIAL_PATCH_DETECTED"):
            install.proposed(without)


def test_full_source_contains_complete_functions() -> None:
    current = install.TARGET.read_text(encoding="utf-8-sig").replace("\r\n", "\n")
    text = install.full_code_md(install.proposed(current))
    assert "def build_shared_typed_bridge" in text
    assert "def shared_expansion_provider" in text


def test_default_shared_bridge_has_one_screened_quadruple_source() -> None:
    from phase165_r52_r9_shared_math import build_shared_typed_bridge
    from phase165_r55_nk_only_goal import registered_group_goal_candidates
    from phase169_r10e2_unpositioned_citation.source_first import (
        screen_independent_sources_for_derived_goal,
    )
    bridge = build_shared_typed_bridge()
    roots = registered_group_goal_candidates(bridge, n=3, k=5)
    assert len(roots) == 1
    screened = screen_independent_sources_for_derived_goal(bridge, goal=roots[0])
    statements = tuple(link.step.conclusion for link in screened.proof_links
                       if link.step is not None and link.step.rule is ProofRule.GIVEN)
    assert statements.count(Toda55UniversalQuadrupleStatement()) == 1
    assert roots[0] not in statements


def test_shared_provider_proposes_and_proves_nu5_quadruple() -> None:
    from phase165_r52_r9_shared_math import build_shared_typed_bridge, shared_expansion_provider
    from phase165_r55_nk_only_goal import registered_group_goal_candidates
    from phase169_r10e2_unpositioned_citation.source_first import (
        screen_independent_sources_for_derived_goal,
    )
    from phase165_r3_recursive_search import reconstruct_registered_goal
    from phase166_r3t_goal_source_binding.goal_source import resolve_specialized_goal_citing_id

    bridge = build_shared_typed_bridge()
    roots = registered_group_goal_candidates(bridge, n=3, k=5)
    assert len(roots) == 1
    root = roots[0]
    # An unpositioned DB group goal has no invented source citation.
    assert resolve_specialized_goal_citing_id(bridge, root) is None
    screened = screen_independent_sources_for_derived_goal(bridge, goal=root)
    provider = shared_expansion_provider(screened, proof_target=root)
    goal = canonical_quadruple_goal(5)
    assert goal is not None
    choices = tuple(item for item in provider(goal)
                    if item.rule.name == "specialize cited Toda (5.5) quadruple nu-family identity")
    assert len(choices) == 1
    assert len(choices[0].subgoals) == 3

    # The reconstruction API requires an existing assertion ID as a context
    # anchor.  Use the uniquely screened (5.5) source, NOT an invented
    # citation for the unrelated, still-unproved pi_8^3 group goal.
    source_links = tuple(
        link for link in screened.proof_links
        if link.step is not None
        and link.step.rule is ProofRule.GIVEN
        and link.step.conclusion == Toda55UniversalQuadrupleStatement()
    )
    assert len(source_links) == 1
    context_id = source_links[0].assertion_id
    assert bridge.registry.assertion(context_id).content == Toda55UniversalQuadrupleStatement()
    result = reconstruct_registered_goal(
        goal, screened, context_id, provider, lookup_mode="typed_reference",
    )
    assert result is not None and result.rule is ProofRule.INFERENCE
    assert result.conclusion == goal
    assert len(result.premises) == 3
    assert not any(step.conclusion == root for step in result.premises)

```

## 変更対象テスト関数全文

```python
def test_shared_provider_proposes_and_proves_nu5_quadruple() -> None:
    from phase165_r52_r9_shared_math import build_shared_typed_bridge, shared_expansion_provider
    from phase165_r55_nk_only_goal import registered_group_goal_candidates
    from phase169_r10e2_unpositioned_citation.source_first import (
        screen_independent_sources_for_derived_goal,
    )
    from phase165_r3_recursive_search import reconstruct_registered_goal
    from phase166_r3t_goal_source_binding.goal_source import resolve_specialized_goal_citing_id

    bridge = build_shared_typed_bridge()
    roots = registered_group_goal_candidates(bridge, n=3, k=5)
    assert len(roots) == 1
    root = roots[0]
    # An unpositioned DB group goal has no invented source citation.
    assert resolve_specialized_goal_citing_id(bridge, root) is None
    screened = screen_independent_sources_for_derived_goal(bridge, goal=root)
    provider = shared_expansion_provider(screened, proof_target=root)
    goal = canonical_quadruple_goal(5)
    assert goal is not None
    choices = tuple(item for item in provider(goal)
                    if item.rule.name == "specialize cited Toda (5.5) quadruple nu-family identity")
    assert len(choices) == 1
    assert len(choices[0].subgoals) == 3

    # The reconstruction API requires an existing assertion ID as a context
    # anchor.  Use the uniquely screened (5.5) source, NOT an invented
    # citation for the unrelated, still-unproved pi_8^3 group goal.
    source_links = tuple(
        link for link in screened.proof_links
        if link.step is not None
        and link.step.rule is ProofRule.GIVEN
        and link.step.conclusion == Toda55UniversalQuadrupleStatement()
    )
    assert len(source_links) == 1
    context_id = source_links[0].assertion_id
    assert bridge.registry.assertion(context_id).content == Toda55UniversalQuadrupleStatement()
    result = reconstruct_registered_goal(
        goal, screened, context_id, provider, lookup_mode="typed_reference",
    )
    assert result is not None and result.rule is ProofRule.INFERENCE
    assert result.conclusion == goal
    assert len(result.premises) == 3
    assert not any(step.conclusion == root for step in result.premises)

```

## 新規 install.py 全文

```python
"""R3R28R1: replace only the failed citation-context test function."""
from __future__ import annotations

import argparse
import ast
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]
TARGET = ROOT / "phase176_r3r28_toda55_quadruple_public" / "tests" / "test_public.py"
BASE = Path(__file__).resolve().parent
EXPECTED_OLD = (BASE / "OLD_FUNCTION.txt").read_text(encoding="utf-8")
REPLACEMENT = (BASE / "NEW_FUNCTION.txt").read_text(encoding="utf-8")


def git(*args: str) -> str:
    result = subprocess.run(("git", *args), cwd=ROOT, text=True,
                            encoding="utf-8", errors="replace", capture_output=True)
    if result.returncode != 0:
        raise RuntimeError("GIT_FAILED: " + result.stderr.strip())
    return result.stdout.strip()


def check_checkout() -> str:
    if Path(git("rev-parse", "--show-toplevel")).resolve() != ROOT.resolve():
        raise RuntimeError("WRONG_REPOSITORY_ROOT")
    if git("branch", "--show-current") != "develop":
        raise RuntimeError("DEVELOP_BRANCH_REQUIRED")
    if not TARGET.is_file():
        raise RuntimeError("TARGET_TEST_NOT_FOUND")
    return git("rev-parse", "HEAD")


def function_body(source: str, name: str) -> str:
    tree = ast.parse(source)
    lines = source.splitlines(keepends=True)
    matches = [node for node in tree.body if isinstance(node, ast.FunctionDef) and node.name == name]
    if len(matches) != 1:
        raise RuntimeError("TEST_FUNCTION_MISSING_OR_DUPLICATED")
    node = matches[0]
    return "".join(lines[node.lineno - 1:node.end_lineno])


def proposed(source: str) -> str:
    name = "test_shared_provider_proposes_and_proves_nu5_quadruple"
    current = function_body(source, name)
    if current.rstrip("\n") == REPLACEMENT.rstrip("\n"):
        return source
    if current.rstrip("\n") != EXPECTED_OLD.rstrip("\n"):
        raise RuntimeError("TEST_BASELINE_CHANGED")
    result = source.replace(current, REPLACEMENT, 1)
    ast.parse(result)
    if function_body(result, name).rstrip("\n") != REPLACEMENT.rstrip("\n"):
        raise RuntimeError("FUNCTION_REPLACEMENT_FAILED")
    return result


def execute(dry_run: bool) -> int:
    row = {"phase": "176_R3R28R1", "gate": "FAIL_R3R28R1",
           "full_pytest": "NOT_RUN", "production_changes": 0,
           "new_given": 0, "new_mathematical_rules": 0}
    try:
        row["head"] = check_checkout()
        raw = TARGET.read_bytes()
        newline = "\r\n" if b"\r\n" in raw else "\n"
        original = raw.decode("utf-8-sig").replace("\r\n", "\n")
        replacement = proposed(original)
        row["changed"] = replacement != original
        if not dry_run and replacement != original:
            TARGET.write_bytes(replacement.replace("\n", newline).encode("utf-8"))
        row["gate"] = "PASS_R3R28R1_DRYRUN" if dry_run else "PASS_R3R28R1_TEST_FIXED_PENDING_PYTEST"
    except Exception as exc:
        row["error"] = type(exc).__name__ + ": " + str(exc)
    path = Path(os.environ.get("LOCALAPPDATA") or tempfile.gettempdir()) / "EHPProofTracerAudit" / "phase176_r3r28r1_uncited_root_test_fix"
    path.mkdir(parents=True, exist_ok=True)
    report = path / "report.json"
    report.write_text(json.dumps(row, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    for key in ("gate", "head", "changed", "production_changes"):
        if key in row:
            print("PHASE176_R3R28R1_" + key.upper() + "=" + str(row[key]))
    if "error" in row:
        print("PHASE176_R3R28R1_ERROR=" + row["error"])
    print("PHASE176_R3R28R1_REPORT=" + str(report))
    print("PHASE176_R3R28R1_FULL_PYTEST=NOT_RUN")
    print("(END)")
    return 0 if row["gate"].startswith("PASS_") else 1


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    return execute(parser.parse_args().dry_run)


if __name__ == "__main__":
    sys.exit(main())

```

## 新規 run.ps1 全文

```powershell
param([switch]$DryRun)
$ErrorActionPreference = 'Stop'
$repo = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Push-Location $repo
try {
    if ($DryRun) {
        python -B -m phase176_r3r28r1_uncited_root_test_fix.install --dry-run
        if ($LASTEXITCODE -ne 0) { throw 'R3R28R1 DryRun failed' }
    } else {
        python -B -m phase176_r3r28r1_uncited_root_test_fix.install
        if ($LASTEXITCODE -ne 0) { throw 'R3R28R1 test update failed' }
        python -B -m pytest -q -p no:cacheprovider `
            .\phase176_r3r28_toda55_quadruple_public\tests `
            .\phase176_r3r27r1_toda55_quadruple_isolated\tests `
            .\phase174_r3_r6_source_extension\tests\test_source.py
        if ($LASTEXITCODE -ne 0) { throw 'R3R28R1 focused pytest failed' }
        Write-Host 'PHASE176_R3R28R1_GATE=PASS_R3R28R1_FOCUSED_TESTS'
        Write-Host 'PHASE176_R3R28R1_FULL_PYTEST=NOT_RUN'
        Write-Host '(END)'
    }
} finally {
    Pop-Location
}

```
