"""Strict notation planning, rejected inputs, and independent checked replay."""
from dataclasses import replace

import pytest

from expression import Composition, GeneratorSymbol, MapApplication, Multiple
from phase165_r3_recursive_search import reconstruct_registered_goal
from phase165_r52_r9_shared_math import build_shared_typed_bridge, shared_expansion_provider
from phase169_r10e2_unpositioned_citation.source_first import screen_independent_sources_for_derived_goal
from phase169_r10e4_ordered_db_prior.db_prior import exact_prior_database_result
from phase176_r3r40r1_eta_notation_bridge.tests.test_notation import example
from phase176_r3r41_public_quadruple_connection.source import (
    _strict_public_quadruple_backward_plan, public_quadruple_backward_plan,
    build_public_quadruple_connection_provider,
)
from phase176_r3r49_hopf_image_frontier.audit import source_rows
from phase176_r3r50_strict_nu_prime_connection.apply import PINS, ROOT, updated_source
from phase176_r3r50_strict_nu_prime_connection.notation import RULE_NAME, alias_hopf_input, alias_hopf_rule
from proof import ProofRule, Relation, apply_inference_match, find_inference_matches_for_rule
from unified_statement_registry import AssertionOrigin


def example_goals():
    transported, forward, available = example()
    canonical = Relation(transported.lhs, forward.lhs)
    left = canonical.lhs.expression.left
    db = replace(left, name="ν'", generator=GeneratorSymbol("\\nu'"))
    goal = replace(canonical, lhs=MapApplication(canonical.lhs.map, Composition(db, canonical.lhs.expression.right)))
    return goal, canonical, available


def test_preserve_exact_plan_and_transport_one_step():
    goal, canonical, available = example_goals()
    strict = _strict_public_quadruple_backward_plan(canonical, available)
    assert len(strict) == 21
    assert not _strict_public_quadruple_backward_plan(goal, available)
    actual = public_quadruple_backward_plan(goal, available)
    assert len(actual) == len(strict) + 1
    assert [(g, o.rule.name, o.subgoals) for g, o in actual[:-1]] == [(g, o.rule.name, o.subgoals) for g, o in strict]
    target, option = actual[-1]
    assert target == goal and option.rule.name == RULE_NAME and option.subgoals == (canonical,)
    expand = build_public_quadruple_connection_provider(available)
    assert expand(goal)[0].subgoals == (canonical,)
    assert expand(canonical)[0].rule.name == strict[-1][1].rule.name
    assert goal not in available and canonical not in available


def test_missing_or_duplicate_sources_fail_closed():
    goal, canonical, available = example_goals()
    for index in range(len(available)):
        assert not public_quadruple_backward_plan(goal, available[:index] + available[index+1:])
        assert not public_quadruple_backward_plan(goal, available + (available[index],))
    assert not public_quadruple_backward_plan(goal, ())


def test_wrong_name_type_factor_and_rhs_rejected():
    goal, canonical, available = example_goals()
    expr = goal.lhs.expression
    for wrong in (replace(expr.left, name='ν'),
                  replace(expr.left, source=7),
                  replace(expr.left, dimension=4),
                  replace(expr.left, generator=GeneratorSymbol('η')),
                  replace(expr.left, generator=GeneratorSymbol("\\nu'", index=3))):
        bad = replace(goal, lhs=MapApplication(goal.lhs.map, Composition(wrong, expr.right)))
        assert alias_hopf_input(bad, canonical) is None
        assert not public_quadruple_backward_plan(bad, available)
    wrong_right = replace(expr.right, left=replace(expr.right.left, name='different'))
    bad = replace(goal, lhs=MapApplication(goal.lhs.map, Composition(expr.left, wrong_right)))
    assert alias_hopf_input(bad, canonical) is None
    assert alias_hopf_input(replace(goal, rhs=Multiple(2, goal.rhs.expression)), canonical) is None
    assert alias_hopf_input(goal, goal) is None
    with pytest.raises(ValueError):
        alias_hopf_rule(goal, goal)


def test_real_canonical_proof_is_required_and_replayed():
    root = exact_prior_database_result(3,5)
    bridge = screen_independent_sources_for_derived_goal(build_shared_typed_bridge(), goal=root)
    goal0, _, _ = example_goals()
    goal = Relation(MapApplication(goal0.lhs.map, root.rhs.generator), goal0.rhs)
    rows = [(item, row) for item, row in source_rows(bridge, root.rhs.generator.left)
            if row['locator'] == '(5.3)' and row['strict_nu_prime_alias'] and not row['exact_alpha']]
    (item, row), = rows
    canonical = Relation(MapApplication(goal.lhs.map, Composition(item.lhs.expression, root.rhs.generator.right)), goal.rhs)
    proof = reconstruct_registered_goal(canonical, bridge, row['assertion_id'],
                shared_expansion_provider(bridge, proof_target=root), lookup_mode='typed_reference')
    assert proof.conclusion == canonical and proof.rule is ProofRule.INFERENCE
    rule = alias_hopf_rule(goal, canonical)
    match, = find_inference_matches_for_rule(rule, (proof,))
    derived = apply_inference_match(match)
    assert derived.conclusion == goal and derived.rule is ProofRule.INFERENCE and derived.premises == (proof,)
    for invalid in (replace(proof, rule=ProofRule.GIVEN), replace(proof, premises=()),
                    replace(proof, inference_rule=None), replace(proof, conclusion=goal)):
        assert not find_inference_matches_for_rule(rule, (invalid,))
    assert not find_inference_matches_for_rule(rule, ())
    assert all(link.step is None or link.step.conclusion != goal for link in bridge.proof_links)
    assert any(bridge.registry.assertion(link.assertion_id).origin is AssertionOrigin.FIXED_STATEMENT
               and link.step is not None and link.step.conclusion == item for link in bridge.proof_links)


def test_exact_replacement_idempotence_and_unknown_bytes():
    for path in PINS:
        raw = (ROOT / path).read_bytes()
        assert updated_source(path, raw) == raw
        with pytest.raises(ValueError):
            updated_source(path, raw + b'\n# unknown change\n')
