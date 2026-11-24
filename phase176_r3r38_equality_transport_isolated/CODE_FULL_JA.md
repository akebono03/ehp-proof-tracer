# Phase 176 R3R38 — 追加コード全文

既存コードの変更なし。新規ディレクトリをプロジェクトルート直下に追加する。新規関数はそれぞれ対応する新規ファイル内に配置。import を含む全文を以下に示す。

## source.py

```python
"""Replay typed right-Hopf equality transport using existing general rules.

This isolated helper neither registers a new inference rule nor modifies a
shared provider.  Both input steps must already be independent inferences.
"""
from __future__ import annotations

from expression import Composition, HomotopyElement, MapApplication, Suspension
from hopf_rules import ehp_h_preserves_equality_inference_rule
from map_facts import EHP_H_MAP
from phase174_r3_r7_r7_composite_zero_audit.rule import expression_endpoints
from proof import (
    ProofRule,
    ProofStep,
    Relation,
    RelationType,
    apply_inference_match,
    find_inference_matches_for_rule,
)
from relation_rules import (
    equality_preserved_under_left_composition_inference_rule,
    equality_symmetry_inference_rule,
    equality_transitivity_inference_rule,
)


def right_hopf_transport_inputs(
    goal: object, beta: object,
) -> tuple[Relation, Relation] | None:
    """Build the two exact independent premises for a typed H right transport.

    From H(alpha o E beta)=delta o E beta and E beta=gamma, the desired
    conclusion is H(alpha o gamma)=delta o gamma. No textual name matching
    or unverified relation is admitted.
    """
    if (not isinstance(goal, Relation)
            or goal.relation_type is not RelationType.EQUALITY
            or not isinstance(goal.lhs, MapApplication)
            or goal.lhs.map != EHP_H_MAP
            or not isinstance(goal.lhs.expression, Composition)
            or not isinstance(goal.rhs, Composition)
            or not isinstance(beta, Composition)):
        return None
    alpha = goal.lhs.expression.left
    gamma = goal.lhs.expression.right
    delta = goal.rhs.left
    if (not isinstance(alpha, (HomotopyElement, Composition))
            or not isinstance(gamma, Composition)
            or not isinstance(delta, (HomotopyElement, Composition))
            or goal.rhs.right != gamma):
        return None
    alpha_span = expression_endpoints(alpha)
    beta_span = expression_endpoints(beta)
    gamma_span = expression_endpoints(gamma)
    delta_span = expression_endpoints(delta)
    if (alpha_span is None or beta_span is None or gamma_span is None
            or delta_span is None
            or gamma_span != (beta_span[0] + 1, beta_span[1] + 1)
            or alpha_span[0] != gamma_span[1]
            or delta_span != (alpha_span[0], 2 * alpha_span[1] - 1)):
        return None
    suspended = Suspension(beta)
    substituted = Relation(
        MapApplication(EHP_H_MAP, Composition(alpha, suspended)),
        Composition(delta, suspended),
        RelationType.EQUALITY,
    )
    suspension = Relation(suspended, gamma, RelationType.EQUALITY)
    return substituted, suspension


def _derive_existing_step(
    inference_rule: object,
    premises: tuple[ProofStep, ...],
    expected: Relation,
) -> ProofStep:
    """Replay an actual existing rule and fail closed if its result differs."""
    matches = find_inference_matches_for_rule(inference_rule, premises)
    if len(matches) != 1:
        raise ValueError("EXISTING_RULE_MATCH_NOT_UNIQUE")
    derived = apply_inference_match(matches[0])
    if (derived.rule is not ProofRule.INFERENCE
            or derived.conclusion != expected
            or derived.premises != premises
            or derived.inference_rule is not inference_rule):
        raise ValueError("EXISTING_RULE_REPLAY_MISMATCH")
    return derived


def replay_right_hopf_transport(
    goal: Relation,
    beta: Composition,
    substituted_step: ProofStep,
    suspension_step: ProofStep,
) -> tuple[ProofStep, ...]:
    """Return six inferred steps using only pre-existing congruence rules.

    The returned final step has a complete two-branch premise tree.  Neither
    independent input is manufactured; callers must obtain them from their
    ordinary source-screened proof process.
    """
    required = right_hopf_transport_inputs(goal, beta)
    if required is None:
        raise ValueError("INVALID_TYPED_HOPF_TRANSPORT_GOAL")
    substituted, suspension = required
    if (not isinstance(substituted_step, ProofStep)
            or not isinstance(suspension_step, ProofStep)
            or substituted_step.rule is not ProofRule.INFERENCE
            or suspension_step.rule is not ProofRule.INFERENCE
            or substituted_step.conclusion != substituted
            or suspension_step.conclusion != suspension):
        raise ValueError("INDEPENDENT_INFERENCE_PREMISES_REQUIRED")

    alpha = goal.lhs.expression.left
    gamma = goal.lhs.expression.right
    delta = goal.rhs.left
    suspended = Suspension(beta)
    alpha_comp = _derive_existing_step(
        equality_preserved_under_left_composition_inference_rule(alpha),
        (suspension_step,),
        Relation(Composition(alpha, suspended), Composition(alpha, gamma),
                 RelationType.EQUALITY),
    )
    hopf_comp = _derive_existing_step(
        ehp_h_preserves_equality_inference_rule(),
        (alpha_comp,),
        Relation(substituted.lhs, goal.lhs, RelationType.EQUALITY),
    )
    reverse_hopf_comp = _derive_existing_step(
        equality_symmetry_inference_rule(),
        (hopf_comp,),
        Relation(goal.lhs, substituted.lhs, RelationType.EQUALITY),
    )
    delta_comp = _derive_existing_step(
        equality_preserved_under_left_composition_inference_rule(delta),
        (suspension_step,),
        Relation(substituted.rhs, goal.rhs, RelationType.EQUALITY),
    )
    intermediate = _derive_existing_step(
        equality_transitivity_inference_rule(),
        (reverse_hopf_comp, substituted_step),
        Relation(goal.lhs, substituted.rhs, RelationType.EQUALITY),
    )
    result = _derive_existing_step(
        equality_transitivity_inference_rule(),
        (intermediate, delta_comp),
        goal,
    )
    return alpha_comp, hopf_comp, reverse_hopf_comp, delta_comp, intermediate, result
```

