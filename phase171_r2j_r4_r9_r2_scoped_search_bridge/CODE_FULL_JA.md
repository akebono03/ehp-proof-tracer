# Phase 171 R2J-R4-R9-R2 — 新規コード・import・テスト全文

変更対象：新規フォルダのみ。既存のファイル・クラス・関数・import は変更しない。新規ファイルの配置位置はリポジトリ直下の `phase171_r2j_r4_r9_r2_scoped_search_bridge/` とその `tests/`。以下、各ファイルを省略なしで示す。

## `source.py`

```python
"""Scoped backward-search routes from R4-R8 inference rules, not completed steps.

This adapter is AUDIT_ONLY.  It never injects a previously inferred ProofStep
into search, never manufactures a GIVEN, and never alters shared production
providers.  Every expansion must be re-proved by the canonical search engine.
"""
from __future__ import annotations

from phase165_r3_recursive_search import GoalExpansion
from proof import ProofRule, ProofStep


def walk_proof_ancestry(root: ProofStep) -> tuple[ProofStep, ...]:
    """Visit each concrete proof node once; reject cycles and foreign rule kinds."""
    if not isinstance(root, ProofStep):
        raise TypeError("a real ProofStep root is required")
    visited: set[int] = set()
    active: set[int] = set()
    result: list[ProofStep] = []

    def visit(step: ProofStep) -> None:
        if not isinstance(step, ProofStep):
            raise TypeError("all premises must be ProofStep instances")
        identifier = id(step)
        if identifier in active:
            raise ValueError("cyclic proof dependency")
        if identifier in visited:
            return
        active.add(identifier)
        if step.rule is ProofRule.GIVEN:
            if step.premises:
                raise ValueError("GIVEN must be a leaf")
        elif step.rule is ProofRule.INFERENCE:
            if step.inference_rule is None or not step.premises:
                raise ValueError("inferred nodes require a rule and premises")
        else:
            raise ValueError("unverified ProofRule in ancestry")
        for parent in step.premises:
            visit(parent)
        active.remove(identifier)
        visited.add(identifier)
        result.append(step)

    visit(root)
    return tuple(result)


def inference_expansion_catalog(root: ProofStep) -> tuple[tuple[object, GoalExpansion], ...]:
    """Extract *only* rules and subgoal statements, never prior ProofSteps.

    Duplicate conclusions with different derivations are refused: silently
    selecting an arbitrary proof route would break the ambiguity boundary.
    """
    rows: list[tuple[object, GoalExpansion]] = []
    for step in walk_proof_ancestry(root):
        if step.rule is not ProofRule.INFERENCE:
            continue
        proposal = GoalExpansion(
            step.inference_rule,
            tuple(parent.conclusion for parent in step.premises),
        )
        earlier = [old for conclusion, old in rows
                   if type(conclusion) is type(step.conclusion)
                   and conclusion == step.conclusion]
        if earlier:
            if (len(earlier) != 1
                    or earlier[0].rule.name != proposal.rule.name
                    or earlier[0].subgoals != proposal.subgoals):
                raise ValueError("ambiguous inferred route for one typed goal")
            continue
        rows.append((step.conclusion, proposal))
    return tuple(rows)


def scoped_expansion_provider(
    root: ProofStep, fallback_provider,
):
    """Prioritize inferred R4-R8 obligations and retain ordinary fallback.

    This is a local experiment, NOT registration in the public provider.
    """
    if not callable(fallback_provider):
        raise TypeError("fallback_provider must be callable")
    catalog = inference_expansion_catalog(root)
    if not catalog or catalog[-1][0] != root.conclusion:
        raise ValueError("the root must be the last inferred goal")

    def expand(goal: object) -> tuple[GoalExpansion, ...]:
        matches = tuple(route for conclusion, route in catalog
                        if type(conclusion) is type(goal) and conclusion == goal)
        if matches:
            if len(matches) != 1:
                raise ValueError("ambiguous scoped goal")
            return matches
        ordinary = fallback_provider(goal)
        if not isinstance(ordinary, tuple) or not all(
            isinstance(item, GoalExpansion) for item in ordinary
        ):
            raise TypeError("fallback provider returned invalid proposals")
        return ordinary

    return expand
```

