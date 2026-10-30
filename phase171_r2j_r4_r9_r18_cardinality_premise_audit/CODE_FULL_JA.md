# Phase 171 R18：変更・追加コードの全文

既存ファイル、クラス、関数、import は変更しない。追加位置は新規パッケージ `phase171_r2j_r4_r9_r18_cardinality_premise_audit/` 内。

## 新規 `audit.py`（import・関数全文）

`audit.py`

```python
"""Phase 171 R18: read-only public cardinality premise and matcher audit.

No provider, source registry, canonical resolver, or proof tree is modified.
The three independent premises are inspected without feeding their proof
steps back into public search. Derived matches are diagnostic only.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any

from phase171_r2j_r4_r9_r17_public_context_path_audit import audit as r17
from phase171_r2j_r4_r9_r16_hopf_route_audit import audit as r16

PACKAGE = Path(__file__).resolve().parent
ROOT = PACKAGE.parent
OUTPUT = PACKAGE / "output" / "audit.json"
PRIOR_REPORT = ROOT / "phase171_r2j_r4_r9_r17_public_context_path_audit" / "output" / "audit.json"
SOURCE_MODULE = "phase165_r52_r9_shared_math.py"
REVIEWED_BLOB = "10d3303e6b3a52246f1cfb8a8998f3a67be0b0ac"
ROUTE_NAME = "finite middle-group cardinality from short exact sequence"
PARTS = ("left_end_group", "short_exact", "right_end_group")


def preflight() -> dict[str, Any]:
    """Require the reviewed provider and positive R17 audit on develop."""
    ready = r16.preflight()
    if ready["provider_blob"] != REVIEWED_BLOB:
        raise RuntimeError("R18 reviewed provider changed")
    if not PRIOR_REPORT.is_file():
        raise RuntimeError("R17 output/audit.json is missing")
    prior_data = PRIOR_REPORT.read_bytes()
    prior = json.loads(prior_data.decode("utf-8-sig"))
    if prior.get("phase") != "171-R2J-R4-R9-R17":
        raise RuntimeError("unexpected R17 report phase")
    if (prior.get("source_changes") != 0 or prior.get("new_given") != 0
            or prior.get("public_root_status") != "partial"):
        raise RuntimeError("R17 source purity or public baseline changed")
    states = prior.get("probe_statuses", {})
    for label in ("screened", "public"):
        branch = states.get(label, {})
        if branch.get("short_exact") != "proved" or branch.get("cardinality") != "unresolved":
            raise RuntimeError("R17 cardinality boundary was not reproduced: " + label)
    return {
        **ready,
        "r17_sha256": hashlib.sha256(prior_data).hexdigest(),
        "r17_source_comparison": prior.get("source_comparison"),
    }


def cardinality_route(provider: object, target: object) -> object:
    """Extract one real typed backward route, not an artificial proof tree."""
    from phase171_r2j_r4_r6_middle_cardinality.source import FiniteGroupCardinality
    from phase171_r2j_r4_r5_short_exact_sequence.source import EHPShortExactSequence
    from proof import Relation, RelationType
    from homotopy_groups import FiniteCyclicGroup, TodaPrimaryGroup

    if target != FiniteGroupCardinality(TodaPrimaryGroup(6, 3), 4):
        raise ValueError("R18 audits only the registered order-four target")
    proposals = provider(target)
    if not isinstance(proposals, tuple):
        raise TypeError("provider must return a tuple")
    found = [option for option in proposals if getattr(option.rule, "name", None) == ROUTE_NAME]
    if len(found) != 1:
        raise RuntimeError("expected one source-backed cardinality route, found " + str(len(found)))
    option = found[0]
    if len(option.subgoals) != 3:
        raise RuntimeError("cardinality route must have exactly three premises")
    left, sequence, right = option.subgoals
    if (not isinstance(left, Relation) or not isinstance(right, Relation)
            or left.relation_type is not RelationType.EQUALITY
            or right.relation_type is not RelationType.EQUALITY
            or not isinstance(left.rhs, FiniteCyclicGroup)
            or not isinstance(right.rhs, FiniteCyclicGroup)
            or left.lhs != TodaPrimaryGroup(5, 2)
            or right.lhs != TodaPrimaryGroup(6, 5)
            or left.rhs.order != 2 or right.rhs.order != 2
            or not isinstance(sequence, EHPShortExactSequence)
            or sequence.middle_group != target.group):
        raise RuntimeError("invalid mathematical shape of R18 cardinality premises")
    return option


def proof_source_check(root: object, bridge: object, citing: str, group_goal: object) -> dict[str, Any]:
    """Re-check all GIVEN ancestry against earlier screened fixed citations."""
    from proof import ProofRule
    from phase166_r3c_publication_order import precedes_citing_assertion
    from unified_statement_registry import AssertionOrigin

    leaves = r16.proof_leaves(root)
    cited: list[str] = []
    for leaf in leaves:
        if leaf.conclusion == group_goal:
            raise RuntimeError("forbidden completed pi6^3 GIVEN")
        matches = []
        for link in bridge.proof_links:
            if link.step is None or link.step.rule is not ProofRule.GIVEN:
                continue
            assertion = bridge.registry.assertion(link.assertion_id)
            if (assertion.origin is AssertionOrigin.FIXED_STATEMENT
                    and assertion.content == leaf.conclusion
                    and link.step.conclusion == leaf.conclusion
                    and precedes_citing_assertion(bridge, link.assertion_id, citing)):
                matches.append(link.assertion_id)
        if len(matches) != 1:
            raise RuntimeError("leaf lacks one screened earlier citation: " + repr(leaf.conclusion))
        cited.append(matches[0])
    return {"given_leaves": len(leaves), "source_ids": cited}


def probe_premise(goal: object, provider: object, bridge: object, citing: str,
                  group_goal: object) -> tuple[dict[str, Any], object | None]:
    """Use canonical reconstruction independently, including legitimate fixed GIVEN leaves."""
    from phase165_r3_recursive_search import RegisteredGoalUnresolved, reconstruct_registered_goal
    from proof import ProofRule

    routes = provider(goal)
    if not isinstance(routes, tuple):
        raise TypeError("provider must return a tuple")
    try:
        step = reconstruct_registered_goal(
            goal, bridge, citing, provider,
            lookup_mode="typed_reference_publication",
        )
    except RegisteredGoalUnresolved as exc:
        return ({
            "status": "unresolved", "error": str(exc)[:1500],
            "provider_route_count": len(routes),
            "provider_rule_names": [getattr(option.rule, "name", "") for option in routes[:20]],
            "goal": repr(goal), "given_leaves": None, "source_ids": None,
        }, None)
    if step.conclusion != goal or step.rule not in (ProofRule.GIVEN, ProofRule.INFERENCE):
        raise RuntimeError("canonical resolver returned the wrong conclusion")
    sources = proof_source_check(step, bridge, citing, group_goal)
    return ({
        "status": "proved", "error": None,
        "proof_rule": step.rule.value if hasattr(step.rule, "value") else step.rule.name,
        "provider_route_count": len(routes),
        "provider_rule_names": [getattr(option.rule, "name", "") for option in routes[:20]],
        "goal": repr(goal), **sources,
    }, step)


def classify(premises: dict[str, str], matcher_count: int | None,
             cardinality_status: str) -> str:
    """Classify observations without claiming completion from an isolated match."""
    if any(premises.get(name) != "proved" for name in PARTS):
        return "CARDINALITY_PREMISE_NOT_INDEPENDENTLY_PROVED"
    if matcher_count == 0:
        return "CARDINALITY_MATCHER_REJECTS_PROVED_PREMISES"
    if matcher_count is None or matcher_count > 1:
        return "CARDINALITY_MATCH_AMBIGUOUS_OR_UNOBSERVED"
    if cardinality_status == "proved":
        return "CARDINALITY_INDEPENDENTLY_PROVED"
    return "CARDINALITY_VALID_PREMISES_BUT_RECURSIVE_PATH_UNRESOLVED"


def inspect() -> dict[str, Any]:
    """Compare independent obligations in actual public vs R2I screened contexts."""
    from phase165_r52_r9_shared_math import build_shared_typed_bridge, shared_expansion_provider
    from phase165_r55_nk_only_goal import search_group_from_registered_goal
    from phase171_r2i_eta_hopf_bridge.audit import _screened_context
    from phase171_r2j_r4_r6_middle_cardinality.source import FiniteGroupCardinality
    from homotopy_groups import TodaPrimaryGroup
    from proof import ProofRule, find_inference_matches_for_rule
    from phase164_r8_proofstep_factory import derive_inference_proof_step

    screened, root, citing = _screened_context()
    contexts: list[object] = []
    public = search_group_from_registered_goal(
        n=3, k=3, bridge=build_shared_typed_bridge(), goal=root,
        context_sink=contexts.append,
    )
    if len(contexts) != 1:
        raise RuntimeError("actual public search did not expose one context")
    actual_public = contexts[0]
    actual_ids = r17.linked_fixed_ids(actual_public)
    screened_ids = r17.linked_fixed_ids(screened)
    prior = json.loads(PRIOR_REPORT.read_text(encoding="utf-8-sig"))
    comparison = r17.source_comparison(screened_ids, actual_ids)
    if comparison != prior["source_comparison"]:
        raise RuntimeError("R17 screened/public source identities changed")
    cardinality = FiniteGroupCardinality(TodaPrimaryGroup(6, 3), 4)
    rows: dict[str, Any] = {}
    for label, context in (("screened", screened), ("public", actual_public)):
        provider = shared_expansion_provider(context, proof_target=root)
        expansion = cardinality_route(provider, cardinality)
        parts = {}
        steps = []
        for name, subgoal in zip(PARTS, expansion.subgoals):
            observed, step = probe_premise(subgoal, provider, context, citing, root)
            parts[name] = observed
            steps.append(step)
        statuses = {name: parts[name]["status"] for name in PARTS}
        match_count: int | None = None
        derived = False
        if all(step is not None for step in steps):
            matches = tuple(match for match in find_inference_matches_for_rule(expansion.rule, tuple(steps))
                            if len(match.premises) == 3
                            and all(a is b for a, b in zip(match.premises, steps)))
            match_count = len(matches)
            if match_count == 1:
                inferred = derive_inference_proof_step(matches[0])
                if inferred.conclusion != cardinality or inferred.rule is not ProofRule.INFERENCE:
                    raise RuntimeError("cardinality rule produced incorrect statement")
                proof_source_check(inferred, context, citing, root)
                derived = True
        direct, _step = probe_premise(cardinality, provider, context, citing, root)
        rows[label] = {
            "premises": parts,
            "premise_statuses": statuses,
            "matcher_count": match_count,
            "independent_inference_matched": derived,
            "cardinality_direct": direct,
            "classification": classify(statuses, match_count, direct["status"]),
            "route_name": expansion.rule.name,
        }
    return {
        "phase": "171-R2J-R4-R9-R18",
        "mode": "AUDIT_ONLY_CARDINALITY_THREE_PREMISES_AND_INFERENCE_MATCH",
        "public_root_status": public.status.value,
        "source_comparison": comparison,
        "contexts": rows,
        "classification": rows["public"]["classification"],
        "new_given": 0,
        "source_changes": 0,
        "completed_proof_imported": False,
        "trust_boundary_modified": False,
        "public_complete": False,
        "full_pytest": False,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    ready = preflight()
    print("PHASE171_R18_BRANCH=" + ready["branch"], flush=True)
    print("PHASE171_R18_HEAD=" + ready["head"], flush=True)
    print("PHASE171_R18_R17_REPORT=PASS", flush=True)
    print("PHASE171_R18_REVIEWED_PROVIDER=PASS", flush=True)
    if args.dry_run:
        print("PHASE171_R18_RESULT=PASS_DRY_RUN", flush=True)
        return
    before = r17.git_read("status", "--porcelain", "--untracked-files=no")
    report = inspect()
    after = r17.git_read("status", "--porcelain", "--untracked-files=no")
    if before != after:
        raise RuntimeError("R18 changed tracked files during audit")
    report["git_head"] = ready["head"]
    report["r17_sha256"] = ready["r17_sha256"]
    report["tracked_status_unchanged"] = True
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print("PHASE171_R18_PUBLIC_ROOT=" + report["public_root_status"], flush=True)
    print("PHASE171_R18_SOURCE_ID_SET_EQUAL=" + str(report["source_comparison"]["same_id_set"]), flush=True)
    for name, value in report["contexts"].items():
        print("PHASE171_R18_" + name.upper() + "_PREMISES="
              + json.dumps(value["premise_statuses"], ensure_ascii=False), flush=True)
        print("PHASE171_R18_" + name.upper() + "_MATCH_COUNT=" + str(value["matcher_count"]), flush=True)
        print("PHASE171_R18_" + name.upper() + "_CARDINALITY="
              + value["cardinality_direct"]["status"], flush=True)
    print("PHASE171_R18_CLASSIFICATION=" + report["classification"], flush=True)
    print("PHASE171_R18_NEW_GIVEN=0", flush=True)
    print("PHASE171_R18_SOURCE_CHANGES=0", flush=True)
    print("PHASE171_R18_TRACKED_STATUS_UNCHANGED=PASS", flush=True)
    print("PHASE171_R18_REPORT=" + str(OUTPUT), flush=True)
    print("PHASE171_R18_RESULT=PASS_AUDIT_ONLY", flush=True)


if __name__ == "__main__":
    main()
```

