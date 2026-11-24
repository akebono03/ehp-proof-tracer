# R3R40 — 追加コード全文

すべて新規ファイル。既存ファイルの変更なし。

## source.py

```python
"""Audit-only backward connection using existing equality rules."""
from __future__ import annotations

from collections.abc import Callable

from expression import HomotopyElement, Multiple
from phase165_r3_recursive_search import GoalExpansion
from phase176_r3r27r1_toda55_quadruple_isolated.source import (
    canonical_quadruple_goal,
    expand_cited_quadruple,
)
from phase176_r3r39_public_equality_transport.source import (
    right_hopf_transport_backward_plan,
)
from proof import Relation, RelationType
from relation_rules import (
    equality_symmetry_inference_rule,
    equality_transitivity_inference_rule,
)


def quadruple_hopf_backward_plan(
    goal: object, available: tuple[object, ...],
) -> tuple[tuple[Relation, GoalExpansion], ...]:
    """Require a source-eligible canonical quadruple and typed Hopf transport.

    The two independent statements are open DFS obligations. No name-based
    rewriting, reassociation, direct GIVEN, or new inference rule is used.
    """
    if not isinstance(available, tuple):
        raise TypeError("available must be a tuple")
    if (not isinstance(goal, Relation)
            or goal.relation_type is not RelationType.EQUALITY
            or not isinstance(goal.rhs, Multiple)
            or type(goal.rhs.coefficient) is not int
            or goal.rhs.coefficient != 4
            or not isinstance(goal.rhs.expression, HomotopyElement)):
        return ()
    forward = canonical_quadruple_goal(goal.rhs.expression.dimension)
    if forward is None or forward.lhs != goal.rhs:
        return ()
    if len(expand_cited_quadruple(forward, available)) != 1:
        return ()
    transported = Relation(goal.lhs, forward.rhs, RelationType.EQUALITY)
    if len(right_hopf_transport_backward_plan(transported, available)) != 6:
        return ()
    reversed_quadruple = Relation(forward.rhs, forward.lhs, RelationType.EQUALITY)
    return (
        (reversed_quadruple, GoalExpansion(
            equality_symmetry_inference_rule(), (forward,),
        )),
        (goal, GoalExpansion(
            equality_transitivity_inference_rule(),
            (transported, reversed_quadruple),
        )),
    )


def build_audit_connection_provider(
    goal: Relation, available: tuple[object, ...],
) -> Callable[[object], tuple[GoalExpansion, ...]]:
    """Install exactly the two open expansions in an explicit audit context."""
    plan = quadruple_hopf_backward_plan(goal, available)

    def expand(target: object) -> tuple[GoalExpansion, ...]:
        return tuple(proposal for statement, proposal in plan
                     if isinstance(target, Relation) and target == statement)

    return expand
```

## audit.py

