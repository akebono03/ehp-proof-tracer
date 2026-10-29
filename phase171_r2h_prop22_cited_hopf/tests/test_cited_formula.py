"""R2H proof-origin and type-safety regressions against the current repository."""
from __future__ import annotations

from dataclasses import replace

import pytest

from expression import Composition, GeneratorSymbol, HomotopyElement, MapApplication, Suspension
from map_facts import EHP_H_MAP
from phase163_r4_registry_bridge import RegistryBridgeResult
from phase165_r9_production_wiring import discover_goal_search_inputs
from phase171_r2h_prop22_cited_hopf.source import (
    ASSERTION_ID, SOURCE_ID, TodaProp22RightFormula,
    _formula_parts, build_cited_prop22_right_reference,
    cited_prop22_right_specialization_rule, expand_cited_prop22_right_formula,
)
from proof import ProofRule, Relation, RelationType
from unified_statement_registry import AssertionOrigin, UnifiedStatementRegistry


def _elements():
    alpha = HomotopyElement(
        "ν′", 3, 6, 3, GeneratorSymbol("ν", decoration="′"),
    )
    beta = HomotopyElement(
        "η₅", 5, 6, 5, GeneratorSymbol("η", index=5),
    )
    return alpha, beta


def _formal_goal():
    alpha, beta = _elements()
    return Relation(
        MapApplication(EHP_H_MAP, Composition(alpha, Suspension(beta))),
        Composition(MapApplication(EHP_H_MAP, alpha), Suspension(beta)),
        RelationType.EQUALITY,
    )


def test_proposition_22_archived_source_and_general_given():
    source_bridge = discover_goal_search_inputs().bridge
    cited = build_cited_prop22_right_reference(source_bridge)
    assert len(cited.proof_links) == 1
    assert cited.proof_links[0].step.rule is ProofRule.GIVEN
    assert cited.proof_links[0].step.conclusion == TodaProp22RightFormula()
    assertion = cited.registry.assertion(ASSERTION_ID)
    assert assertion.origin is AssertionOrigin.FIXED_STATEMENT
    assert cited.registry.reference(assertion.reference_id).locator == "Proposition 2.2"


def test_proposition_22_rejects_falsified_source_bytes():
    base = discover_goal_search_inputs().bridge
    registry = UnifiedStatementRegistry()
    for reference in base.registry._references.values():
        registry.add_reference(reference)
    for assertion in base.registry._assertions.values():
        if (assertion.origin is AssertionOrigin.SOURCE_ARCHIVE
                and isinstance(assertion.content, dict)
                and assertion.content.get("source_statement_id") == SOURCE_ID):
            modified = dict(assertion.content)
            modified["source_text"] += " altered"
            assertion = replace(assertion, content=modified)
        registry.add_assertion(assertion)
    tampered = RegistryBridgeResult(registry, base.records, base.proof_links)
    with pytest.raises(ValueError, match="source verification"):
        build_cited_prop22_right_reference(tampered)


def test_right_formula_requires_screened_source():
    goal = _formal_goal()
    assert _formula_parts(goal) is not None
    assert expand_cited_prop22_right_formula(goal, ()) == ()
    options = expand_cited_prop22_right_formula(goal, (TodaProp22RightFormula(),))
    assert len(options) == 1
    assert options[0].subgoals == (TodaProp22RightFormula(),)
    assert cited_prop22_right_specialization_rule(goal).conclusion_pattern == goal


def test_right_formula_rejects_wrong_rhs_and_bad_dimensions():
    goal = _formal_goal()
    bad_rhs = replace(goal, rhs=goal.lhs.expression.right)
    assert expand_cited_prop22_right_formula(bad_rhs, (TodaProp22RightFormula(),)) == ()
    alpha, beta = _elements()
    invalid_alpha = replace(alpha, source=70)
    bad_goal = Relation(
        MapApplication(EHP_H_MAP, Composition(invalid_alpha, Suspension(beta))),
        Composition(MapApplication(EHP_H_MAP, invalid_alpha), Suspension(beta)),
        RelationType.EQUALITY,
    )
    assert _formula_parts(bad_goal) is None


def test_hopf_substitution_requires_exact_screened_hopf_relation():
    alpha, beta = _elements()
    final = Relation(
        MapApplication(EHP_H_MAP, Composition(alpha, Suspension(beta))),
        Composition(beta, Suspension(beta)),
        RelationType.EQUALITY,
    )
    source = TodaProp22RightFormula()
    hopf = Relation(MapApplication(EHP_H_MAP, alpha), beta, RelationType.EQUALITY)
    assert expand_cited_prop22_right_formula(final, (source,)) == ()
    assert expand_cited_prop22_right_formula(final, (source, hopf, hopf)) == ()
    options = expand_cited_prop22_right_formula(final, (source, hopf))
    assert len(options) == 1
    assert options[0].subgoals[1] == hopf
    assert _formula_parts(options[0].subgoals[0]) is not None


def test_cited_proposition_22_actual_two_step_proof_tree():
    from phase171_r2h_prop22_cited_hopf.audit import run
    run()
