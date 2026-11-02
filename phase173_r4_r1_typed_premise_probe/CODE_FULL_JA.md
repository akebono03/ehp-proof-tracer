# Phase 173 R4-R1 — HEAD 修正コード全文

対象は監査専用パッケージです。`audit.py` は定数 `REVIEWED_HEADS` のみの変更ですが、import を含む完全なファイルを示します。`tests/test_audit.py` はテストの全コードを示します。既存 `run.ps1` は実行単位ごと掲載します。コード内の省略はありません。

## `phase173_r4_r1_typed_premise_probe/audit.py`（全文）

```python
"""Phase 173 R4-R1: audit typed prerequisites before any Toda (5.6) integration.

No production edits, invented citations, GIVEN steps, or unproved DB premises.
"""
from __future__ import annotations

import argparse
import ast
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import subprocess
from typing import Any

REVIEWED_HEADS = frozenset((
    "f9fdaf350ff4de3f6a6f9b3cd6d6901f5b439941",
    "6f5adde0a0e0f124d5247ef6b1c255f83697f42b",
    "c352f7d24d3156ba7cde26ebb0933c4680a8c813",
))
REVIEWED_BLOBS = {
    "sources/toda/Toda_05_2.tex": "579661138928499ba04a51327f686d9b971b5314",
    "sources/toda/Toda_04_2.tex": "4d0c32b196f4bd51c04650dd26b0fd7133b6d4f7",
    "toda_rules.py": "77f4159644f10eff65a79f6e528cf7b471c6ddc9",
    "phase165_r52_r9_shared_math.py": "2718c55789af7f442ac2c086d016d3d6f7ca3133",
    "phase165_r52_r16_web_citation_gate.py": "d1138c0450f234b6da761902ed7358b6038a19c8",
    "phase165_r55_nk_only_goal.py": "b207b8169590e634229d412324d857ffb3857939",
    "phase165_r52_r27_r5_literature.py": "c9bfe2788f4cf043db6dada98a437afea6accf75",
    "phase165_r14_r8_source_link.py": "35ac57198c49ed7d768dc17edf4029001c8f3d49",
    "phase165_r14_r15_typed_diagonal.py": "4bbabad167c31cb66191107cf05a616f583700b7",
    "phase165_r57_r26_generic_search_connection.py": "4fc6497bd1c601b30cbaefb03c92357338644118",
    "phase169_r3m_prior_result_catalog/prior_results.py": "c522cbaf924b3a9aa500d453b8eb6a1a66c42611",
}
RULE_FACTORIES = (
    "toda_prop44_isomorphism_inference_rule",
    "toda_prop56_pi7_4_decomposition_inference_rule",
    "toda_56_nu4_decomposition_integration_inference_rule",
    "toda_56_nu4_prop44_specialization_inference_rule",
    "toda_56_nu4_prop44_isomorphism_inference_rule",
    "toda_56_nu4_decomposition_isomorphism_inference_rule",
)


def git(root: Path, *args: str) -> str:
    result = subprocess.run(
        ("git", *args), cwd=root, capture_output=True, text=True,
        encoding="utf-8", check=True,
    )
    return result.stdout.rstrip("\r\n")


def guard_source_files(root: Path) -> dict[str, Any]:
    """Pin source blobs and ensure both index and worktree are unmodified.

    Unrelated audit files and the known pytest cache are neither trusted nor
    deleted. An unknown HEAD must be reviewed rather than silently accepted.
    """
    if git(root, "branch", "--show-current") != "develop":
        raise RuntimeError("This audit requires the develop branch")
    head = git(root, "rev-parse", "HEAD")
    if head not in REVIEWED_HEADS:
        raise RuntimeError("Unreviewed HEAD; review new GitHub commits: " + head)
    inspected = []
    for path, expected in REVIEWED_BLOBS.items():
        actual = git(root, "rev-parse", "HEAD:" + path)
        if actual != expected:
            raise RuntimeError("Committed reviewed source blob changed: " + path)
        for diff_args in (("diff", "--quiet", "--", path),
                          ("diff", "--cached", "--quiet", "--", path)):
            result = subprocess.run(
                ("git", *diff_args), cwd=root, capture_output=True, check=False,
            )
            if result.returncode != 0:
                raise RuntimeError("Reviewed source has local modifications: " + path)
        inspected.append(path)
    return {"branch": "develop", "head": head, "reviewed_unchanged": True,
            "source_paths": inspected, "git_mutated": False}


def inspect_factories(source: str) -> list[dict[str, Any]]:
    """Show entire existing function bodies in the JSON, never infer proof from syntax."""
    module = ast.parse(source)
    functions: dict[str, list[ast.FunctionDef]] = {}
    for node in module.body:
        if isinstance(node, ast.FunctionDef):
            functions.setdefault(node.name, []).append(node)
    results = []
    for name in RULE_FACTORIES:
        found = functions.get(name, [])
        row: dict[str, Any] = {"factory": name, "definition_count": len(found),
                               "registered_rule_names": [], "source": None}
        if len(found) == 1:
            node = found[0]
            row["line"] = node.lineno
            row["source"] = ast.get_source_segment(source, node)
            names = []
            for child in ast.walk(node):
                if not isinstance(child, ast.Call):
                    continue
                if isinstance(child.func, ast.Name) and child.func.id == "InferenceRule":
                    for keyword in child.keywords:
                        if (keyword.arg == "name" and isinstance(keyword.value, ast.Constant)
                                and isinstance(keyword.value.value, str)):
                            names.append(keyword.value.value)
            row["registered_rule_names"] = sorted(set(names))
            row["uses_typed_premises"] = "PremisePattern" in row["source"]
            row["has_explicit_reference"] = "LiteratureReference" in row["source"]
        results.append(row)
    return results


def candidate_summary(options: tuple[object, ...]) -> list[dict[str, Any]]:
    """Record backward proposals, without turning a proposal into proof."""
    output = []
    for item in options:
        children = getattr(item, "subgoals", ())
        output.append({"rule_name": getattr(getattr(item, "rule", None), "name", "UNKNOWN"),
                       "premise_types": [type(x).__name__ for x in children],
                       "premises": [repr(x)[:2500] for x in children]})
    return output


def inspect_runtime(*, search_pi77: bool) -> dict[str, Any]:
    """Check the real provider, source-bound pi_7^7 and hypothetical prior input."""
    from phase165_r52_r9_shared_math import (
        build_shared_typed_bridge, shared_expansion_provider,
    )
    from phase165_r6_2_unified_registry_r1.unified_backward_rule_registry import (
        build_unified_backward_rule_registry,
    )
    from phase165_r55_nk_only_goal import (
        registered_group_goal_candidates, search_group_from_registered_goal,
    )
    from phase165_r52_r16_web_citation_gate import screen_shared_proof_context
    from phase165_r12_r11_prop42_unified import prefer_universal_prop42_derivation
    from phase166_r3t_goal_source_binding.goal_source import (
        resolve_specialized_goal_citing_id,
    )
    from phase169_r3m_prior_result_catalog.prior_results import (
        resolve_prior_group_result,
    )
    from phase165_r52_r27_r5_literature import TodaProp44UniversalStatement
    from phase165_r52_partial_proof import ProofSearchStatus
    from proof import ProofRule

    bridge = build_shared_typed_bridge()
    goals = registered_group_goal_candidates(bridge, n=4, k=3)
    if len(goals) != 1:
        raise RuntimeError("Expected precisely one typed pi_7^4 goal")
    goal = goals[0]
    citing_id = resolve_specialized_goal_citing_id(bridge, goal)
    if citing_id is None:
        raise RuntimeError("Cannot position pi_7^4 in the source")
    screened = prefer_universal_prop42_derivation(screen_shared_proof_context(
        bridge, goal=goal, citing_assertion_id=citing_id,
        explicit_publication_target=True,
    ))
    fixed = tuple(link.step.conclusion for link in screened.proof_links
                  if link.step is not None and link.step.rule is ProofRule.GIVEN)
    if any(type(s) is type(goal) and s == goal for s in fixed):
        raise RuntimeError("Target was promoted to an unproved GIVEN")
    prop44 = sum(type(s) is TodaProp44UniversalStatement and
                 s == TodaProp44UniversalStatement() for s in fixed)
    prior = resolve_prior_group_result(
        screened, source_n=3, source_k=3, citing_assertion_id=citing_id,
    )
    regular = shared_expansion_provider(screened, proof_target=goal)
    usual = candidate_summary(regular(goal))
    hypothetical = []
    if prior.eligible and prior.relation is not None:
        # This is a proposal-only diagnostic. The DB relation is NOT made a GIVEN.
        with_prior = shared_expansion_provider(
            screened, proof_target=goal, prior_conclusions=(prior.relation,),
        )
        hypothetical = candidate_summary(with_prior(goal))
    registry, report = build_unified_backward_rule_registry()
    registered_names = {rule.name for rule in registry.rules()}
    factory_metadata = inspect_factories(
        (Path.cwd() / "toda_rules.py").read_text(encoding="utf-8-sig")
    )
    for row in factory_metadata:
        row["matching_registered_rule_names"] = sorted(
            registered_names.intersection(row["registered_rule_names"])
        )
    pi77_goals = registered_group_goal_candidates(bridge, n=7, k=0)
    pi77: dict[str, Any] = {
        "goal_count": len(pi77_goals),
        "goal_reprs": [repr(item)[:2500] for item in pi77_goals],
        "proof_search_performed": search_pi77,
        "complete": False,
    }
    if search_pi77 and len(pi77_goals) == 1:
        try:
            result = search_group_from_registered_goal(n=7, k=0, bridge=bridge)
            complete = (result.status is ProofSearchStatus.COMPLETE
                        and result.conclusion == pi77_goals[0])
            pi77["complete"] = bool(complete)
            pi77["status"] = getattr(result.status, "value", str(result.status))
            pi77["exact_target_reproduced"] = result.conclusion == pi77_goals[0]
            pi77["proof_steps"] = str(getattr(result, "proven_steps", "UNKNOWN"))[:2000]
            pi77["open_goals"] = [repr(x)[:500] for x in getattr(result, "open_goals", ())]
            pi77["diagnostics"] = [str(x)[:500] for x in getattr(result, "diagnostics", ())]
        except Exception as exc:
            pi77["search_error"] = type(exc).__name__ + ": " + str(exc)[:1800]
    return {
        "target": repr(goal), "source_assertion_id": citing_id,
        "prop44_cited_given_count": prop44,
        "prior_pi63_eligible": prior.eligible, "prior_pi63_reason": prior.reason,
        "prior_pi63_proved_by_this_audit": False,
        "production_root_candidates": usual,
        "hypothetical_prior_input_candidates": hypothetical,
        "hypothetical_prior_is_proof": False,
        "pi77": pi77,
        "unified_rule_count": len(registered_names),
        "historical_rules": factory_metadata,
        "completion_certified": False,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Read-only Phase 173 R4-R1 typed-premise audit")
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--skip-pi77-search", action="store_true")
    args = parser.parse_args()
    root = args.root.resolve()
    source_guard = guard_source_files(root)
    if args.dry_run:
        print("PHASE173_R4_R1_TYPED_PREMISE_DRY_RUN=PASS")
        print("PHASE173_R4_R1_REVIEWED_SOURCE_UNCHANGED=True")
        print("PHASE173_R4_R1_NO_GIT_MUTATION=True")
        return 0
    report: dict[str, Any] = {
        "phase": "173-R4-R1-typed-premise", "scope": "AUDIT_ONLY",
        "time_utc": datetime.now(timezone.utc).isoformat(),
        "preflight": source_guard,
        "runtime": inspect_runtime(search_pi77=not args.skip_pi77_search),
        "production_changes": [],
    }
    destination = (Path(os.environ.get("LOCALAPPDATA", str(Path.home()))) /
                   "EHPProofTracerRecovery" / "phase173_r4_r1_typed_premise_probe" / "audit.json")
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    runtime = report["runtime"]
    print("PHASE173_R4_R1_TYPED_PREMISE_AUDIT=PASS")
    print("HEAD=" + source_guard["head"])
    print("PROP44_CITED_GIVEN=" + str(runtime["prop44_cited_given_count"]))
    print("PI63_PRIOR_ELIGIBLE=" + str(runtime["prior_pi63_eligible"]))
    print("PI77_GOALS=" + str(runtime["pi77"]["goal_count"]))
    print("PI77_PROOF_SEARCH_PERFORMED=" + str(runtime["pi77"]["proof_search_performed"]))
    print("PI77_COMPLETE=" + str(runtime["pi77"]["complete"]))
    if "status" in runtime["pi77"]:
        print("PI77_SEARCH_STATUS=" + runtime["pi77"]["status"])
    if "search_error" in runtime["pi77"]:
        print("PI77_SEARCH_ERROR=" + runtime["pi77"]["search_error"])
    print("PUBLIC_ROOT_CANDIDATES=" + str(len(runtime["production_root_candidates"])))
    print("HYPOTHETICAL_PRIOR_ROOT_CANDIDATES=" + str(len(runtime["hypothetical_prior_input_candidates"])))
    for rule in runtime["historical_rules"]:
        print("FACTORY=" + rule["factory"] +
              " DEFINED=" + str(rule["definition_count"] == 1) +
              " REGISTERED=" + str(bool(rule["matching_registered_rule_names"])))
    print("COMPLETE_PROOF_CERTIFIED=False")
    print("OBSERVATION_ONLY=True")
    print("AUDIT_JSON=" + str(destination))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

```