```python
"""Audit the Toda (5.5) connection using the canonical recursive DFS."""
from __future__ import annotations

import argparse
import ast
import json
import os
from pathlib import Path
import sys
import tempfile

PACKAGE = "phase176_r3r40_toda55_connection_audit"
ROOT = Path(__file__).resolve().parent.parent


def source_guard() -> None:
    required = (
        "phase165_r52_r9_shared_math.py",
        "phase176_r3r27r1_toda55_quadruple_isolated/source.py",
        "phase176_r3r39_public_equality_transport/source.py",
        "phase165_r3_recursive_search.py",
        "relation_rules.py",
    )
    for filename in required:
        path = ROOT / filename
        ast.parse(path.read_text(encoding="utf-8-sig"), filename=filename)
    shared = (ROOT / required[0]).read_text(encoding="utf-8-sig")
    anchors = (
        "options.extend(public_right_hopf_transport(goal))",
        "return expand_cited_quadruple(goal, tuple(available))",
        "build_cited_toda55_quadruple_source(),",
    )
    if any(shared.count(anchor) != 1 for anchor in anchors):
        raise ValueError("EXISTING_PUBLIC_HOOKS_REQUIRED")


def probe() -> dict:
    from expression import Composition, GeneratorSymbol, HomotopyElement, MapApplication
    from map_facts import EHP_H_MAP
    from phase165_r3_recursive_search import reconstruct_registered_goal
    from phase165_r52_r9_shared_math import build_shared_typed_bridge, shared_expansion_provider
    from phase165_r55_nk_only_goal import registered_group_goal_candidates
    from phase165_r57_r11_proof_order_gate import retain_ordered_root_expansions
    from phase169_r10e2_unpositioned_citation.source_first import (
        screen_independent_sources_for_derived_goal,
    )
    from phase171_r2h_prop22_cited_hopf.source import TodaProp22RightFormula
    from phase176_r3r27r1_toda55_quadruple_isolated.source import (
        RULE_NAME, Toda55UniversalQuadrupleStatement, canonical_quadruple_goal,
        quadruple_inputs,
    )
    from phase176_r3r39_public_equality_transport.source import right_hopf_transport_backward_plan
    from phase176_r3r40_toda55_connection_audit.source import (
        build_audit_connection_provider, quadruple_hopf_backward_plan,
    )
    from proof import ProofRule, Relation, RelationType
    from unified_statement_registry import AssertionOrigin

    alpha = HomotopyElement("ν′", 3, 6, 3, GeneratorSymbol("ν", decoration="′"))
    eta5 = HomotopyElement("η₅", 5, 6, 5, GeneratorSymbol("η", index=5))
    eta6 = HomotopyElement("η₆", 6, 7, 6, GeneratorSymbol("η", index=6))
    eta7 = HomotopyElement("η₇", 7, 8, 7, GeneratorSymbol("η", index=7))
    gamma = Composition(eta6, eta7)
    transported = Relation(MapApplication(EHP_H_MAP, Composition(alpha, gamma)),
                           Composition(eta5, gamma), RelationType.EQUALITY)
    forward = canonical_quadruple_goal(5)
    if forward is None or forward.rhs != transported.rhs:
        raise RuntimeError("TYPED_ETA_CUBE_MISMATCH")
    goal = Relation(transported.lhs, forward.lhs, RelationType.EQUALITY)

    bridge = build_shared_typed_bridge()
    roots = registered_group_goal_candidates(bridge, n=3, k=5)
    if len(roots) != 1:
        raise RuntimeError("ROOT_NOT_UNIQUE")
    root = roots[0]
    screened = screen_independent_sources_for_derived_goal(bridge, goal=root)
    links = tuple(link for link in screened.proof_links
                  if link.step is not None and link.step.rule is ProofRule.GIVEN
                  and screened.registry.assertion(link.assertion_id).origin
                  is AssertionOrigin.FIXED_STATEMENT
                  and screened.registry.assertion(link.assertion_id).content
                  == link.step.conclusion)
    available = tuple(link.step.conclusion for link in links)
    source_links = tuple(link for link in links
                         if link.step.conclusion == Toda55UniversalQuadrupleStatement())
    if len(source_links) != 1 or available.count(TodaProp22RightFormula()) != 1:
        raise RuntimeError("SOURCE_SCREENING_FAILED")
    if any(item in available for item in (root, goal, transported, forward)):
        raise RuntimeError("DERIVED_CONCLUSION_PRESENT_AS_GIVEN")
    context_id = source_links[0].assertion_id
    plan = quadruple_hopf_backward_plan(goal, available)
    if len(plan) != 2 or plan[1][1].subgoals[0] != transported:
        raise RuntimeError("TWO_STAGE_PLAN_MISSING")
    local = build_audit_connection_provider(goal, available)
    provider = shared_expansion_provider(screened, extra_providers=(local,), proof_target=root)
    for target, proposal in plan:
        if retain_ordered_root_expansions(root, target, (proposal,)) != (proposal,):
            raise RuntimeError("ROOT_ORDER_GATE_REJECTED")
        if not any(option.rule.name == proposal.rule.name and option.subgoals == proposal.subgoals
                   for option in provider(target)):
            raise RuntimeError("LOCAL_EXPANSION_NOT_REACHABLE")
    events = []
    result = reconstruct_registered_goal(
        goal, screened, context_id, provider, lookup_mode="typed_reference",
        progress_observer=lambda kind, target, step: events.append((kind, target)),
    )
    if (result.rule is not ProofRule.INFERENCE or result.conclusion != goal
            or result.inference_rule.name != "equality transitivity"
            or tuple(step.conclusion for step in result.premises) != plan[1][1].subgoals):
        raise RuntimeError("FINAL_TRANSITIVITY_TREE_MISMATCH")
    hopf, reverse = result.premises
    if (reverse.rule is not ProofRule.INFERENCE
            or reverse.inference_rule.name != "equality symmetry"
            or len(reverse.premises) != 1):
        raise RuntimeError("SYMMETRY_TREE_MISMATCH")
    quad = reverse.premises[0]
    if (quad.rule is not ProofRule.INFERENCE or quad.conclusion != forward
            or quad.inference_rule.name != RULE_NAME
            or tuple(step.conclusion for step in quad.premises) != quadruple_inputs(forward)):
        raise RuntimeError("TODA55_PROOF_TREE_MISMATCH")
    if (quad.premises[0].rule is not ProofRule.INFERENCE
            or any(step.rule is not ProofRule.GIVEN for step in quad.premises[1:])):
        raise RuntimeError("TODA55_PREMISE_PROVENANCE_MISMATCH")
    visited = []

    def visit(step):
        if any(step is old for old in visited):
            return
        visited.append(step)
        for child in step.premises:
            visit(child)

    visit(hopf)
    transport_plan = right_hopf_transport_backward_plan(transported, available)
    if len(transport_plan) != 6:
        raise RuntimeError("R3R39_PLAN_MISSING")
    for target, proposal in transport_plan:
        if not any(step.conclusion == target and step.rule is ProofRule.INFERENCE
                   and step.inference_rule.name == proposal.rule.name
                   and tuple(child.conclusion for child in step.premises) == proposal.subgoals
                   for step in visited):
            raise RuntimeError("R3R39_TREE_NOT_PRESERVED")
    visit(result)
    given_steps = tuple(step for step in visited if step.rule is ProofRule.GIVEN)
    if any(not any(step is link.step for link in links) for step in given_steps):
        raise RuntimeError("UNSCREENED_GIVEN_IN_TREE")
    if not any(step.conclusion == TodaProp22RightFormula() for step in given_steps):
        raise RuntimeError("PROP22_MISSING_IN_TREE")
    if not any(step.conclusion == Toda55UniversalQuadrupleStatement() for step in given_steps):
        raise RuntimeError("TODA55_MISSING_IN_TREE")
    if not any(kind == "proved" and target == goal for kind, target in events):
        raise RuntimeError("DFS_FINAL_EVENT_MISSING")
    generator = getattr(root.rhs, "generator", None)
    return {
        "gate": "PASS_R3R40_TODA55_AUDIT_DFS_EXISTING_RULES",
        "typed_eta_cube_exact_match": True,
        "associativity_required": False,
        "cited_toda55_count": len(source_links),
        "r3r39_six_steps_preserved": True,
        "existing_connection_rules": ["equality symmetry", "equality transitivity"],
        "audit_dfs_hopf_quadruple_proved": True,
        "registered_generator_matches_audit_expression": generator == goal.lhs.expression,
        "registered_generator_repr": repr(generator),
        "shared_default_provider_modified": False,
        "root_group_proved": False,
        "new_given": 0,
        "new_math_rules": 0,
        "full_pytest": "NOT_RUN",
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    try:
        source_guard()
        result = ({"gate": "PASS_R3R40_DRYRUN", "full_pytest": "NOT_RUN"}
                  if args.dry_run else probe())
    except Exception as error:
        result = {"gate": "FAIL_R3R40", "error": type(error).__name__ + ": " + str(error),
                  "full_pytest": "NOT_RUN"}
    destination = (Path(os.environ.get("LOCALAPPDATA") or tempfile.gettempdir())
                   / "EHPProofTracerAudit" / PACKAGE / "report.json")
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    for key, value in result.items():
        print("PHASE176_R3R40_" + key.upper() + "=" + str(value))
    print("REPORT=" + str(destination))
    print("(END)")
    return 0 if result["gate"].startswith("PASS_") else 1


if __name__ == "__main__":
    sys.exit(main())
```

