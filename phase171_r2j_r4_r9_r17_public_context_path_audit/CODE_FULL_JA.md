# Phase 171 R17 — 追加コード全文

既存の import、クラス、関数は変更しない。以下の各ファイルを示した新規ディレクトリに追加する。

## `phase171_r2j_r4_r9_r17_public_context_path_audit/audit.py`

```python
"""Phase 171 R17: compare independent and actual public EHP proof contexts.

The canonical resolver is invoked without preloaded steps. This audit neither
patches the shared provider nor supplies previously completed proof trees.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from pathlib import Path
from typing import Any

from phase171_r2j_r4_r9_r16_hopf_route_audit import audit as r16

PACKAGE = Path(__file__).resolve().parent
ROOT = PACKAGE.parent
OUTPUT = PACKAGE / "output" / "audit.json"
R16_REPORT = ROOT / "phase171_r2j_r4_r9_r16_hopf_route_audit" / "output" / "audit.json"
PROBES = ("hopf_7", "hopf_6", "delta_zero", "suspension_injective",
          "short_exact", "cardinality", "element_order", "cyclic_structure")
MAP_PROBES = PROBES[:4]


def git_read(*args: str) -> bytes:
    """Allow read-only inspection only."""
    if args not in {
        ("status", "--porcelain", "--untracked-files=no"),
        ("branch", "--show-current"),
        ("rev-parse", "HEAD"),
    }:
        raise ValueError("R17 prohibits mutating Git operations")
    return subprocess.run(["git", *args], cwd=ROOT,
                          capture_output=True, check=True).stdout


def preflight() -> dict[str, str]:
    """Reuse R16's reviewed provider guard and require its audited result."""
    checked = r16.preflight()
    if not R16_REPORT.is_file():
        raise RuntimeError("R16 output/audit.json is required")
    record = json.loads(R16_REPORT.read_text(encoding="utf-8-sig"))
    if record.get("phase") != "171-R2J-R4-R9-R16":
        raise RuntimeError("not the reviewed R16 report")
    if record.get("new_given") != 0 or record.get("source_changes") != 0:
        raise RuntimeError("R16 source purity was not retained")
    for key in MAP_PROBES:
        item = record.get("probes", {}).get(key)
        if not isinstance(item, dict) or item.get("status") != "proved":
            raise RuntimeError("R16 map proof is not verified: " + key)
    checked["r16_sha256"] = hashlib.sha256(R16_REPORT.read_bytes()).hexdigest()
    return checked


def linked_fixed_ids(bridge: object) -> tuple[str, ...]:
    """Use exact linked fixed source IDs, never counted database candidates."""
    from proof import ProofRule
    from unified_statement_registry import AssertionOrigin

    ids = []
    for link in bridge.proof_links:
        if link.step is None or link.step.rule is not ProofRule.GIVEN:
            continue
        assertion = bridge.registry.assertion(link.assertion_id)
        if (assertion.origin is AssertionOrigin.FIXED_STATEMENT
                and link.step.conclusion == assertion.content):
            ids.append(link.assertion_id)
    return tuple(ids)


def source_comparison(screened: tuple[str, ...], public: tuple[str, ...]) -> dict[str, Any]:
    """Compare source identities, preserving their ordering and multiplicity."""
    screened_set = set(screened)
    public_set = set(public)
    return {
        "screened_fixed_count": len(screened),
        "public_fixed_count": len(public),
        "same_ordered_ids": screened == public,
        "same_id_set": screened_set == public_set,
        "screened_only": [item for item in screened if item not in public_set],
        "public_only": [item for item in public if item not in screened_set],
    }


def checked_targets(group_goal: object, provider: object) -> dict[str, object]:
    """Construct typed obligations, without inventing a proof or group fact."""
    from homotopy_groups import (
        FiniteCyclicGroup, TodaDeltaMap, TodaHopfInvariantMap,
        TodaPrimaryGroup, TodaSuspensionMap,
    )
    from phase165_r12_r2_quotient_rules import CyclicStructureStatement
    from phase165_r14_r6_generic_iso import MapInjective, MapSurjective
    from phase171_r2j_r4_r5_short_exact_sequence.source import EHPShortExactSequence
    from phase171_r2j_r4_r6_middle_cardinality.source import FiniteGroupCardinality
    from phase171_r2j_r4_r7_nonzero_nu_order.source import FiniteElementOrder
    from proof import Relation, RelationType
    from toda_rules import TodaDeltaZeroStatement

    if (not isinstance(group_goal, Relation)
            or group_goal.relation_type is not RelationType.EQUALITY
            or group_goal.lhs != TodaPrimaryGroup(6, 3)
            or not isinstance(group_goal.rhs, FiniteCyclicGroup)
            or group_goal.rhs.order != 4):
        raise RuntimeError("unexpected typed pi_6^3 root target")
    a, b, c = TodaPrimaryGroup(5, 2), TodaPrimaryGroup(6, 3), TodaPrimaryGroup(6, 5)
    d = TodaPrimaryGroup(7, 5)
    e_map = TodaSuspensionMap(a, b)
    h6_map = TodaHopfInvariantMap(b, c)
    h7_map = TodaHopfInvariantMap(TodaPrimaryGroup(7, 3), d)
    sequence = EHPShortExactSequence(a, b, c, e_map, h6_map)
    root_routes = provider(group_goal)
    if not isinstance(root_routes, tuple):
        raise TypeError("provider did not return a tuple")
    typed_element_order: list[object] = []
    typed_cyclic: list[object] = []
    for option in root_routes:
        for child in option.subgoals:
            if isinstance(child, FiniteElementOrder) and child not in typed_element_order:
                typed_element_order.append(child)
            if isinstance(child, CyclicStructureStatement) and child not in typed_cyclic:
                typed_cyclic.append(child)
    if len(typed_element_order) != 1 or len(typed_cyclic) != 1:
        raise RuntimeError("root generator/order obligations are not unique")
    targets = {
        "hopf_7": MapSurjective(h7_map),
        "hopf_6": MapSurjective(h6_map),
        "delta_zero": TodaDeltaZeroStatement(TodaDeltaMap(d, a)),
        "suspension_injective": MapInjective(e_map),
        "short_exact": sequence,
        "cardinality": FiniteGroupCardinality(b, 4),
        "element_order": typed_element_order[0],
        "cyclic_structure": typed_cyclic[0],
    }
    if tuple(targets) != PROBES:
        raise RuntimeError("probe list changed")
    return targets


def classify(summary: dict[str, Any], public_status: str) -> str:
    """Do not promote a successful subgoal into a completed group proof."""
    if public_status == "complete":
        return "PUBLIC_ROOT_COMPLETE_NEEDS_TRUST_BOUNDARY_REVIEW"
    independent, public = summary["screened"], summary["public"]
    if any(independent[k] == "proved" and public[k] != "proved" for k in MAP_PROBES):
        return "PUBLIC_CONTEXT_MAP_DISAGREEMENT"
    if all(public[k] == "proved" for k in MAP_PROBES):
        if public["short_exact"] != "proved":
            return "SHORT_EXACT_COMPOSITION_MISSING"
        if public["cardinality"] != "proved":
            return "CARDINALITY_COMPOSITION_MISSING"
        if public["element_order"] != "proved":
            return "ELEMENT_ORDER_COMPOSITION_MISSING"
        if public["cyclic_structure"] != "proved":
            return "CYCLIC_STRUCTURE_COMPOSITION_MISSING"
        return "ROOT_PATH_DEPENDENT_DESPITE_INDEPENDENT_SUBGOALS"
    return "MULTIPLE_CONTEXTUAL_FAILURES_NEED_INSPECTION"


def inspect() -> dict[str, Any]:
    """Run public search once, then probe exact goals against both contexts."""
    from phase165_r52_r9_shared_math import (
        build_shared_typed_bridge, shared_expansion_provider,
    )
    from phase165_r55_nk_only_goal import search_group_from_registered_goal
    from phase171_r2i_eta_hopf_bridge.audit import _screened_context
    from phase166_r3t_goal_source_binding.goal_source import resolve_specialized_goal_citing_id

    screened, target, citing = _screened_context()
    contexts: list[object] = []
    public_result = search_group_from_registered_goal(
        n=3, k=3, bridge=build_shared_typed_bridge(),
        goal=target, context_sink=contexts.append,
    )
    if len(contexts) != 1:
        raise RuntimeError("expected one actual public proof context")
    actual_public = contexts[0]
    if resolve_specialized_goal_citing_id(actual_public, target) != citing:
        raise RuntimeError("publication goal position changed between contexts")
    screened_ids = linked_fixed_ids(screened)
    public_ids = linked_fixed_ids(actual_public)
    contexts_equal = source_comparison(screened_ids, public_ids)

    snapshots = {}
    probe_outcomes = {}
    for context_name, context in (("screened", screened), ("public", actual_public)):
        provider = shared_expansion_provider(context, proof_target=target)
        targets = checked_targets(target, provider)
        observations = {}
        for name, goal in targets.items():
            observations[name] = r16.independent_probe(goal, provider, context, citing)
        snapshots[context_name] = observations
        probe_outcomes[context_name] = {
            name: observations[name]["status"] for name in PROBES
        }
    status = public_result.status.value
    comparison = {
        name: {
            "screened": probe_outcomes["screened"][name],
            "public": probe_outcomes["public"][name],
            "same_status": probe_outcomes["screened"][name] == probe_outcomes["public"][name],
        }
        for name in PROBES
    }
    return {
        "phase": "171-R2J-R4-R9-R17",
        "mode": "AUDIT_ONLY_CONTEXT_AND_PATH_DEPENDENCY",
        "public_root_status": status,
        "public_root_open_count": len(public_result.open_goals),
        "public_root_proved_steps": len(public_result.proven_steps),
        "citing_assertion_id": citing,
        "source_comparison": contexts_equal,
        "probe_statuses": probe_outcomes,
        "probe_comparison": comparison,
        "probes": snapshots,
        "classification": classify(probe_outcomes, status),
        "new_given": 0,
        "source_changes": 0,
        "proof_tree_imported": False,
        "trust_boundary_modified": False,
        "public_complete": status == "complete",
        "full_pytest": False,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    checked = preflight()
    print("PHASE171_R17_BRANCH=" + checked["branch"], flush=True)
    print("PHASE171_R17_HEAD=" + checked["head"], flush=True)
    print("PHASE171_R17_PROVIDER_BLOB=PASS", flush=True)
    print("PHASE171_R17_R16_REPORT=PASS", flush=True)
    if args.dry_run:
        print("PHASE171_R17_RESULT=PASS_DRY_RUN", flush=True)
        return
    before = git_read("status", "--porcelain", "--untracked-files=no")
    report = inspect()
    after = git_read("status", "--porcelain", "--untracked-files=no")
    if before != after:
        raise RuntimeError("tracked source changed during read-only R17 audit")
    report["git_head"] = checked["head"]
    report["r16_sha256"] = checked["r16_sha256"]
    report["tracked_status_unchanged"] = True
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print("PHASE171_R17_PUBLIC_ROOT=" + report["public_root_status"], flush=True)
    print("PHASE171_R17_CONTEXT_SAME_ID_SET=" + str(report["source_comparison"]["same_id_set"]), flush=True)
    print("PHASE171_R17_PROBE_STATUSES=" + json.dumps(report["probe_statuses"], ensure_ascii=False), flush=True)
    print("PHASE171_R17_CLASSIFICATION=" + report["classification"], flush=True)
    print("PHASE171_R17_SOURCE_CHANGES=0", flush=True)
    print("PHASE171_R17_NEW_GIVEN=0", flush=True)
    print("PHASE171_R17_TRACKED_STATUS_UNCHANGED=PASS", flush=True)
    print("PHASE171_R17_REPORT=" + str(OUTPUT), flush=True)
    print("PHASE171_R17_RESULT=PASS_AUDIT_ONLY", flush=True)


if __name__ == "__main__":
    main()
```

