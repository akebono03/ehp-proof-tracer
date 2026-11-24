# R3R40R1 — 追加コード全文

既存コード変更なし。以下は新規ファイルの完全な内容。

## source.py

```python
"""Audit-only eta notation transport using independently proved old rules."""
from __future__ import annotations

from expression import Composition, HomotopyElement, Suspension
from homotopy_groups import TodaPrimaryGroup, TodaSuspensionMap
from phase165_r12_r20_eta_definition import TodaEtaFamilyGeneralDefinition
from phase165_r12_r28_presentation_connection import _matching_eta_name
from phase165_r14_r14_diagonal_and_prop42 import GeneratorSuspension
from phase165_r3_recursive_search import GoalExpansion
from phase171_r2i_eta_hopf_bridge.source import cited_eta_suspension_equality_rule
from phase174_r3_r7_r7_composite_zero_audit.rule import expression_endpoints
from phase176_r3r27r1_toda55_quadruple_isolated.source import expand_cited_quadruple
from phase176_r3r39_public_equality_transport.source import right_hopf_transport_backward_plan
from proof import Relation, RelationType
from relation_rules import (
    equality_preserved_under_left_composition_inference_rule,
    equality_preserved_under_right_composition_inference_rule,
    equality_symmetry_inference_rule,
    equality_transitivity_inference_rule,
)
from toda_rules import toda_eta_family_definition_statement


def eta_notation_backward_plan(
    left: object, right: object, available: tuple[object, ...],
) -> tuple[tuple[Relation, GoalExpansion], ...]:
    """Propose exact notation equalities, without identifying unequal objects.

    Each unequal leaf needs two inferred suspension equalities with the same
    canonical witness. Composition is handled by the old congruence rules.
    The empty result means no proof plan (or no change is needed).
    """
    if not isinstance(available, tuple):
        raise TypeError("available must be a tuple")
    if available.count(TodaEtaFamilyGeneralDefinition()) != 1:
        return ()
    if left == right:
        return ()
    stages: dict[Relation, GoalExpansion] = {}

    def add(lhs, rhs, rule, premises):
        target = Relation(lhs, rhs, RelationType.EQUALITY)
        old = stages.get(target)
        if old is not None:
            if old.rule.name != rule.name or old.subgoals != premises:
                raise ValueError("CONFLICTING_NOTATION_STAGE")
        else:
            stages[target] = GoalExpansion(rule, premises)
        return target

    def build(a, b):
        span = expression_endpoints(a)
        if span is None or span != expression_endpoints(b):
            return False
        if isinstance(a, HomotopyElement) and isinstance(b, HomotopyElement):
            n = a.target
            if type(n) is not int or n < 4:
                return False
            older = toda_eta_family_definition_statement(n - 1).element
            canonical = toda_eta_family_definition_statement(n).element
            if not (_matching_eta_name(a, canonical) and _matching_eta_name(b, canonical)):
                return False
            if a == b:
                return True
            witness = GeneratorSuspension(
                TodaSuspensionMap(TodaPrimaryGroup(n, n - 1), TodaPrimaryGroup(n + 1, n)),
                older, canonical,
            )
            suspended = Suspension(older)
            first = Relation(suspended, a)
            second = Relation(suspended, b)
            ea = add(suspended, a, cited_eta_suspension_equality_rule(first, witness), (witness,))
            eb = add(suspended, b, cited_eta_suspension_equality_rule(second, witness), (witness,))
            reverse = add(a, suspended, equality_symmetry_inference_rule(), (ea,))
            add(a, b, equality_transitivity_inference_rule(), (reverse, eb))
            return True
        if not isinstance(a, Composition) or not isinstance(b, Composition):
            return False
        if not build(a.left, b.left) or not build(a.right, b.right):
            return False
        if a == b:
            return True
        middle = Composition(b.left, a.right)
        parts = []
        if a.left != b.left:
            parts.append(add(a, middle,
                equality_preserved_under_right_composition_inference_rule(a.right),
                (Relation(a.left, b.left),)))
        if a.right != b.right:
            parts.append(add(middle, b,
                equality_preserved_under_left_composition_inference_rule(b.left),
                (Relation(a.right, b.right),)))
        if len(parts) == 2:
            add(a, b, equality_transitivity_inference_rule(), tuple(parts))
        return True

    if not build(left, right):
        return ()
    target = Relation(left, right)
    if target not in stages:
        return ()
    return tuple(stages.items())


def connection_backward_plan(
    transported: Relation, forward: Relation, available: tuple[object, ...],
) -> tuple[tuple[Relation, GoalExpansion], ...]:
    """Connect separately provable R3R39 and Toda (5.5) premises."""
    if not isinstance(available, tuple):
        raise TypeError("available must be a tuple")
    if len(right_hopf_transport_backward_plan(transported, available)) != 6:
        return ()
    if len(expand_cited_quadruple(forward, available)) != 1:
        return ()
    reverse = Relation(forward.rhs, forward.lhs)
    goal = Relation(transported.lhs, forward.lhs)
    stages = []
    if transported.rhs != forward.rhs:
        notation = eta_notation_backward_plan(transported.rhs, forward.rhs, available)
        if not notation:
            return ()
        stages.extend(notation)
        aligned = Relation(transported.lhs, forward.rhs)
        stages.append((aligned, GoalExpansion(equality_transitivity_inference_rule(),
                                             (transported, Relation(transported.rhs, forward.rhs)))))
    else:
        aligned = transported
    stages.append((reverse, GoalExpansion(equality_symmetry_inference_rule(), (forward,))))
    stages.append((goal, GoalExpansion(equality_transitivity_inference_rule(), (aligned, reverse))))
    if len({target for target, _ in stages}) != len(stages):
        raise ValueError("DUPLICATE_CONNECTION_STAGE")
    return tuple(stages)
```