## audit.py

```python
"""Read-only Phase 176 R3R38 source-screened local replay audit."""
from __future__ import annotations

import argparse
import ast
import json
import os
from pathlib import Path
import sys
import tempfile

PACKAGE = "phase176_r3r38_equality_transport_isolated"
ROOT = Path(__file__).resolve().parent.parent


def source_guard() -> None:
    """Require exactly the already-reviewed public hooks and existing rules."""
    required = (
        "phase165_r52_r9_shared_math.py",
        "phase176_r3r34_composite_suspension_isolated/source.py",
        "phase176_r3r36_composite_right_hopf_isolated/source.py",
        "relation_rules.py",
        "hopf_rules.py",
    )
    for path in required:
        source = ROOT / path
        if not source.is_file():
            raise ValueError("MISSING_SOURCE:" + path)
        ast.parse(source.read_text(encoding="utf-8-sig"), filename=str(source))
    shared = (ROOT / "phase165_r52_r9_shared_math.py").read_text(encoding="utf-8-sig")
    anchors = (
        "options.extend(expand_composite_suspension_equality(goal))",
        "options.extend(expand_cited_composite_right_hopf(goal, tuple(available)))",
    )
    if any(shared.count(anchor) != 1 for anchor in anchors):
        raise ValueError("R3R35_R3R37_PUBLIC_HOOKS_REQUIRED")


def probe() -> dict:
    """Replay sourced R3R35+R3R37 input proofs and six old transport rules."""
    from expression import Composition, GeneratorSymbol, HomotopyElement, MapApplication, Suspension
    from map_facts import EHP_H_MAP
    from phase165_r52_r9_shared_math import build_shared_typed_bridge, shared_expansion_provider
    from phase165_r55_nk_only_goal import registered_group_goal_candidates
    from phase169_r10e2_unpositioned_citation.source_first import (
        screen_independent_sources_for_derived_goal,
    )
    from phase171_r2h_prop22_cited_hopf.source import TodaProp22RightFormula
    from phase176_r3r34_composite_suspension_isolated.source import (
        composite_suspension_equality_input,
    )
    from phase176_r3r36_composite_right_hopf_isolated.source import (
        COMPOSITE_FORMULA_RULE_NAME,
        COMPOSITE_SUBSTITUTION_RULE_NAME,
    )
    from phase176_r3r38_equality_transport_isolated.source import (
        right_hopf_transport_inputs,
        replay_right_hopf_transport,
    )
    from proof import ProofRule, Relation, RelationType, find_inference_match, apply_inference_match
    from unified_statement_registry import AssertionOrigin

    nu_prime = HomotopyElement("ν′", 3, 6, 3, GeneratorSymbol("ν", decoration="′"))
    eta5 = HomotopyElement("η₅", 5, 6, 5, GeneratorSymbol("η", index=5))
    eta6 = HomotopyElement("η₆", 6, 7, 6, GeneratorSymbol("η", index=6))
    eta7 = HomotopyElement("η₇", 7, 8, 7, GeneratorSymbol("η", index=7))
    beta = Composition(eta5, eta6)
    gamma = Composition(eta6, eta7)
    suspension_goal = Relation(Suspension(beta), gamma, RelationType.EQUALITY)
    goal = Relation(
        MapApplication(EHP_H_MAP, Composition(nu_prime, gamma)),
        Composition(eta5, gamma), RelationType.EQUALITY,
    )
    required = right_hopf_transport_inputs(goal, beta)
    if required is None or required[1] != suspension_goal:
        raise RuntimeError("TRANSPORT_TYPED_PREMISES_INVALID")
    substituted, _ = required
    formula = Relation(
        substituted.lhs,
        Composition(MapApplication(EHP_H_MAP, nu_prime), Suspension(beta)),
        RelationType.EQUALITY,
    )
    hopf_value = Relation(MapApplication(EHP_H_MAP, nu_prime), eta5,
                          RelationType.EQUALITY)

    bridge = build_shared_typed_bridge()
    roots = registered_group_goal_candidates(bridge, n=3, k=5)
    if len(roots) != 1:
        raise RuntimeError("ROOT_NOT_UNIQUE")
    screened = screen_independent_sources_for_derived_goal(bridge, goal=roots[0])
    fixed_steps = tuple(
        link.step for link in screened.proof_links
        if link.step is not None
        and link.step.rule is ProofRule.GIVEN
        and screened.registry.assertion(link.assertion_id).origin is AssertionOrigin.FIXED_STATEMENT
    )
    available = tuple(step.conclusion for step in fixed_steps)
    if (available.count(TodaProp22RightFormula()) != 1
            or available.count(hopf_value) != 1):
        raise RuntimeError("SCREENED_SOURCES_NOT_UNIQUE")
    prop22_step = next(s for s in fixed_steps if s.conclusion == TodaProp22RightFormula())
    hopf_step = next(s for s in fixed_steps if s.conclusion == hopf_value)
    provider = shared_expansion_provider(screened, proof_target=roots[0])

    def choose(item, rule_name):
        matches = tuple(x for x in provider(item) if x.rule.name == rule_name)
        if len(matches) != 1:
            raise RuntimeError("PROVIDER_CANDIDATE_NOT_UNIQUE:" + rule_name)
        return matches[0]

    formula_candidate = choose(formula, COMPOSITE_FORMULA_RULE_NAME)
    substitution_candidate = choose(substituted, COMPOSITE_SUBSTITUTION_RULE_NAME)
    suspension_candidate = choose(
        suspension_goal, "proved composite suspension image yields typed element equality",
    )
    image_goal = composite_suspension_equality_input(suspension_goal)
    if (image_goal is None
            or formula_candidate.subgoals != (TodaProp22RightFormula(),)
            or substitution_candidate.subgoals != (formula, hopf_value)
            or suspension_candidate.subgoals != (image_goal,)):
        raise RuntimeError("PUBLIC_SUBGOALS_CHANGED")
    image_candidates = tuple(x for x in provider(image_goal) if not x.subgoals)
    if len(image_candidates) != 1:
        raise RuntimeError("IMAGE_LEAF_NOT_UNIQUE")

    def apply_one(candidate, steps, expected):
        match = find_inference_match(candidate.rule, steps)
        if match is None:
            raise RuntimeError("CANNOT_REPLAY:" + candidate.rule.name)
        step = apply_inference_match(match)
        if (step.rule is not ProofRule.INFERENCE or step.conclusion != expected
                or step.premises != steps):
            raise RuntimeError("REPLAY_OUTPUT_INVALID:" + candidate.rule.name)
        return step

    formula_step = apply_one(formula_candidate, (prop22_step,), formula)
    substituted_step = apply_one(substitution_candidate, (formula_step, hopf_step), substituted)
    image_step = apply_one(image_candidates[0], (), image_goal)
    suspension_step = apply_one(suspension_candidate, (image_step,), suspension_goal)
    transport = replay_right_hopf_transport(
        goal, beta, substituted_step, suspension_step,
    )
    if transport[-1].conclusion != goal or len(transport) != 6:
        raise RuntimeError("TRANSPORT_REPLAY_NOT_CONCLUDED")
    return {
        "gate": "PASS_R3R38_SOURCED_LOCAL_TRANSPORT_REPLAY_NOT_PUBLIC",
        "source_screened_prop22_count": available.count(TodaProp22RightFormula()),
        "source_screened_hopf_value_count": available.count(hopf_value),
        "r3r35_suspension_inference_replayed": True,
        "r3r37_hopf_substitution_replayed": True,
        "old_transport_inference_steps": len(transport),
        "old_transport_rule_names": [x.inference_rule.name for x in transport],
        "transport_to_eta_composite_local_replayed": True,
        "shared_provider_modified": False,
        "shared_dfs_source_order_gate_verified": False,
        "toda55_eta_cube_equivalence_proved": False,
        "hopf_image_goal_proved_in_shared_dfs": False,
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
        result = ({
            "gate": "PASS_R3R38_DRYRUN",
            "full_pytest": "NOT_RUN",
        } if args.dry_run else probe())
    except Exception as error:
        result = {
            "gate": "FAIL_R3R38",
            "error": type(error).__name__ + ": " + str(error),
            "full_pytest": "NOT_RUN",
        }
    destination = (Path(os.environ.get("LOCALAPPDATA") or tempfile.gettempdir())
                   / "EHPProofTracerAudit" / PACKAGE / "report.json")
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n",
                           encoding="utf-8")
    for key, value in result.items():
        print("PHASE176_R3R38_" + key.upper() + "=" + str(value))
    print("REPORT=" + str(destination))
    print("(END)")
    return 0 if result["gate"].startswith("PASS_") else 1


if __name__ == "__main__":
    sys.exit(main())
```