## `audit.py`

```python
"""Phase 171 R2J-R4-R9-R2: scoped canonical search, no production changes.

R4-R8 supplies a validated *rule graph*; every conclusion is re-derived by the
normal registered-goal engine from publication-screened sources.  Completion
and trust-boundary acceptance are reported separately and never fabricated.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import subprocess

from phase165_r52_partial_proof import ProofSearchStatus
from phase165_r52_r2_search_adapter import search_registered_partial_proof
from phase165_r52_r9_shared_math import shared_expansion_provider
from phase168_r3_41p13_trust_boundary import (
    UnverifiedProofTree,
    verify_proof_tree_for_narrative,
)
from phase171_r2i_eta_hopf_bridge.audit import _screened_context
from phase171_r2j_r4_r8_cyclic_structure.audit import build_cyclic_pi63_proof
from phase171_r2j_r4_r9_r2_scoped_search_bridge.source import (
    inference_expansion_catalog,
    scoped_expansion_provider,
    walk_proof_ancestry,
)
from proof import ProofRule

ROOT = Path(__file__).resolve().parent.parent
OUTPUT = Path(__file__).resolve().parent / "output"


def _git(*arguments: str) -> str:
    allowed = {
        ("branch", "--show-current"),
        ("rev-parse", "HEAD"),
        ("status", "--porcelain", "--untracked-files=no"),
    }
    if arguments not in allowed:
        raise ValueError("only read-only Git commands are permitted")
    return subprocess.run(
        ["git", *arguments], cwd=ROOT,
        capture_output=True, text=True, check=True,
    ).stdout.strip()


def replay_scoped_search() -> dict:
    screened, target, citing_id = _screened_context()
    root, _, r8_report = build_cyclic_pi63_proof()
    if (root.conclusion != target or root.rule is not ProofRule.INFERENCE
            or r8_report["new_given_added"] != 0):
        raise RuntimeError("R4-R8 did not prove the positioned registered goal")

    catalog = inference_expansion_catalog(root)
    ordinary = shared_expansion_provider(screened, proof_target=target)
    scoped = scoped_expansion_provider(root, ordinary)
    root_proposals = scoped(target)
    if (len(root_proposals) != 1
            or root_proposals[0].subgoals != tuple(
                parent.conclusion for parent in root.premises
            )):
        raise RuntimeError("scoped route does not match the R4-R8 root")

    result = search_registered_partial_proof(
        n=3, k=3, goal=target, bridge=screened,
        citing_assertion_id=citing_id,
        expansion_provider=scoped,
        lookup_mode="typed_reference_publication",
    )
    complete = (result.status is ProofSearchStatus.COMPLETE
                and result.conclusion == target and not result.open_goals)
    verified = False
    verification_result = None
    if complete:
        try:
            verification_result = verify_proof_tree_for_narrative(
                result, screened, citing_assertion_id=citing_id,
            )
            verified = True
        except UnverifiedProofTree as error:
            verification_result = str(error)
    original_nodes = walk_proof_ancestry(root)
    if not original_nodes or len(catalog) < 2:
        raise RuntimeError("original inferred proof graph disappeared")
    # A limited-phase audit cannot confer a public COMPLETE status.  This
    # report never substitutes its scoped result into Web or production.
    return {
        "phase": "171-R2J-R4-R9-R2",
        "mode": "AUDIT_ONLY_SCOPED_CANONICAL_SEARCH",
        "target": repr(target),
        "citing_assertion_id": citing_id,
        "r8_inferred": True,
        "r8_rule_catalog_size": len(catalog),
        "r8_given_leaves": sum(node.rule is ProofRule.GIVEN for node in original_nodes),
        "scoped_root_options": len(root_proposals),
        "scoped_search_status": result.status.value,
        "scoped_search_complete": complete,
        "scoped_search_proven_steps": len(result.proven_steps),
        "scoped_open_goals": [repr(item)[:600] for item in result.open_goals[:20]],
        "scoped_diagnostics": list(result.diagnostics[:20]),
        "trust_boundary_accepted": verified,
        "trust_boundary_result": verification_result,
        "public_provider_modified": False,
        "public_web_verified": False,
        "new_given_added": 0,
        "full_pytest": False,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    branch = _git("branch", "--show-current")
    head = _git("rev-parse", "HEAD")
    before = _git("status", "--porcelain", "--untracked-files=no")
    if branch != "develop":
        raise RuntimeError("R9-R2 requires develop")
    for required in (
        "phase171_r2j_r4_r8_cyclic_structure/audit.py",
        "phase171_r2j_r4_r7_nonzero_nu_order/audit.py",
    ):
        if not (ROOT / required).is_file():
            raise RuntimeError("missing R4 prerequisite: " + required)
    print("PHASE171_R2J_R4_R9_R2_BRANCH=" + branch, flush=True)
    print("PHASE171_R2J_R4_R9_R2_HEAD=" + head, flush=True)
    if args.dry_run:
        print("PHASE171_R2J_R4_R9_R2_RESULT=PASS_DRY_RUN", flush=True)
        return
    report = replay_scoped_search()
    if _git("status", "--porcelain", "--untracked-files=no") != before:
        raise RuntimeError("tracked working tree changed during audit")
    report.update({"git_head": head, "tracked_status_unchanged": True})
    OUTPUT.mkdir(parents=True, exist_ok=True)
    destination = OUTPUT / "audit.json"
    destination.write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8",
    )
    print("PHASE171_R2J_R4_R9_R2_RULE_CATALOG=" + str(report["r8_rule_catalog_size"]), flush=True)
    print("PHASE171_R2J_R4_R9_R2_SCOPED_SEARCH=" + report["scoped_search_status"], flush=True)
    print("PHASE171_R2J_R4_R9_R2_TRUST_VERIFIED=" + str(report["trust_boundary_accepted"]), flush=True)
    print("PHASE171_R2J_R4_R9_R2_NEW_GIVEN=0", flush=True)
    print("PHASE171_R2J_R4_R9_R2_PUBLIC_WEB_VERIFIED=False", flush=True)
    print("PHASE171_R2J_R4_R9_R2_TRACKED_STATUS_UNCHANGED=PASS", flush=True)
    print("PHASE171_R2J_R4_R9_R2_REPORT=" + str(destination), flush=True)
    print("PHASE171_R2J_R4_R9_R2_RESULT=PASS_AUDIT_ONLY", flush=True)


if __name__ == "__main__":
    main()
```