## `phase171_r2j_r4_r9_r17_public_context_path_audit/tests/test_audit.py`

```python
"""Focused R17 context-comparison and independent-goal audit tests."""
from __future__ import annotations

import pytest

from phase171_r2j_r4_r9_r17_public_context_path_audit import audit


def _states(default="unresolved"):
    return {name: default for name in audit.PROBES}


def test_refuses_mutating_git_commands():
    with pytest.raises(ValueError):
        audit.git_read("reset", "--hard")
    with pytest.raises(ValueError):
        audit.git_read("add", "phase165_r52_r9_shared_math.py")


def test_r16_baseline_and_provider_are_reviewed():
    ready = audit.preflight()
    assert ready["branch"] == "develop"
    assert ready["provider_blob"] == audit.r16.REVIEWED_PROVIDER_BLOB
    assert len(ready["r16_sha256"]) == 64


def test_source_comparison_detects_differences_without_normalizing_ids():
    result = audit.source_comparison(("a", "b"), ("b", "a"))
    assert result["same_ordered_ids"] is False
    assert result["same_id_set"] is True
    assert result["screened_only"] == []
    assert result["public_only"] == []
    changed = audit.source_comparison(("a", "b"), ("a", "c"))
    assert changed["screened_only"] == ["b"]
    assert changed["public_only"] == ["c"]


def test_map_disagreement_takes_priority():
    screened = _states("proved")
    public = _states("proved")
    public["hopf_7"] = "unresolved"
    assert audit.classify({"screened": screened, "public": public}, "partial") == "PUBLIC_CONTEXT_MAP_DISAGREEMENT"


def test_deeper_dependency_failures_have_separate_classes():
    base = _states("proved")
    for goal, expected in (
        ("short_exact", "SHORT_EXACT_COMPOSITION_MISSING"),
        ("cardinality", "CARDINALITY_COMPOSITION_MISSING"),
        ("element_order", "ELEMENT_ORDER_COMPOSITION_MISSING"),
        ("cyclic_structure", "CYCLIC_STRUCTURE_COMPOSITION_MISSING"),
    ):
        public = dict(base)
        public[goal] = "unresolved"
        assert audit.classify({"screened": base, "public": public}, "partial") == expected


def test_proved_subgoals_do_not_claim_group_completion():
    complete_individually = _states("proved")
    pair = {"screened": complete_individually, "public": complete_individually}
    assert audit.classify(pair, "partial") == "ROOT_PATH_DEPENDENT_DESPITE_INDEPENDENT_SUBGOALS"
    assert audit.classify(pair, "complete") == "PUBLIC_ROOT_COMPLETE_NEEDS_TRUST_BOUNDARY_REVIEW"
```