## `phase173_r4_r1_typed_premise_probe/tests/test_audit.py`（全文）

```python
"""Offline focused tests for the R4-R1 proof-premise audit only."""
from __future__ import annotations

from pathlib import Path
import subprocess

import pytest

from phase173_r4_r1_typed_premise_probe import audit


def test_rule_inventory_has_six_unique_factories() -> None:
    assert len(audit.RULE_FACTORIES) == 6
    assert len(set(audit.RULE_FACTORIES)) == 6


def test_extract_rule_factory_and_references() -> None:
    source = """
def toda_prop44_isomorphism_inference_rule():
    return InferenceRule(name='old iso', premise_patterns=(PremisePattern(),), conclusion_pattern='x')
"""
    found = audit.inspect_factories(source)
    assert found[0]["definition_count"] == 1
    assert found[0]["registered_rule_names"] == ["old iso"]
    assert found[0]["uses_typed_premises"] is True
    assert found[0]["has_explicit_reference"] is False
    assert found[1]["definition_count"] == 0


def test_duplicate_rule_factory_is_not_accepted_as_unique() -> None:
    source = """
def toda_prop44_isomorphism_inference_rule():
    return 1

def toda_prop44_isomorphism_inference_rule():
    return 2
"""
    assert audit.inspect_factories(source)[0]["definition_count"] == 2


def test_candidate_summary_does_not_claim_success() -> None:
    class Rule:
        name = "candidate"
    class Option:
        rule = Rule()
        subgoals = ("unproved",)
    assert audit.candidate_summary((Option(),)) == [
        {"rule_name": "candidate", "premise_types": ["str"],
         "premises": ["'unproved'"]}
    ]


def test_reviewed_head_is_strictly_pinned() -> None:
    assert audit.REVIEWED_HEADS == {
        "f9fdaf350ff4de3f6a6f9b3cd6d6901f5b439941",
        "6f5adde0a0e0f124d5247ef6b1c255f83697f42b",
        "c352f7d24d3156ba7cde26ebb0933c4680a8c813",
    }


def test_production_blob_guard_fails_on_changed_source(monkeypatch, tmp_path: Path) -> None:
    def fake_git(root: Path, *args: str) -> str:
        if args == ("branch", "--show-current"):
            return "develop"
        if args == ("rev-parse", "HEAD"):
            return "f9fdaf350ff4de3f6a6f9b3cd6d6901f5b439941"
        if args[:1] == ("rev-parse",):
            return "unreviewed"
        raise AssertionError(args)
    monkeypatch.setattr(audit, "git", fake_git)
    with pytest.raises(RuntimeError, match="Committed reviewed source blob changed"):
        audit.guard_source_files(tmp_path)


@pytest.mark.parametrize("exit_code", [1, 2, 128])
def test_tracked_source_changes_rejected(monkeypatch, tmp_path: Path, exit_code: int) -> None:
    def fake_git(root: Path, *args: str) -> str:
        if args == ("branch", "--show-current"):
            return "develop"
        if args == ("rev-parse", "HEAD"):
            return "f9fdaf350ff4de3f6a6f9b3cd6d6901f5b439941"
        if args[:1] == ("rev-parse",):
            return audit.REVIEWED_BLOBS[args[1][5:]]
        raise AssertionError(args)
    monkeypatch.setattr(audit, "git", fake_git)
    monkeypatch.setattr(audit.subprocess, "run", lambda *a, **k: type("Result", (), {"returncode": exit_code})())
    with pytest.raises(RuntimeError, match="Reviewed source has local modifications"):
        audit.guard_source_files(tmp_path)


def test_audit_has_no_production_write_functions() -> None:
    from inspect import getsource
    source = getsource(audit)
    assert "git reset" not in source
    assert "git checkout" not in source
    assert "git restore" not in source
    assert "production_changes\": []" in source


def test_reviewed_c352_head_accepts_only_unchanged_source_blobs(monkeypatch, tmp_path: Path) -> None:
    expected_head = "c352f7d24d3156ba7cde26ebb0933c4680a8c813"
    def fake_git(root: Path, *args: str) -> str:
        if args == ("branch", "--show-current"):
            return "develop"
        if args == ("rev-parse", "HEAD"):
            return expected_head
        if len(args) == 2 and args[0] == "rev-parse" and args[1].startswith("HEAD:"):
            return audit.REVIEWED_BLOBS[args[1][5:]]
        raise AssertionError(args)
    monkeypatch.setattr(audit, "git", fake_git)
    monkeypatch.setattr(
        audit.subprocess, "run",
        lambda *args, **kwargs: type("GitResult", (), {"returncode": 0})(),
    )
    report = audit.guard_source_files(tmp_path)
    assert report["head"] == expected_head
    assert report["reviewed_unchanged"] is True
    assert report["git_mutated"] is False
    assert set(report["source_paths"]) == set(audit.REVIEWED_BLOBS)


def test_unknown_new_head_still_rejected(monkeypatch, tmp_path: Path) -> None:
    def fake_git(root: Path, *args: str) -> str:
        if args == ("branch", "--show-current"):
            return "develop"
        if args == ("rev-parse", "HEAD"):
            return "not-reviewed-after-c352"
        raise AssertionError(args)
    monkeypatch.setattr(audit, "git", fake_git)
    with pytest.raises(RuntimeError, match="Unreviewed HEAD"):
        audit.guard_source_files(tmp_path)

```

## `phase173_r4_r1_typed_premise_probe/run.ps1`（全文）

```powershell
param(
    [switch]$DryRun,
    [switch]$SkipPi77Search
)
Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'
$RepoRoot = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Push-Location $RepoRoot
try {
    $env:PYTHONPATH = $RepoRoot
    $env:PYTHONDONTWRITEBYTECODE = '1'
    Write-Output 'PHASE173_R4_R1_TYPED_PREMISE_FOCUSED_PYTEST_START'
    & python -m pytest -q -p no:cacheprovider '.\phase173_r4_r1_typed_premise_probe\tests\test_audit.py'
    if ($LASTEXITCODE -ne 0) { throw 'R4-R1 typed-premise focused tests failed' }
    Write-Output 'PHASE173_R4_R1_TYPED_PREMISE_FOCUSED_PYTEST=PASS'
    $Arguments = @('-m', 'phase173_r4_r1_typed_premise_probe.audit')
    if ($DryRun) { $Arguments += '--dry-run' }
    if ($SkipPi77Search) { $Arguments += '--skip-pi77-search' }
    & python @Arguments
    if ($LASTEXITCODE -ne 0) { throw 'R4-R1 typed-premise audit failed' }
} finally {
    Pop-Location
}

```