## `tests/test_audit.py`

```python
"""Focused, fail-closed checks of scoped rule-only public-path experiment."""
from __future__ import annotations

from dataclasses import replace

import pytest

from phase165_r3_recursive_search import GoalExpansion
from phase171_r2j_r4_r9_r2_scoped_search_bridge.audit import _git
from phase171_r2j_r4_r9_r2_scoped_search_bridge.source import (
    inference_expansion_catalog,
    scoped_expansion_provider,
    walk_proof_ancestry,
)
from proof import InferenceRule, ProofRule, ProofStep


def _fixture():
    cited = ProofStep("earlier-cited", (), ProofRule.GIVEN)
    rule = InferenceRule(name="typed inference")
    root = ProofStep("derived", (cited,), ProofRule.INFERENCE, inference_rule=rule)
    return cited, root


def test_catalog_extracts_only_subgoals_not_prior_proofsteps():
    cited, root = _fixture()
    assert walk_proof_ancestry(root) == (cited, root)
    catalog = inference_expansion_catalog(root)
    assert len(catalog) == 1
    assert catalog[0][0] == "derived"
    assert catalog[0][1].subgoals == ("earlier-cited",)
    assert all(not isinstance(item, ProofStep) for item in catalog[0][1].subgoals)


def test_scoped_provider_prioritizes_exact_rule_and_delegates_other_goals():
    _, root = _fixture()
    fallback = lambda goal: (GoalExpansion(InferenceRule(name="fallback"), (goal,)),)
    provider = scoped_expansion_provider(root, fallback)
    assert provider("derived") == (GoalExpansion(root.inference_rule, ("earlier-cited",)),)
    assert provider("other") == fallback("other")


def test_rejects_fake_given_and_noninference_premise():
    cited, root = _fixture()
    with pytest.raises(ValueError, match="GIVEN"):
        walk_proof_ancestry(replace(cited, premises=(root,)))
    with pytest.raises(ValueError, match="inferred"):
        walk_proof_ancestry(replace(root, inference_rule=None))
    with pytest.raises(ValueError, match="unverified"):
        walk_proof_ancestry(ProofStep("foreign", (), ProofRule.RELATION))


def test_duplicate_conclusion_with_two_incompatible_rules_fails_closed():
    cited, root = _fixture()
    other = ProofStep("derived", (cited,), ProofRule.INFERENCE,
                      inference_rule=InferenceRule(name="different"))
    final = ProofStep("final", (root, other), ProofRule.INFERENCE,
                      inference_rule=InferenceRule(name="combine"))
    with pytest.raises(ValueError, match="ambiguous"):
        inference_expansion_catalog(final)


def test_cyclic_proof_is_rejected():
    cited, root = _fixture()
    object.__setattr__(root, "premises", (root,))
    with pytest.raises(ValueError, match="cyclic"):
        walk_proof_ancestry(root)


def test_invalid_fallback_provider_fails_closed():
    _, root = _fixture()
    with pytest.raises(TypeError):
        scoped_expansion_provider(root, object())
    provider = scoped_expansion_provider(root, lambda goal: ["invalid"])
    with pytest.raises(TypeError):
        provider("other")


def test_readonly_git_guard():
    with pytest.raises(ValueError):
        _git("reset", "--hard")
```