## tests/test_connection.py

```python
"""Focused tests: candidate construction only, no synthetic proof certificates."""
from __future__ import annotations

from dataclasses import replace

import pytest

from expression import Composition, GeneratorSymbol, HomotopyElement, MapApplication, Multiple
from map_facts import EHP_H_MAP
from phase165_r12_r20_eta_definition import TodaEtaFamilyGeneralDefinition
from phase169_r10d2_general_family_definition.family_citation import CitedStableFamilyDefinition
from phase171_r2h_prop22_cited_hopf.source import TodaProp22RightFormula
from phase176_r3r27r1_toda55_quadruple_isolated.source import (
    Toda55UniversalQuadrupleStatement, canonical_quadruple_goal,
)
from phase176_r3r40_toda55_connection_audit.source import (
    build_audit_connection_provider, quadruple_hopf_backward_plan,
)
from proof import Relation, RelationType


def example(n=5):
    forward = canonical_quadruple_goal(n)
    # The real R3R39 case has n=5; n=7 tests the structural generalization.
    sphere = (n + 1) // 2
    alpha = HomotopyElement("formal-alpha", sphere, n + 1, sphere)
    if n == 5:
        alpha = HomotopyElement("ν′", 3, 6, 3, GeneratorSymbol("ν", decoration="′"))
    cube = forward.rhs
    hopf = Relation(MapApplication(EHP_H_MAP, alpha), cube.left)
    goal = Relation(MapApplication(EHP_H_MAP, Composition(alpha, cube.right)), forward.lhs)
    sources = (Toda55UniversalQuadrupleStatement(), CitedStableFamilyDefinition(4, 4, 3),
               TodaEtaFamilyGeneralDefinition(), TodaProp22RightFormula(), hopf)
    return goal, forward, sources


@pytest.mark.parametrize("n", (5, 7))
def test_two_old_rules_and_exact_open_obligations(n):
    goal, forward, sources = example(n)
    plan = quadruple_hopf_backward_plan(goal, sources)
    reverse = Relation(forward.rhs, forward.lhs)
    transport = Relation(goal.lhs, forward.rhs)
    assert len(plan) == 2
    assert plan[0][0] == reverse
    assert plan[0][1].rule.name == "equality symmetry"
    assert plan[0][1].subgoals == (forward,)
    assert plan[1][0] == goal
    assert plan[1][1].rule.name == "equality transitivity"
    assert plan[1][1].subgoals == (transport, reverse)


def test_each_source_is_required_and_ambiguity_rejected():
    goal, _, sources = example()
    for i, source in enumerate(sources):
        assert quadruple_hopf_backward_plan(goal, sources[:i] + sources[i+1:]) == ()
        assert quadruple_hopf_backward_plan(goal, sources + (source,)) == ()
    with pytest.raises(TypeError):
        quadruple_hopf_backward_plan(goal, list(sources))


def test_rejects_wrong_coefficient_and_map_and_untyped_goal():
    goal, forward, sources = example()
    assert quadruple_hopf_backward_plan(replace(goal, rhs=Multiple(2, forward.lhs.expression)), sources) == ()
    assert quadruple_hopf_backward_plan(replace(goal, lhs=forward.rhs), sources) == ()
    assert quadruple_hopf_backward_plan(replace(goal, relation_type=RelationType.ZERO), sources) == ()
    assert quadruple_hopf_backward_plan("untyped", sources) == ()


def test_rejects_different_rhs_generator_and_right_factor():
    goal, forward, sources = example()
    wrong_nu = replace(forward.lhs.expression, name="different")
    assert quadruple_hopf_backward_plan(replace(goal, rhs=Multiple(4, wrong_nu)), sources) == ()
    product = goal.lhs.expression
    changed = Composition(product.right.left, replace(product.right.right, name="different"))
    wrong_goal = replace(goal, lhs=MapApplication(EHP_H_MAP, Composition(product.left, changed)))
    assert quadruple_hopf_backward_plan(wrong_goal, sources) == ()


def test_local_provider_does_not_claim_independent_inputs():
    goal, forward, sources = example()
    plan = quadruple_hopf_backward_plan(goal, sources)
    provider = build_audit_connection_provider(goal, sources)
    for target, expansion in plan:
        options = provider(target)
        assert len(options) == 1
        assert options[0].rule.name == expansion.rule.name
        assert options[0].subgoals == expansion.subgoals
    assert provider(forward) == ()
    assert provider(plan[1][1].subgoals[0]) == ()
    assert provider("unrelated") == ()
```

