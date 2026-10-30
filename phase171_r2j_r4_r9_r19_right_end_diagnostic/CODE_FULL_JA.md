# Phase 171 R19 追加コード全文

新規ファイルのみ。既存の import・クラス・関数は変更しない。

## audit.py

```python
"""Phase 171 R19: diagnose the unresolved right end group of EHP cardinality.

No proof source, provider, resolver, source registry, or trusted proof is
modified or inserted. The previously recorded R18 result is the baseline.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path
from typing import Any

from phase171_r2j_r4_r9_r18_cardinality_premise_audit import audit as r18
from phase171_r2j_r4_r9_r17_public_context_path_audit import audit as r17
from phase171_r2j_r4_r9_r14_root_branch_diagnostic.audit import CanonicalResolveTrace

PACKAGE = Path(__file__).resolve().parent
ROOT = PACKAGE.parent
R18_REPORT = ROOT / "phase171_r2j_r4_r9_r18_cardinality_premise_audit" / "output" / "audit.json"
OUTPUT = PACKAGE / "output" / "audit.json"
MAX_REPR = 1900


def preflight() -> dict[str, Any]:
    """Reject unsupported sources and nonmatching R18 observations."""
    checked = r18.preflight()
    if not R18_REPORT.is_file():
        raise RuntimeError("R18 output/audit.json is required")
    raw = R18_REPORT.read_bytes()
    report = json.loads(raw.decode("utf-8-sig"))
    if report.get("phase") != "171-R2J-R4-R9-R18":
        raise RuntimeError("unexpected R18 report")
    if report.get("source_changes") != 0 or report.get("new_given") != 0:
        raise RuntimeError("R18 source purity violated")
    if report.get("public_root_status") != "partial":
        raise RuntimeError("R18 public root baseline changed")
    for context in ("screened", "public"):
        statuses = report.get("contexts", {}).get(context, {}).get("premise_statuses", {})
        if statuses != {
            "left_end_group": "proved", "short_exact": "proved", "right_end_group": "unresolved",
        }:
            raise RuntimeError("R18 premise baseline changed: " + context)
    checked["r18_sha256"] = hashlib.sha256(raw).hexdigest()
    return checked


def classify_right_failure(*, status: str, route_names: tuple[str, ...],
                           exact_leaf_count: int, eta_source_count: int,
                           eta_route_count: int, error: str) -> str:
    """Classify observed evidence without inferring a proof from a candidate."""
    if status == "proved":
        return "RIGHT_GROUP_NOW_PROVED_CHECK_ROOT"
    if status != "unresolved":
        return "RIGHT_GROUP_UNEXPECTED_RESULT"
    if not route_names:
        if eta_source_count and not eta_route_count:
            return "CITED_ETA_SPECIALIZATION_NOT_CONNECTED"
        return "RIGHT_GROUP_NO_PROVIDER_EXPANSION"
    if re.search(r"found [2-9][0-9]*\Z", error):
        return "RIGHT_GROUP_AMBIGUOUS_DERIVATIONS"
    if re.search(r"found 0\Z", error):
        if exact_leaf_count == 0 and eta_source_count == 0:
            return "RIGHT_GROUP_CITED_SOURCE_NOT_AVAILABLE"
        if eta_source_count and eta_route_count == 0:
            return "RIGHT_GROUP_ETA_SOURCE_PRESENT_ROUTE_MISSING"
        return "RIGHT_GROUP_PROPOSALS_DO_NOT_CLOSE"
    if "cyclic proof dependency" in error:
        return "RIGHT_GROUP_CYCLIC_DEPENDENCY"
    return "RIGHT_GROUP_OTHER_UNRESOLVED"


def exact_screened_sources(goal: object, bridge: object, citing: str) -> list[dict[str, str]]:
    """Identify prior linked exact facts without converting them to new leaves."""
    from proof import ProofRule
    from phase166_r3c_publication_order import precedes_citing_assertion
    from unified_statement_registry import AssertionOrigin

    found: list[dict[str, str]] = []
    for link in bridge.proof_links:
        if link.step is None or link.step.rule is not ProofRule.GIVEN:
            continue
        assertion = bridge.registry.assertion(link.assertion_id)
        if (assertion.origin is AssertionOrigin.FIXED_STATEMENT
                and type(assertion.content) is type(goal)
                and assertion.content == goal
                and link.step.conclusion == goal
                and precedes_citing_assertion(bridge, link.assertion_id, citing)):
            found.append({
                "id": link.assertion_id,
                "locator": bridge.registry.reference(assertion.reference_id).locator,
            })
    return found


def describe_route(route: object) -> dict[str, Any]:
    """Record a GoalExpansion as an obligation, not as an accepted proof."""
    return {
        "rule": str(getattr(route.rule, "name", "")),
        "subgoals": [repr(goal)[:MAX_REPR] for goal in route.subgoals],
    }


def inspect() -> dict[str, Any]:
    """Probe exact R18 right-end goal and inspect eligible source ancestry."""
    from phase165_r52_r9_shared_math import shared_expansion_provider
    from phase165_r57_r8_eta_specialization import (
        _is_generic_eta_group_relation, expand_registered_eta_specialization,
        specialize_eta_group_relation,
    )
    from phase165_r57_r20_general_specialization import expand_cited_general_specialization
    from phase171_r2i_eta_hopf_bridge.audit import _screened_context
    from phase171_r2j_r4_r6_middle_cardinality.source import FiniteGroupCardinality
    from homotopy_groups import TodaPrimaryGroup
    from proof import ProofRule

    screened, root, citing = _screened_context()
    provider = shared_expansion_provider(screened, proof_target=root)
    cardinality = FiniteGroupCardinality(TodaPrimaryGroup(6, 3), 4)
    route = r18.cardinality_route(provider, cardinality)
    right = route.subgoals[2]
    available = tuple(
        link.step.conclusion for link in screened.proof_links
        if link.step is not None and link.step.rule is ProofRule.GIVEN
    )
    eta_sources: list[dict[str, str]] = []
    eta_sources_conclusions = []
    for link in screened.proof_links:
        if link.step is None or link.step.rule is not ProofRule.GIVEN:
            continue
        source = link.step.conclusion
        if not _is_generic_eta_group_relation(source):
            continue
        eta_sources_conclusions.append(source)
        try:
            specialized = specialize_eta_group_relation(source, right.lhs.sphere_dimension)
        except (ValueError, TypeError):
            continue
        if specialized == right:
            assertion = screened.registry.assertion(link.assertion_id)
            eta_sources.append({
                "id": link.assertion_id,
                "locator": screened.registry.reference(assertion.reference_id).locator,
                "specialization_matches_right": "True",
            })
    eta_expansions = expand_registered_eta_specialization(right, available)
    scalar_expansions = expand_cited_general_specialization(right, available)
    all_routes = provider(right)
    # Exact R18 standalone run again, with an observational exception trace.
    trace = CanonicalResolveTrace(root, right, right)
    with trace:
        observed, _ = r18.probe_premise(right, provider, screened, citing, root)
    prior = json.loads(R18_REPORT.read_text(encoding="utf-8-sig"))
    old = prior["contexts"]["screened"]["premises"]["right_end_group"]
    if old["goal"] != observed["goal"]:
        raise RuntimeError("R18 right-end goal identity changed")
    if old["status"] != observed["status"]:
        raise RuntimeError("R18 right-end status changed")
    exact = exact_screened_sources(right, screened, citing)
    origin = [
        {
            "kind": event["kind"],
            "target": event["target"][:MAX_REPR],
            "candidate_rule": event["candidate_rule"],
            "active_last": event["active_last"],
        }
        for event in trace.exceptions if event["origin"]
    ]
    result = {
        "phase": "171-R2J-R4-R9-R19",
        "mode": "READ_ONLY_RIGHT_END_GROUP_SOURCE_AND_PROVIDER_DIAGNOSTIC",
        "right_end_goal": repr(right),
        "r18_screened_error": old.get("error"),
        "r18_public_error": prior["contexts"]["public"]["premises"]["right_end_group"].get("error"),
        "status": observed["status"],
        "error": observed.get("error"),
        "provider_route_count": len(all_routes),
        "provider_routes": [describe_route(option) for option in all_routes],
        "exact_prior_screened_sources": exact,
        "eligible_eta_general_sources": eta_sources,
        "eta_general_source_count": len(eta_sources_conclusions),
        "eta_specialization_route_count": len(eta_expansions),
        "eta_specialization_routes": [describe_route(option) for option in eta_expansions],
        "general_scalar_route_count": len(scalar_expansions),
        "general_scalar_routes": [describe_route(option) for option in scalar_expansions],
        "recursive_resolve_calls": trace.calls,
        "origin_events": origin[:55],
        "origin_counts": dict(trace.origin_totals),
        "r18_source_id_set_equal": prior["source_comparison"]["same_id_set"],
        "new_given": 0,
        "source_changes": 0,
        "completed_proof_imported": False,
        "trust_boundary_modified": False,
        "full_pytest": False,
    }
    result["classification"] = classify_right_failure(
        status=observed["status"],
        route_names=tuple(item["rule"] for item in result["provider_routes"]),
        exact_leaf_count=len(exact),
        eta_source_count=len(eta_sources),
        eta_route_count=len(eta_expansions),
        error=observed.get("error") or "",
    )
    return result


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    checked = preflight()
    print("PHASE171_R19_BRANCH=" + checked["branch"], flush=True)
    print("PHASE171_R19_HEAD=" + checked["head"], flush=True)
    print("PHASE171_R19_R18_REPORT=PASS", flush=True)
    print("PHASE171_R19_REVIEWED_PROVIDER=PASS", flush=True)
    if args.dry_run:
        print("PHASE171_R19_RESULT=PASS_DRY_RUN", flush=True)
        return
    before = r17.git_read("status", "--porcelain", "--untracked-files=no")
    report = inspect()
    after = r17.git_read("status", "--porcelain", "--untracked-files=no")
    if before != after:
        raise RuntimeError("tracked files changed during R19 audit")
    report["git_head"] = checked["head"]
    report["r18_sha256"] = checked["r18_sha256"]
    report["tracked_status_unchanged"] = True
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("PHASE171_R19_RIGHT=" + report["status"], flush=True)
    print("PHASE171_R19_R18_SCREENED_ERROR=" + str(report["r18_screened_error"]), flush=True)
    print("PHASE171_R19_R18_PUBLIC_ERROR=" + str(report["r18_public_error"]), flush=True)
    print("PHASE171_R19_PROVIDER_RULES=" + json.dumps(
        [route["rule"] for route in report["provider_routes"]], ensure_ascii=False), flush=True)
    print("PHASE171_R19_EXACT_SOURCES=" + str(len(report["exact_prior_screened_sources"])), flush=True)
    print("PHASE171_R19_ETA_GENERAL_SOURCES=" + str(len(report["eligible_eta_general_sources"])), flush=True)
    print("PHASE171_R19_ETA_SPECIALIZATION_ROUTES=" + str(report["eta_specialization_route_count"]), flush=True)
    print("PHASE171_R19_GENERAL_SCALAR_ROUTES=" + str(report["general_scalar_route_count"]), flush=True)
    print("PHASE171_R19_ORIGIN_COUNTS=" + json.dumps(report["origin_counts"], ensure_ascii=False), flush=True)
    print("PHASE171_R19_CLASSIFICATION=" + report["classification"], flush=True)
    print("PHASE171_R19_NEW_GIVEN=0", flush=True)
    print("PHASE171_R19_SOURCE_CHANGES=0", flush=True)
    print("PHASE171_R19_TRACKED_STATUS_UNCHANGED=PASS", flush=True)
    print("PHASE171_R19_REPORT=" + str(OUTPUT), flush=True)
    print("PHASE171_R19_RESULT=PASS_AUDIT_ONLY", flush=True)


if __name__ == "__main__":
    main()

```