## tests/test_source.py

```python
"""R3R38 pure-rule tests; synthetic input steps are NOT proof certificates."""
from __future__ import annotations

from dataclasses import replace

import pytest

from expression import Composition, GeneratorSymbol, HomotopyElement, MapApplication, Suspension
from map_facts import EHP_H_MAP
from phase176_r3r38_equality_transport_isolated.source import (
    replay_right_hopf_transport,
    right_hopf_transport_inputs,
)
from proof import ProofRule, ProofStep, Relation, RelationType


def _case():
    alpha = HomotopyElement("ν′", 3, 6, 3, GeneratorSymbol("ν", decoration="′"))
    delta = HomotopyElement("η₅", 5, 6, 5, GeneratorSymbol("η", index=5))
    first = HomotopyElement("η₅", 5, 6, 5, GeneratorSymbol("η", index=5))
    second = HomotopyElement("η₆", 6, 7, 6, GeneratorSymbol("η", index=6))
    third = HomotopyElement("η₇", 7, 8, 7, GeneratorSymbol("η", index=7))
    beta = Composition(first, second)
    gamma = Composition(second, third)
    goal = Relation(MapApplication(EHP_H_MAP, Composition(alpha, gamma)),
                    Composition(delta, gamma), RelationType.EQUALITY)
    return alpha, delta, beta, gamma, goal


def _synthetic_inputs():
    _, _, beta, _, goal = _case()
    premises = right_hopf_transport_inputs(goal, beta)
    assert premises is not None
    return beta, goal, ProofStep(premises[0], (), ProofRule.INFERENCE), ProofStep(
        premises[1], (), ProofRule.INFERENCE,
    )


def test_builds_two_explicit_typed_obligations():
    alpha, delta, beta, gamma, goal = _case()
    substituted, suspension = right_hopf_transport_inputs(goal, beta)
    assert substituted.lhs.expression == Composition(alpha, Suspension(beta))
    assert substituted.rhs == Composition(delta, Suspension(beta))
    assert suspension == Relation(Suspension(beta), gamma, RelationType.EQUALITY)


def test_replays_six_preexisting_inference_rules_without_new_axioms():
    beta, goal, left, right = _synthetic_inputs()
    chain = replay_right_hopf_transport(goal, beta, left, right)
    assert len(chain) == 6
    assert chain[-1].conclusion == goal
    assert all(x.rule is ProofRule.INFERENCE for x in chain)
    assert [x.inference_rule.name for x in chain] == [
        "equality preserved under left composition",
        "EHP H preserves equality",
        "equality symmetry",
        "equality preserved under left composition",
        "equality transitivity",
        "equality transitivity",
    ]
    assert chain[0].premises == (right,)
    assert chain[3].premises == (right,)
    assert chain[4].premises == (chain[2], left)
    assert chain[5].premises == (chain[4], chain[3])


def test_independently_inferred_inputs_required():
    beta, goal, left, right = _synthetic_inputs()
    with pytest.raises(ValueError, match="INDEPENDENT_INFERENCE_PREMISES_REQUIRED"):
        replay_right_hopf_transport(goal, beta,
                                    ProofStep(left.conclusion, (), ProofRule.GIVEN), right)
    with pytest.raises(ValueError, match="INDEPENDENT_INFERENCE_PREMISES_REQUIRED"):
        replay_right_hopf_transport(goal, beta, left,
                                    ProofStep(right.conclusion, (), ProofRule.GIVEN))
    with pytest.raises(ValueError, match="INDEPENDENT_INFERENCE_PREMISES_REQUIRED"):
        replay_right_hopf_transport(goal, beta, None, right)


def test_wrong_suspension_or_formula_are_rejected():
    beta, goal, left, right = _synthetic_inputs()
    with pytest.raises(ValueError, match="INDEPENDENT_INFERENCE_PREMISES_REQUIRED"):
        replay_right_hopf_transport(
            goal, beta,
            ProofStep(replace(left.conclusion, rhs=goal.rhs), (), ProofRule.INFERENCE),
            right,
        )
    with pytest.raises(ValueError, match="INDEPENDENT_INFERENCE_PREMISES_REQUIRED"):
        replay_right_hopf_transport(
            goal, beta, left,
            ProofStep(replace(right.conclusion, rhs=beta), (), ProofRule.INFERENCE),
        )


def test_wrong_goal_shape_types_and_dimensions_fail_closed():
    alpha, delta, beta, gamma, goal = _case()
    assert right_hopf_transport_inputs(replace(goal, rhs=delta), beta) is None
    assert right_hopf_transport_inputs(replace(goal, rhs=Composition(delta, beta)), beta) is None
    assert right_hopf_transport_inputs(goal, delta) is None
    assert right_hopf_transport_inputs(replace(goal, lhs=goal.rhs), beta) is None
    assert right_hopf_transport_inputs(
        replace(goal, rhs=Composition(replace(delta, target=4), gamma)), beta,
    ) is None
    assert right_hopf_transport_inputs(
        replace(goal, lhs=MapApplication(EHP_H_MAP, Composition(
            replace(alpha, source=100), gamma,
        ))), beta,
    ) is None
    with pytest.raises(ValueError, match="INVALID_TYPED_HOPF_TRANSPORT_GOAL"):
        replay_right_hopf_transport(replace(goal, rhs=delta), beta,
                                    ProofStep(goal, (), ProofRule.INFERENCE),
                                    ProofStep(goal, (), ProofRule.INFERENCE))


def test_not_hardcoded_to_nu_prime_eta_names():
    alpha, delta, beta, gamma, _ = _case()
    other_alpha = replace(alpha, name="formal-alpha", generator=None)
    other_delta = replace(delta, name="formal-delta", generator=None)
    goal = Relation(MapApplication(EHP_H_MAP, Composition(other_alpha, gamma)),
                    Composition(other_delta, gamma), RelationType.EQUALITY)
    assert right_hopf_transport_inputs(goal, beta) is not None
    inputs = right_hopf_transport_inputs(goal, beta)
    assert inputs is not None
    steps = replay_right_hopf_transport(
        goal, beta,
        ProofStep(inputs[0], (), ProofRule.INFERENCE),
        ProofStep(inputs[1], (), ProofRule.INFERENCE),
    )
    assert steps[-1].conclusion == goal
```