## `tests/test_live_scoped.py`

```python
"""Real-source scoped canonical backward search; its result may remain incomplete."""
from __future__ import annotations

from phase171_r2j_r4_r9_r2_scoped_search_bridge.audit import replay_scoped_search


def test_scoped_audit_is_readonly_and_never_claims_public_completion():
    report = replay_scoped_search()
    assert report["r8_inferred"] is True
    assert report["r8_rule_catalog_size"] >= 2
    assert report["scoped_root_options"] == 1
    assert report["new_given_added"] == 0
    assert report["public_provider_modified"] is False
    assert report["public_web_verified"] is False
    assert report["scoped_search_status"] in (
        "complete", "partial", "search_failed",
    )
    if report["trust_boundary_accepted"]:
        assert report["scoped_search_complete"] is True
```

## `run.ps1`

```powershell
param([switch]$DryRun)
$ErrorActionPreference = 'Stop'
$Package = $PSScriptRoot
$Repo = (Resolve-Path (Join-Path $Package '..')).Path
Push-Location $Repo
try {
    if (-not (Test-Path '.git')) { throw 'Run R9-R2 at the Git repository root.' }
    python -B -m phase171_r2j_r4_r9_r2_scoped_search_bridge.audit --dry-run
    if ($LASTEXITCODE -ne 0) { throw 'R9-R2 preflight failed' }
    if ($DryRun) {
        Write-Host 'PHASE171_R2J_R4_R9_R2_RESULT=PASS_DRY_RUN'
        return
    }
    python -B -m pytest -q -p no:cacheprovider `
        '.\phase171_r2j_r4_r9_r2_scoped_search_bridge\tests\test_audit.py' `
        '.\phase171_r2j_r4_r9_r2_scoped_search_bridge\tests\test_live_scoped.py'
    if ($LASTEXITCODE -ne 0) { throw 'R9-R2 focused pytest failed' }
    Write-Host 'PHASE171_R2J_R4_R9_R2_FOCUSED_PYTEST=PASS'
    python -B -m phase171_r2j_r4_r9_r2_scoped_search_bridge.audit
    if ($LASTEXITCODE -ne 0) { throw 'R9-R2 scoped canonical search failed' }
} finally {
    Pop-Location
}
```

## `__init__.py`

```python
"""R2J-R4-R9-R2 audit-only route experiment."""
```

## `tests/__init__.py`

```python
"""Focused tests for R9-R2."""
```