## tests/test_audit.py

```python
"""Focused read-only right-end group diagnostics and classification tests."""
from __future__ import annotations

import pytest

from phase171_r2j_r4_r9_r19_right_end_diagnostic.audit import (
    classify_right_failure,
    describe_route,
    exact_screened_sources,
)
from phase165_r3_recursive_search import GoalExpansion
from proof import Relation, RelationType


def test_missing_source_and_empty_provider_is_not_proved():
    assert classify_right_failure(
        status="unresolved", route_names=(), exact_leaf_count=0,
        eta_source_count=0, eta_route_count=0, error="found 0",
    ) == "RIGHT_GROUP_NO_PROVIDER_EXPANSION"


def test_existing_eta_source_but_missing_route_is_distinguished():
    assert classify_right_failure(
        status="unresolved", route_names=("candidate",), exact_leaf_count=0,
        eta_source_count=1, eta_route_count=0, error="found 0",
    ) == "RIGHT_GROUP_ETA_SOURCE_PRESENT_ROUTE_MISSING"


def test_cited_source_absence_is_not_filled_by_a_fake_given():
    assert classify_right_failure(
        status="unresolved", route_names=("candidate",), exact_leaf_count=0,
        eta_source_count=0, eta_route_count=0, error="found 0",
    ) == "RIGHT_GROUP_CITED_SOURCE_NOT_AVAILABLE"


def test_ambiguous_derivation_is_not_treated_as_completion():
    assert classify_right_failure(
        status="unresolved", route_names=("a", "b"), exact_leaf_count=1,
        eta_source_count=1, eta_route_count=1,
        error="expected one registered derivation, found 2",
    ) == "RIGHT_GROUP_AMBIGUOUS_DERIVATIONS"


def test_proposal_representation_is_only_a_backward_obligation():
    from proof import InferenceRule
    proposed = GoalExpansion(InferenceRule(name="sample"), (
        Relation("x", "y", RelationType.EQUALITY),
    ))
    row = describe_route(proposed)
    assert row["rule"] == "sample"
    assert row["subgoals"] == [repr(proposed.subgoals[0])]


def test_read_only_git_guard_rejects_mutating_command():
    from phase171_r2j_r4_r9_r16_hopf_route_audit.audit import git_read
    with pytest.raises(ValueError):
        git_read("reset", "--hard")


def test_live_screened_source_search_rejects_unrelated_goal():
    from phase171_r2i_eta_hopf_bridge.audit import _screened_context
    bridge, _, citing = _screened_context()
    assert exact_screened_sources(object(), bridge, citing) == []

```

## run.ps1

```powershell
param([switch]$DryRun)
$ErrorActionPreference = 'Stop'
Set-StrictMode -Version Latest
$Package = Split-Path -Parent $MyInvocation.MyCommand.Path
$Root = Split-Path -Parent $Package
Set-Location $Root
if ($DryRun) {
    python -m phase171_r2j_r4_r9_r19_right_end_diagnostic.audit --dry-run
    if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
    Write-Output 'PHASE171_R19_DRY_RUN=PASS'
    exit 0
}
python -m phase171_r2j_r4_r9_r19_right_end_diagnostic.audit --dry-run
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
Write-Output 'PHASE171_R19_FOCUSED_PYTEST_START'
python -m pytest -q -p no:cacheprovider .\phase171_r2j_r4_r9_r19_right_end_diagnostic\tests\test_audit.py
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
Write-Output 'PHASE171_R19_FOCUSED_PYTEST=PASS'
python -m phase171_r2j_r4_r9_r19_right_end_diagnostic.audit
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
Write-Output 'PHASE171_R19_RESULT=PASS_READ_ONLY_RIGHT_END_AUDIT'

```