## audit.py

```python
"""Read-only real shared-DFS audit with explicitly scoped notation proposals."""
from __future__ import annotations

import argparse
import ast
import json
import os
from pathlib import Path
import sys
import tempfile

PACKAGE = "phase176_r3r40r1_eta_notation_bridge"
ROOT = Path(__file__).resolve().parent.parent


def source_guard() -> None:
    from phase176_r3r40_toda55_connection_audit.audit import source_guard as prior_guard
    prior_guard()
    for filename in (
        "phase165_r12_r21_eta_generator_chain.py",
        "phase165_r12_r28_presentation_connection.py",
        "phase171_r2i_eta_hopf_bridge/source.py",
        "phase176_r3r40r1_eta_notation_bridge/source.py",
    ):
        ast.parse((ROOT / filename).read_text(encoding="utf-8-sig"), filename=filename)


def probe() -> dict:
    from expression import Composition, GeneratorSymbol, HomotopyElement, MapApplication
    from map_facts import EHP_H_MAP
    from phase165_r3_recursive_search import reconstruct_registered_goal
    from phase165_r52_r9_shared_math import build_shared_typed_bridge, shared_expansion_provider
    from phase165_r55_nk_only_goal import registered_group_goal_candidates
    from phase165_r57_r11_proof_order_gate import retain_ordered_root_expansions
    from phase169_r10e2_unpositioned_citation.source_first import screen_independent_sources_for_derived_goal
    from phase165_r12_r20_eta_definition import TodaEtaFamilyGeneralDefinition
    from phase165_r14_r14_diagonal_and_prop42 import GeneratorSuspension
    from phase171_r2h_prop22_cited_hopf.source import TodaProp22RightFormula
    from phase176_r3r27r1_toda55_quadruple_isolated.source import (
        RULE_NAME, Toda55UniversalQuadrupleStatement, canonical_quadruple_goal, quadruple_inputs,
    )
    from phase176_r3r39_public_equality_transport.source import right_hopf_transport_backward_plan
    from phase176_r3r40r1_eta_notation_bridge.source import connection_backward_plan, eta_notation_backward_plan
    from proof import ProofRule, Relation
    from unified_statement_registry import AssertionOrigin

    alpha = HomotopyElement("ν′", 3, 6, 3, GeneratorSymbol("ν", decoration="′"))
    eta5 = HomotopyElement("η₅", 5, 6, 5, GeneratorSymbol("η", index=5))
    eta6 = HomotopyElement("η₆", 6, 7, 6, GeneratorSymbol("η", index=6))
    eta7 = HomotopyElement("η₇", 7, 8, 7, GeneratorSymbol("η", index=7))
    gamma = Composition(eta6, eta7)
    transported = Relation(MapApplication(EHP_H_MAP, Composition(alpha, gamma)), Composition(eta5, gamma))
    forward = canonical_quadruple_goal(5)
    if forward is None:
        raise RuntimeError("CANONICAL_QUADRUPLE_MISSING")
    print("PHASE176_R3R40R1_TRANSPORT_CUBE_REPR=" + repr(transported.rhs))
    print("PHASE176_R3R40R1_TODA55_CUBE_REPR=" + repr(forward.rhs))
    goal = Relation(transported.lhs, forward.lhs)
    bridge = build_shared_typed_bridge()
    roots = registered_group_goal_candidates(bridge, n=3, k=5)
    if len(roots) != 1:
        raise RuntimeError("ROOT_NOT_UNIQUE")
    root = roots[0]
    screened = screen_independent_sources_for_derived_goal(bridge, goal=root)
    links = tuple(link for link in screened.proof_links
                  if link.step is not None and link.step.rule is ProofRule.GIVEN
                  and screened.registry.assertion(link.assertion_id).origin is AssertionOrigin.FIXED_STATEMENT
                  and screened.registry.assertion(link.assertion_id).content == link.step.conclusion)
    available = tuple(link.step.conclusion for link in links)
    sources = tuple(link for link in links if link.step.conclusion == Toda55UniversalQuadrupleStatement())
    if (len(sources) != 1 or available.count(TodaEtaFamilyGeneralDefinition()) != 1
            or available.count(TodaProp22RightFormula()) != 1):
        raise RuntimeError("SCREENED_SOURCES_MISSING_OR_AMBIGUOUS")
    notation = eta_notation_backward_plan(transported.rhs, forward.rhs, available)
    if transported.rhs != forward.rhs and not notation:
        raise RuntimeError("NO_TYPED_ETA_NOTATION_PLAN")
    plan = connection_backward_plan(transported, forward, available)
    transport_plan = right_hopf_transport_backward_plan(transported, available)
    if not plan or len(transport_plan) != 6:
        raise RuntimeError("CONNECTION_PLAN_MISSING")
    if any(item in available for item in (root, transported, forward, goal) + tuple(target for target, _ in plan)):
        raise RuntimeError("DERIVED_GOAL_PRESENT_AS_GIVEN")
    stages = dict(plan)
    default = shared_expansion_provider(screened, proof_target=root)

    def provider(target):
        # Prioritize only the explicit audit plan. All other obligations go to
        # the unmodified shared provider; no pre-completed proof is supplied.
        if isinstance(target, Relation) and target in stages:
            candidate = (stages[target],)
            if retain_ordered_root_expansions(root, target, candidate) != candidate:
                raise RuntimeError("ROOT_ORDER_GATE_REJECTED")
            return candidate + default(target)
        return default(target)

    events = []
    result = reconstruct_registered_goal(goal, screened, sources[0].assertion_id, provider,
        lookup_mode="typed_reference", progress_observer=lambda kind, target, step: events.append((kind, target)))
    visited = []

    def visit(step):
        if any(step is earlier for earlier in visited):
            return
        visited.append(step)
        for child in step.premises:
            visit(child)

    visit(result)
    if result.conclusion != goal or result.rule is not ProofRule.INFERENCE:
        raise RuntimeError("FINAL_GOAL_NOT_INFERRED")
    for target, expansion in tuple(transport_plan) + plan:
        if not any(step.conclusion == target and step.rule is ProofRule.INFERENCE
                   and step.inference_rule.name == expansion.rule.name
                   and tuple(child.conclusion for child in step.premises) == expansion.subgoals
                   for step in visited):
            raise RuntimeError("TREE_STAGE_MISSING:" + expansion.rule.name + ":" + repr(target))
    quad = next((step for step in visited if step.conclusion == forward), None)
    if (quad is None or quad.rule is not ProofRule.INFERENCE or quad.inference_rule.name != RULE_NAME
            or tuple(child.conclusion for child in quad.premises) != quadruple_inputs(forward)
            or quad.premises[0].rule is not ProofRule.INFERENCE
            or any(child.rule is not ProofRule.GIVEN for child in quad.premises[1:])):
        raise RuntimeError("TODA55_TREE_MISSING")
    witness_targets = tuple(dict.fromkeys(child for _, option in notation for child in option.subgoals
                                         if isinstance(child, GeneratorSuspension)))
    for witness in witness_targets:
        if not any(step.conclusion == witness and step.rule is ProofRule.INFERENCE for step in visited):
            raise RuntimeError("ETA_WITNESS_NOT_INFERRED")
    givens = tuple(step for step in visited if step.rule is ProofRule.GIVEN)
    if any(not any(step is link.step for link in links) for step in givens):
        raise RuntimeError("UNSCREENED_GIVEN")
    for required in (Toda55UniversalQuadrupleStatement(), TodaEtaFamilyGeneralDefinition(), TodaProp22RightFormula()):
        if not any(step.conclusion == required for step in givens):
            raise RuntimeError("CITED_ANCESTOR_MISSING:" + repr(required))
    if not any(kind == "proved" and target == goal for kind, target in events):
        raise RuntimeError("FINAL_DFS_EVENT_MISSING")
    generator = getattr(root.rhs, "generator", None)
    return {
        "gate": "PASS_R3R40R1_AUDIT_DFS_TYPED_ETA_NOTATION",
        "raw_eta_cube_equal": transported.rhs == forward.rhs,
        "notation_steps": len(notation),
        "independently_inferred_eta_witnesses": len(witness_targets),
        "notation_connection_proved": True,
        "r3r39_six_steps_preserved": True,
        "toda55_inferred_with_cited_ancestors": True,
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
        result = {"gate": "PASS_R3R40R1_DRYRUN", "full_pytest": "NOT_RUN"} if args.dry_run else probe()
    except Exception as error:
        result = {"gate": "FAIL_R3R40R1", "error": type(error).__name__ + ": " + str(error), "full_pytest": "NOT_RUN"}
    destination = Path(os.environ.get("LOCALAPPDATA") or tempfile.gettempdir()) / "EHPProofTracerAudit" / PACKAGE / "report.json"
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    for key, value in result.items():
        print("PHASE176_R3R40R1_" + key.upper() + "=" + str(value))
    print("REPORT=" + str(destination))
    print("(END)")
    return 0 if result["gate"].startswith("PASS_") else 1


if __name__ == "__main__":
    sys.exit(main())
```