## run.ps1

```powershell
param([switch]$DryRun)
$ErrorActionPreference = 'Stop'
$root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Push-Location $root
try {
    $parameters = @()
    if ($DryRun) { $parameters += '--dry-run' }
    & python -B -m phase176_r3r38_equality_transport_isolated.audit @parameters
    if ($LASTEXITCODE -ne 0) { throw 'R3R38 audit failed' }
    if (-not $DryRun) {
        & python -B -m pytest -q -p no:cacheprovider `
            .\phase176_r3r38_equality_transport_isolated\tests\test_source.py `
            .\phase176_r3r34_composite_suspension_isolated\tests\test_source.py `
            .\phase176_r3r36_composite_right_hopf_isolated\tests\test_source.py `
            .\phase171_r2h_prop22_cited_hopf\tests\test_cited_formula.py
        if ($LASTEXITCODE -ne 0) { throw 'R3R38 focused pytest failed' }
        & git diff --check
        if ($LASTEXITCODE -ne 0) { throw 'R3R38 git diff check failed' }
        Write-Host 'PHASE176_R3R38_GATE=PASS_R3R38_ISOLATED_FOCUSED_TESTS'
        Write-Host 'PHASE176_R3R38_FULL_PYTEST=NOT_RUN'
        Write-Host '(END)'
    }
} finally {
    Pop-Location
}
```