## run.ps1

```powershell
param([switch]$DryRun)
$ErrorActionPreference = 'Stop'
$root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Push-Location $root
try {
    $argsForAudit = @()
    if ($DryRun) { $argsForAudit += '--dry-run' }
    & python -B -m phase176_r3r40_toda55_connection_audit.audit @argsForAudit
    if ($LASTEXITCODE -ne 0) { throw 'R3R40 audit failed' }
    if (-not $DryRun) {
        & python -B -m pytest -q -p no:cacheprovider --import-mode=importlib `
            .\phase176_r3r40_toda55_connection_audit\tests\test_connection.py `
            .\phase176_r3r27r1_toda55_quadruple_isolated\tests\test_source.py `
            .\phase176_r3r28_toda55_quadruple_public\tests\test_public.py `
            .\phase176_r3r39_public_equality_transport\tests\test_source.py
        if ($LASTEXITCODE -ne 0) { throw 'R3R40 focused pytest failed' }
        & git diff --check
        if ($LASTEXITCODE -ne 0) { throw 'R3R40 git diff check failed' }
        Write-Host 'PHASE176_R3R40_GATE=PASS_R3R40_TODA55_CONNECTION_FOCUSED_TESTS'
        Write-Host 'PHASE176_R3R40_FULL_PYTEST=NOT_RUN'
        Write-Host '(END)'
    }
} finally {
    Pop-Location
}
```