## tests/test_notation.py

```python
"""Focused contracts for typed eta notation obligations, not proof fixtures."""
from __future__ import annotations

from dataclasses import replace

import pytest

from expression import Composition, GeneratorSymbol, HomotopyElement, MapApplication, Suspension
from map_facts import EHP_H_MAP
from phase165_r12_r20_eta_definition import TodaEtaFamilyGeneralDefinition
from phase165_r14_r14_diagonal_and_prop42 import GeneratorSuspension
from phase169_r10d2_general_family_definition.family_citation import CitedStableFamilyDefinition
from phase171_r2h_prop22_cited_hopf.source import TodaProp22RightFormula
from phase176_r3r27r1_toda55_quadruple_isolated.source import Toda55UniversalQuadrupleStatement, canonical_quadruple_goal
from phase176_r3r40r1_eta_notation_bridge.source import connection_backward_plan, eta_notation_backward_plan
from proof import ProofRule, ProofStep, Relation, apply_inference_match, find_inference_match
from toda_rules import toda_eta_family_definition_statement


def unicode_eta(n):
    canonical = toda_eta_family_definition_statement(n).element
    name = "η" + str(n).translate(str.maketrans("0123456789", "₀₁₂₃₄₅₆₇₈₉"))
    return replace(canonical, name=name)


def example():
    alpha = HomotopyElement("ν′", 3, 6, 3, GeneratorSymbol("ν", decoration="′"))
    e5, e6, e7 = (unicode_eta(n) for n in (5, 6, 7))
    gamma = Composition(e6, e7)
    forward = canonical_quadruple_goal(5)
    transport = Relation(MapApplication(EHP_H_MAP, Composition(alpha, gamma)), Composition(e5, gamma))
    available = (TodaEtaFamilyGeneralDefinition(), TodaProp22RightFormula(),
                 Toda55UniversalQuadrupleStatement(), CitedStableFamilyDefinition(4, 4, 3),
                 Relation(MapApplication(EHP_H_MAP, alpha), e5))
    return transport, forward, available


def test_real_canonical_spelling_differs_but_has_same_typed_symbol():
    observed = unicode_eta(5)
    canonical = toda_eta_family_definition_statement(5).element
    assert observed.name == "η₅" and canonical.name == "η_5"
    assert observed != canonical
    assert replace(observed, name=canonical.name) == canonical


@pytest.mark.parametrize("n", (5, 6, 7))
def test_leaf_requires_two_suspension_equalities_and_old_rules(n):
    a, b = unicode_eta(n), toda_eta_family_definition_statement(n).element
    plan = eta_notation_backward_plan(a, b, (TodaEtaFamilyGeneralDefinition(),))
    assert len(plan) == 4
    assert plan[-1][0] == Relation(a, b)
    assert [x.rule.name for _, x in plan] == [
        "proved consecutive eta suspension yields element equality",
        "proved consecutive eta suspension yields element equality",
        "equality symmetry", "equality transitivity",
    ]
    witness, = plan[0][1].subgoals
    assert isinstance(witness, GeneratorSuspension)
    assert plan[1][1].subgoals == (witness,)
    assert plan[0][0].lhs == Suspension(witness.source_generator)


def test_cube_plan_replays_existing_rules_with_synthetic_witnesses_only():
    transport, forward, available = example()
    plan = eta_notation_backward_plan(transport.rhs, forward.rhs, available)
    assert len(plan) == 18
    steps = {}
    for target, option in plan:
        for child in option.subgoals:
            if isinstance(child, GeneratorSuspension):
                # Synthetic witness is a unit-test fixture, never a production proof.
                steps.setdefault(child, ProofStep(child, (), ProofRule.INFERENCE))
        premises = tuple(steps[child] for child in option.subgoals)
        match = find_inference_match(option.rule, premises)
        assert match is not None
        result = apply_inference_match(match)
        assert result.conclusion == target and result.rule is ProofRule.INFERENCE
        assert result.premises == premises
        steps[target] = result
    assert Relation(transport.rhs, forward.rhs) in steps


def test_sources_and_type_checks_refuse_forgery():
    a, b = unicode_eta(5), toda_eta_family_definition_statement(5).element
    source = TodaEtaFamilyGeneralDefinition()
    assert eta_notation_backward_plan(a, b, ()) == ()
    assert eta_notation_backward_plan(a, b, (source, source)) == ()
    assert eta_notation_backward_plan(a, a, (source,)) == ()
    for forged in (replace(b, name="eta_5"), replace(b, source=99),
                   replace(b, generator=GeneratorSymbol("ν", index=5))):
        assert eta_notation_backward_plan(a, forged, (source,)) == ()
    with pytest.raises(TypeError):
        eta_notation_backward_plan(a, b, [source])


def test_connection_keeps_independent_obligations_and_final_old_rules():
    transport, forward, available = example()
    plan = connection_backward_plan(transport, forward, available)
    assert len(plan) == 21
    alias = Relation(transport.rhs, forward.rhs)
    aligned = Relation(transport.lhs, forward.rhs)
    reverse = Relation(forward.rhs, forward.lhs)
    final = Relation(transport.lhs, forward.lhs)
    assert plan[-3][0] == aligned and plan[-3][1].subgoals == (transport, alias)
    assert plan[-2][0] == reverse and plan[-2][1].subgoals == (forward,)
    assert plan[-1][0] == final and plan[-1][1].subgoals == (aligned, reverse)
    assert transport not in dict(plan) and forward not in dict(plan)
    for i in range(len(available)):
        assert connection_backward_plan(transport, forward, available[:i] + available[i+1:]) == ()


def test_notation_does_not_reassociate_composition():
    transport, forward, available = example()
    cube = forward.rhs
    reassociated = Composition(Composition(cube.left, cube.right.left), cube.right.right)
    assert eta_notation_backward_plan(transport.rhs, reassociated, available) == ()
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
    & python -B -m phase176_r3r40r1_eta_notation_bridge.audit @argsForAudit
    if ($LASTEXITCODE -ne 0) { throw 'R3R40R1 audit failed' }
    if (-not $DryRun) {
        & python -B -m pytest -q -p no:cacheprovider --import-mode=importlib `
            .\phase176_r3r40r1_eta_notation_bridge\tests\test_notation.py `
            .\phase176_r3r40_toda55_connection_audit\tests\test_connection.py `
            .\phase176_r3r27r1_toda55_quadruple_isolated\tests\test_source.py `
            .\phase176_r3r28_toda55_quadruple_public\tests\test_public.py `
            .\phase176_r3r39_public_equality_transport\tests\test_source.py
        if ($LASTEXITCODE -ne 0) { throw 'R3R40R1 focused pytest failed' }
        & git diff --check
        if ($LASTEXITCODE -ne 0) { throw 'R3R40R1 git diff check failed' }
        Write-Host 'PHASE176_R3R40R1_GATE=PASS_R3R40R1_TYPED_ETA_NOTATION_FOCUSED_TESTS'
        Write-Host 'PHASE176_R3R40R1_FULL_PYTEST=NOT_RUN'
        Write-Host '(END)'
    }
} finally {
    Pop-Location
}
```