## 新規 `tests/test_audit.py`（import・テスト関数全文）

`tests/test_audit.py`

```python
"""Focused read-only cardinality-premise and rule-matcher tests."""
from __future__ import annotations

import pytest

from phase171_r2j_r4_r9_r18_cardinality_premise_audit import audit


def test_preflight_requires_r17_and_reviewed_provider():
    ready = audit.preflight()
    assert ready["branch"] == "develop"
    assert ready["provider_blob"] == audit.REVIEWED_BLOB
    assert len(ready["r17_sha256"]) == 64


def test_rejects_mutating_git():
    with pytest.raises(ValueError):
        audit.r17.git_read("reset", "--hard")
    with pytest.raises(ValueError):
        audit.r16.git_read("checkout", "--", audit.SOURCE_MODULE)


def test_classification_identifies_specific_missing_premise():
    for name in audit.PARTS:
        statuses = {part: "proved" for part in audit.PARTS}
        statuses[name] = "unresolved"
        assert audit.classify(statuses, None, "unresolved") == "CARDINALITY_PREMISE_NOT_INDEPENDENTLY_PROVED"


def test_classification_preserves_inference_and_search_distinction():
    complete = {name: "proved" for name in audit.PARTS}
    assert audit.classify(complete, 0, "unresolved") == "CARDINALITY_MATCHER_REJECTS_PROVED_PREMISES"
    assert audit.classify(complete, 2, "unresolved") == "CARDINALITY_MATCH_AMBIGUOUS_OR_UNOBSERVED"
    assert audit.classify(complete, 1, "unresolved") == "CARDINALITY_VALID_PREMISES_BUT_RECURSIVE_PATH_UNRESOLVED"
    assert audit.classify(complete, 1, "proved") == "CARDINALITY_INDEPENDENTLY_PROVED"


def test_public_cardinality_has_one_checked_source_backed_route():
    from homotopy_groups import TodaPrimaryGroup
    from phase165_r52_r9_shared_math import shared_expansion_provider
    from phase171_r2i_eta_hopf_bridge.audit import _screened_context
    from phase171_r2j_r4_r6_middle_cardinality.source import FiniteGroupCardinality
    bridge, root, _ = _screened_context()
    provider = shared_expansion_provider(bridge, proof_target=root)
    goal = FiniteGroupCardinality(TodaPrimaryGroup(6, 3), 4)
    option = audit.cardinality_route(provider, goal)
    assert option.rule.name == audit.ROUTE_NAME
    assert len(option.subgoals) == 3


def test_reject_wrong_cardinality_goal():
    from homotopy_groups import TodaPrimaryGroup
    from phase171_r2j_r4_r6_middle_cardinality.source import FiniteGroupCardinality
    with pytest.raises(ValueError):
        audit.cardinality_route(lambda goal: (), FiniteGroupCardinality(TodaPrimaryGroup(6, 3), 8))


def test_read_only_live_audit_does_not_promote_independent_proof_to_root():
    result = audit.inspect()
    assert result["source_changes"] == 0
    assert result["new_given"] == 0
    assert result["completed_proof_imported"] is False
    assert result["public_root_status"] == "partial"
    assert result["source_comparison"]["same_id_set"] is False
    assert result["classification"] in (
        "CARDINALITY_PREMISE_NOT_INDEPENDENTLY_PROVED",
        "CARDINALITY_MATCHER_REJECTS_PROVED_PREMISES",
        "CARDINALITY_MATCH_AMBIGUOUS_OR_UNOBSERVED",
        "CARDINALITY_VALID_PREMISES_BUT_RECURSIVE_PATH_UNRESOLVED",
        "CARDINALITY_INDEPENDENTLY_PROVED",
    )
```

