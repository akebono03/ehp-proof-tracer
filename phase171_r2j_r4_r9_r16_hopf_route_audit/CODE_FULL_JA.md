# Phase 171 R16 — 新規コード全文

既存コードは変更しない。新規ファイル・関数はリポジトリ直下の `phase171_r2j_r4_r9_r16_hopf_route_audit/` 内に置く。トップレベル import の変更も既存クラス・関数の変更もない。以下は追加するコード全文である。

## `audit.py`

```python
"""Phase 171 R16: audit EHP map obligations without altering proof search.

The existing canonical resolver is called independently for each genuine map
obligation. This program does not add mathematical rules, source assertions,
ProofSteps, search shortcuts, or admitted completed proofs.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
from pathlib import Path
from typing import Any

PACKAGE = Path(__file__).resolve().parent
ROOT = PACKAGE.parent
REPORT_R14 = ROOT / "phase171_r2j_r4_r9_r14_root_branch_diagnostic" / "output" / "audit.json"
REPORT_R15 = ROOT / "phase171_r2j_r4_r9_r15_branch_blocker_audit" / "output" / "audit.json"
OUTPUT = PACKAGE / "output" / "audit.json"
PROVIDER_NAME = "phase165_r52_r9_shared_math.py"
PROVIDER_PATH = ROOT / PROVIDER_NAME
REVIEWED_PROVIDER_BLOB = "10d3303e6b3a52246f1cfb8a8998f3a67be0b0ac"


def git_read(*args: str) -> bytes:
    """Only read the branch, HEAD, tracked status and reviewed provider blob."""
    allowed = {
        ("branch", "--show-current"),
        ("rev-parse", "HEAD"),
        ("show", "HEAD:" + PROVIDER_NAME),
        ("status", "--porcelain", "--untracked-files=no"),
    }
    if args not in allowed:
        raise ValueError("R16 supports read-only Git commands only")
    return subprocess.run(
        ["git", *args], cwd=ROOT, capture_output=True, check=True,
    ).stdout


def blob_sha(data: bytes) -> str:
    return hashlib.sha1(("blob %d\0" % len(data)).encode("ascii") + data).hexdigest()


def normalize(data: bytes) -> str:
    return data.decode("utf-8-sig").replace("\r\n", "\n")


def preflight() -> dict[str, str]:
    branch = git_read("branch", "--show-current").decode("utf-8").strip()
    head = git_read("rev-parse", "HEAD").decode("utf-8").strip()
    committed = git_read("show", "HEAD:" + PROVIDER_NAME)
    if branch != "develop":
        raise RuntimeError("develop branch is required")
    if not re.fullmatch(r"[0-9a-f]{40}", head):
        raise RuntimeError("HEAD is not a SHA-1 identifier")
    if blob_sha(committed) != REVIEWED_PROVIDER_BLOB:
        raise RuntimeError("reviewed R11 provider changed: R16 must be reaudited")
    if normalize(PROVIDER_PATH.read_bytes()) != normalize(committed):
        raise RuntimeError("working provider differs from committed version")
    return {"branch": branch, "head": head, "provider_blob": blob_sha(committed)}


def read_prior_reports() -> dict[str, Any]:
    """Ensure R15 really summarizes the same, untruncated R14 trace."""
    if not REPORT_R14.is_file() or not REPORT_R15.is_file():
        raise RuntimeError("R14 and R15 output/audit.json files must both exist")
    r14_bytes = REPORT_R14.read_bytes()
    r15_bytes = REPORT_R15.read_bytes()
    r14 = json.loads(r14_bytes.decode("utf-8-sig"))
    r15 = json.loads(r15_bytes.decode("utf-8-sig"))
    if r14.get("phase") != "171-R2J-R4-R9-R14":
        raise RuntimeError("R14 report is not the reviewed canonical trace")
    if r15.get("phase") != "171-R2J-R4-R9-R15":
        raise RuntimeError("R15 report is not the reviewed blocker classification")
    if r14.get("origin_counts", {}).get("no_derivation") != 29:
        raise RuntimeError("R14 zero-derivation baseline changed")
    if r15.get("unique_no_derivation_goal_count") != 16:
        raise RuntimeError("R15 unresolved-goal baseline changed")
    if r15.get("blocker_classes") != {"PROPOSALS_UNPROVED": 15, "NO_EXPANSION": 1}:
        raise RuntimeError("R15 blocker distribution changed")
    if r15.get("r14_report_sha256") != hashlib.sha256(r14_bytes).hexdigest():
        raise RuntimeError("R14 report differs from the R15 analyzed input")
    if r14.get("provider_events_dropped") or r14.get("exception_events_dropped"):
        raise RuntimeError("R14 events were truncated")
    if r15.get("source_changes") != 0 or r15.get("new_given") != 0:
        raise RuntimeError("R15 audit contains source changes or added GIVEN")
    return {
        "r14_head": r14.get("git_head"),
        "r15_head": r15.get("git_head"),
        "r14_sha256": hashlib.sha256(r14_bytes).hexdigest(),
        "r15_sha256": hashlib.sha256(r15_bytes).hexdigest(),
        "r14_search": r14.get("public_status"),
        "r15_no_derivation_goals": 16,
        "r15_classes": r15["blocker_classes"],
    }


def observation_class(routes: list[dict[str, Any]], status: str) -> str:
    """Classify only directly observed canonical-search outcomes."""
    if status == "proved":
        return "INDEPENDENTLY_PROVED"
    if not routes:
        return "NO_PROVIDER_ROUTE"
    if status == "unresolved":
        return "ROUTES_EXIST_BUT_NOT_PROVED"
    return "UNEXPECTED_PROBE_STATUS"


def proof_leaves(root_step: object) -> tuple[object, ...]:
    """Walk a returned proof for audit only, without copying it into search."""
    from proof import ProofRule

    seen: set[int] = set()
    leaves: list[object] = []

    def visit(step: object) -> None:
        if id(step) in seen:
            return
        seen.add(id(step))
        if step.rule is ProofRule.GIVEN:
            if step.premises:
                raise RuntimeError("GIVEN cannot have any premises")
            leaves.append(step)
            return
        if step.rule is not ProofRule.INFERENCE:
            raise RuntimeError("unexpected proof rule in canonical ancestry")
        for parent in step.premises:
            visit(parent)

    visit(root_step)
    return tuple(leaves)


def independent_probe(goal: object, provider: object, bridge: object, citing: str) -> dict[str, Any]:
    """Try ordinary canonical reconstruction with no preloaded subproofs."""
    from phase165_r3_recursive_search import RegisteredGoalUnresolved, reconstruct_registered_goal
    from proof import ProofRule
    from unified_statement_registry import AssertionOrigin

    expansions = provider(goal)
    if not isinstance(expansions, tuple):
        raise TypeError("shared provider must return a tuple")
    routes = [
        {
            "rule": str(getattr(item.rule, "name", "")),
            "subgoals": [repr(subgoal)[:850] for subgoal in item.subgoals],
        }
        for item in expansions
    ]
    observer_events: list[tuple[str, str]] = []

    def observe(kind: str, current: object, step: object) -> None:
        if kind not in ("proved", "unresolved"):
            raise RuntimeError("unexpected canonical observer event")
        observer_events.append((kind, repr(current)[:500]))

    try:
        proof = reconstruct_registered_goal(
            goal, bridge, citing, provider,
            lookup_mode="typed_reference_publication",
            progress_observer=observe,
        )
    except RegisteredGoalUnresolved as exc:
        return {
            "status": "unresolved",
            "classification": observation_class(routes, "unresolved"),
            "goal": repr(goal),
            "provider_routes": routes,
            "provider_route_count": len(routes),
            "error": str(exc)[:1000],
            "proved_event_count": sum(kind == "proved" for kind, _ in observer_events),
            "unresolved_event_count": sum(kind == "unresolved" for kind, _ in observer_events),
            "first_unresolved": [value for kind, value in observer_events if kind == "unresolved"][:5],
            "screened_given_leaves": None,
        }
    if proof.conclusion != goal or proof.rule is not ProofRule.INFERENCE:
        raise RuntimeError("probe returned non-inferred or wrong conclusion")
    leaves = proof_leaves(proof)
    for leaf in leaves:
        matches = tuple(
            link for link in bridge.proof_links
            if link.step is not None
            and link.step.rule is ProofRule.GIVEN
            and link.step.conclusion == leaf.conclusion
            and bridge.registry.assertion(link.assertion_id).origin is AssertionOrigin.FIXED_STATEMENT
        )
        if len(matches) != 1:
            raise RuntimeError("canonical proof leaf lacks exactly one screened source")
    return {
        "status": "proved",
        "classification": observation_class(routes, "proved"),
        "goal": repr(goal),
        "provider_routes": routes,
        "provider_route_count": len(routes),
        "error": None,
        "proved_event_count": sum(kind == "proved" for kind, _ in observer_events),
        "unresolved_event_count": sum(kind == "unresolved" for kind, _ in observer_events),
        "first_unresolved": [value for kind, value in observer_events if kind == "unresolved"][:5],
        "screened_given_leaves": len(leaves),
    }


def inspect_live() -> dict[str, Any]:
    """Audit H7, H6, Delta-zero and E-injectivity independently of pi6^3 root."""
    from homotopy_groups import (
        TodaDeltaMap, TodaHopfInvariantMap, TodaPrimaryGroup,
        TodaSuspensionIsomorphismStatement, TodaSuspensionMap,
    )
    from phase165_r14_r6_generic_iso import MapInjective, MapSurjective
    from phase165_r52_r9_shared_math import shared_expansion_provider
    from phase171_r2i_eta_hopf_bridge.audit import _screened_context
    from toda_rules import TodaDeltaZeroStatement

    bridge, group_goal, citing = _screened_context()
    provider = shared_expansion_provider(bridge, proof_target=group_goal)
    a = TodaPrimaryGroup(5, 2)
    b = TodaPrimaryGroup(6, 3)
    right_6 = TodaPrimaryGroup(6, 5)
    right_7 = TodaPrimaryGroup(7, 5)
    suspension = TodaSuspensionMap(a, b)
    iso = TodaSuspensionIsomorphismStatement(suspension)
    iso_routes = provider(iso)
    if not isinstance(iso_routes, tuple):
        raise TypeError("shared provider returned non-tuple for isomorphism")
    # The 2-primary group orders 2 and 4 are known independently from Toda.
    # Never assert an isomorphism or promote this mathematical fact to GIVEN.
    if iso_routes:
        raise RuntimeError("an unexpected E-isomorphism proposal needs manual review")
    targets = {
        "hopf_7": MapSurjective(TodaHopfInvariantMap(TodaPrimaryGroup(7, 3), right_7)),
        "hopf_6": MapSurjective(TodaHopfInvariantMap(b, right_6)),
        "delta_zero": TodaDeltaZeroStatement(TodaDeltaMap(right_7, a)),
        "suspension_injective": MapInjective(suspension),
    }
    probes = {
        name: independent_probe(goal, provider, bridge, citing)
        for name, goal in targets.items()
    }
    h7 = probes["hopf_7"]
    if h7["status"] == "proved":
        classification = "H7_PROVED_INDEPENDENTLY_ROOT_PATH_DEPENDENCY_REVIEW"
    elif h7["provider_route_count"] > 0:
        classification = "H7_HAS_ROUTES_BUT_CANONICAL_PROOF_UNRESOLVED"
    else:
        classification = "H7_NO_PUBLIC_PROVIDER_ROUTE"
    return {
        "phase": "171-R2J-R4-R9-R16",
        "mode": "READ_ONLY_INDEPENDENT_EHP_MAP_OBLIGATION_PROBES",
        "root": repr(group_goal),
        "suspension_iso_goal": repr(iso),
        "suspension_iso_provider_routes": len(iso_routes),
        "suspension_iso_is_mathematically_false_at_2_primary": True,
        "known_2_primary_orders": {"pi5_s2": 2, "pi6_s3": 4},
        "probes": probes,
        "classification": classification,
        "source_changes": 0,
        "new_given": 0,
        "proof_tree_imported": False,
        "trust_boundary_modified": False,
        "public_complete": False,
        "full_pytest": False,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    ready = preflight()
    print("PHASE171_R16_BRANCH=" + ready["branch"], flush=True)
    print("PHASE171_R16_HEAD=" + ready["head"], flush=True)
    print("PHASE171_R16_R11_BASELINE=PASS", flush=True)
    if args.dry_run:
        print("PHASE171_R16_RESULT=PASS_DRY_RUN", flush=True)
        return
    before = git_read("status", "--porcelain", "--untracked-files=no")
    prior = read_prior_reports()
    report = inspect_live()
    if git_read("status", "--porcelain", "--untracked-files=no") != before:
        raise RuntimeError("tracked files changed during R16 read-only audit")
    report["prior_reports"] = prior
    report["git_head"] = ready["head"]
    report["tracked_status_unchanged"] = True
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("PHASE171_R16_FALSE_ISOMORPHISM_NO_ROUTE=" + str(report["suspension_iso_provider_routes"] == 0), flush=True)
    for name, result in report["probes"].items():
        print("PHASE171_R16_" + name.upper() + "=" + result["status"], flush=True)
        print("PHASE171_R16_" + name.upper() + "_ROUTES=" + str(result["provider_route_count"]), flush=True)
    print("PHASE171_R16_CLASSIFICATION=" + report["classification"], flush=True)
    print("PHASE171_R16_SOURCE_CHANGES=0", flush=True)
    print("PHASE171_R16_NEW_GIVEN=0", flush=True)
    print("PHASE171_R16_TRACKED_STATUS_UNCHANGED=PASS", flush=True)
    print("PHASE171_R16_REPORT=" + str(OUTPUT), flush=True)
    print("PHASE171_R16_RESULT=PASS_AUDIT_ONLY", flush=True)


if __name__ == "__main__":
    main()
```