## `phase171_r2j_r4_r9_r17_public_context_path_audit/run.ps1`

```powershell
param(
    [switch]$DryRun
)
$ErrorActionPreference = 'Stop'
$Package = Split-Path -Parent $MyInvocation.MyCommand.Path
$Root = Split-Path -Parent $Package
Push-Location $Root
try {
    & python -m phase171_r2j_r4_r9_r17_public_context_path_audit.audit --dry-run
    if ($LASTEXITCODE -ne 0) { throw 'R17 preflight failed' }
    if ($DryRun) {
        Write-Output 'PHASE171_R17_DRY_RUN=PASS'
        exit 0
    }
    Write-Output 'PHASE171_R17_FOCUSED_PYTEST_START'
    & python -m pytest -q -p no:cacheprovider 'phase171_r2j_r4_r9_r17_public_context_path_audit/tests/test_audit.py'
    if ($LASTEXITCODE -ne 0) { throw 'R17 focused pytest failed' }
    Write-Output 'PHASE171_R17_FOCUSED_PYTEST=PASS'
    & python -m phase171_r2j_r4_r9_r17_public_context_path_audit.audit
    if ($LASTEXITCODE -ne 0) { throw 'R17 audit failed' }
    Write-Output 'PHASE171_R17_RESULT=PASS_READ_ONLY_CONTEXT_PATH_AUDIT'
}
finally {
    Pop-Location
}
```

## `phase171_r2j_r4_r9_r17_public_context_path_audit/__init__.py`

```python
"""Phase 171 R17 context-path audit package."""
```

## `phase171_r2j_r4_r9_r17_public_context_path_audit/tests/__init__.py`

```python
"""R17 focused tests."""
```