## 新規 `run.ps1`（全文）

`run.ps1`

```powershell
param(
    [switch]$DryRun
)
$ErrorActionPreference = 'Stop'
$Package = Split-Path -Parent $MyInvocation.MyCommand.Path
$Root = Split-Path -Parent $Package
Push-Location $Root
try {
    & python -m phase171_r2j_r4_r9_r18_cardinality_premise_audit.audit --dry-run
    if ($LASTEXITCODE -ne 0) { throw 'R18 preflight failed' }
    if ($DryRun) {
        Write-Output 'PHASE171_R18_DRY_RUN=PASS'
        exit 0
    }
    Write-Output 'PHASE171_R18_FOCUSED_PYTEST_START'
    & python -m pytest -q -p no:cacheprovider 'phase171_r2j_r4_r9_r18_cardinality_premise_audit/tests/test_audit.py'
    if ($LASTEXITCODE -ne 0) { throw 'R18 focused pytest failed' }
    Write-Output 'PHASE171_R18_FOCUSED_PYTEST=PASS'
    & python -m phase171_r2j_r4_r9_r18_cardinality_premise_audit.audit
    if ($LASTEXITCODE -ne 0) { throw 'R18 audit failed' }
    Write-Output 'PHASE171_R18_RESULT=PASS_READ_ONLY_CARDINALITY_AUDIT'
}
finally {
    Pop-Location
}
```

## 新規パッケージ import

`__init__.py`

```python
"""R18 cardinality premise audit package."""
```

## 新規テストパッケージ import

`tests/__init__.py`

```python
"""R18 focused tests."""
```