## `tests/test_audit.py`

```python
"""Focused R16 tests: guards, reports and canonical-map diagnostic shapes."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

import pytest

from phase171_r2j_r4_r9_r16_hopf_route_audit import audit


def test_git_operations_are_read_only():
    with pytest.raises(ValueError):
        audit.git_read("reset", "--hard")
    with pytest.raises(ValueError):
        audit.git_read("add", "phase165_r52_r9_shared_math.py")


def test_reviewed_provider_and_head():
    data = audit.preflight()
    assert data["branch"] == "develop"
    assert len(data["head"]) == 40
    assert data["provider_blob"] == audit.REVIEWED_PROVIDER_BLOB


def test_r14_r15_report_link_is_checked():
    data = audit.read_prior_reports()
    assert data["r14_search"] == "partial"
    assert data["r15_no_derivation_goals"] == 16
    assert data["r15_classes"] == {"PROPOSALS_UNPROVED": 15, "NO_EXPANSION": 1}
    assert len(data["r14_sha256"]) == 64
    assert len(data["r15_sha256"]) == 64


def test_classification_has_no_success_from_available_routes():
    routes = [{"rule": "an inference route", "subgoals": ["unproved"]}]
    assert audit.observation_class(routes, "unresolved") == "ROUTES_EXIST_BUT_NOT_PROVED"
    assert audit.observation_class([], "unresolved") == "NO_PROVIDER_ROUTE"
    assert audit.observation_class(routes, "proved") == "INDEPENDENTLY_PROVED"


def test_false_suspension_isomorphism_is_not_connected():
    from homotopy_groups import TodaPrimaryGroup, TodaSuspensionIsomorphismStatement, TodaSuspensionMap
    from phase165_r52_r9_shared_math import shared_expansion_provider
    from phase171_r2i_eta_hopf_bridge.audit import _screened_context

    screened, group_root, _ = _screened_context()
    source = TodaPrimaryGroup(5, 2)
    target = TodaPrimaryGroup(6, 3)
    iso = TodaSuspensionIsomorphismStatement(TodaSuspensionMap(source, target))
    provider = shared_expansion_provider(screened, proof_target=group_root)
    assert provider(iso) == ()


def test_hopf_map_provider_exposes_real_obligations_only():
    from homotopy_groups import TodaHopfInvariantMap, TodaPrimaryGroup
    from phase165_r14_r6_generic_iso import MapSurjective
    from phase165_r52_r9_shared_math import shared_expansion_provider
    from phase171_r2i_eta_hopf_bridge.audit import _screened_context
    from phase165_r3_recursive_search import GoalExpansion

    screened, group_root, _ = _screened_context()
    provider = shared_expansion_provider(screened, proof_target=group_root)
    goal = MapSurjective(TodaHopfInvariantMap(
        TodaPrimaryGroup(7, 3), TodaPrimaryGroup(7, 5),
    ))
    proposals = provider(goal)
    assert isinstance(proposals, tuple)
    assert all(isinstance(item, GoalExpansion) for item in proposals)
    assert all(not hasattr(subgoal, "premises") for item in proposals for subgoal in item.subgoals)
```

## `run.ps1`

```powershell
param(
    [switch]$DryRun
)
$ErrorActionPreference = 'Stop'
$PackagePath = Split-Path -Parent $MyInvocation.MyCommand.Path
$Root = Split-Path -Parent $PackagePath
Push-Location $Root
try {
    $argsPy = @('-m', 'phase171_r2j_r4_r9_r16_hopf_route_audit.audit', '--dry-run')
    & python @argsPy
    if ($LASTEXITCODE -ne 0) { throw 'R16 preflight failed' }
    if ($DryRun) {
        Write-Output 'PHASE171_R16_DRY_RUN=PASS'
        exit 0
    }
    Write-Output 'PHASE171_R16_FOCUSED_PYTEST_START'
    & python -m pytest -q -p no:cacheprovider 'phase171_r2j_r4_r9_r16_hopf_route_audit/tests/test_audit.py'
    if ($LASTEXITCODE -ne 0) { throw 'R16 focused pytest failed' }
    Write-Output 'PHASE171_R16_FOCUSED_PYTEST=PASS'
    & python -m phase171_r2j_r4_r9_r16_hopf_route_audit.audit
    if ($LASTEXITCODE -ne 0) { throw 'R16 audit failed' }
    Write-Output 'PHASE171_R16_RESULT=PASS_READ_ONLY_HOPF_ROUTE_AUDIT'
}
finally {
    Pop-Location
}
```

## `__init__.py`

```python
"""Read-only R16 EHP independent-obligation audit."""
```

## `tests/__init__.py`

```python
"""R16 focused tests."""
```
