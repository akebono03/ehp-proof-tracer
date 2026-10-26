"""R3O focused tests for existing 2-stem rows and strict (4.5) premises."""
from __future__ import annotations

from dataclasses import replace

from expression import Composition, GeneratorSymbol, HomotopyElement
from homotopy_groups import FiniteCyclicGroup, TodaPrimaryGroup
from phase165_r14_r6_generic_iso import GeneratorImage
from phase165_r57_r20_general_specialization import specialize_typed_statement
from phase165_r52_r27_r5_literature import _toda45_universal_statement
from phase166_r3aj_structured_generator import database_structured_group_goal_candidates
from phase169_r3o_stable_composite_rule import (
    expand_cited_toda45_composite_transport,
    toda45_composite_transport_rule,
)
from proof import ProofRule, ProofStep, Relation, RelationType, find_inference_matches_for_rule, apply_inference_match
from toda_rules import Toda45IsomorphismStatement


def _pi(n):
    result = database_structured_group_goal_candidates(n=n, k=2)
    assert len(result) == 1
    return result[0]


def test_r3o_pi75_gets_real_prior_db_relation_without_prior_proof():
    lower, higher = _pi(4), _pi(5)
    schema = _toda45_universal_statement()
    options = expand_cited_toda45_composite_transport(higher, (lower, schema))
    assert len(options) == 1
    assert options[0].subgoals[0] == lower
    assert isinstance(options[0].subgoals[1], Toda45IsomorphismStatement)
    assert isinstance(options[0].subgoals[2], GeneratorImage)
    assert specialize_typed_statement(schema, options[0].subgoals[1]) is not None


def test_r3o_result_requires_all_three_evidenced_premises():
    lower, higher = _pi(4), _pi(5)
    expansion = expand_cited_toda45_composite_transport(
        higher, (lower, _toda45_universal_statement()),
    )[0]
    source, iso, image = expansion.subgoals
    proof_steps = (
        ProofStep(conclusion=source, premises=(), rule=ProofRule.GIVEN),
        ProofStep(conclusion=iso, premises=(), rule=ProofRule.INFERENCE),
        ProofStep(conclusion=image, premises=(), rule=ProofRule.INFERENCE),
    )
    matches = find_inference_matches_for_rule(expansion.rule, proof_steps)
    assert len(matches) == 1
    result = apply_inference_match(matches[0])
    assert result.rule is ProofRule.INFERENCE
    assert result.conclusion == higher
    assert result.premises == proof_steps


def test_r3o_missing_toda45_is_not_an_admissible_expansion():
    assert expand_cited_toda45_composite_transport(_pi(5), (_pi(4),)) == ()


def test_r3o_source_below_stable_range_cannot_use_toda45():
    assert expand_cited_toda45_composite_transport(
        _pi(4), (_pi(3), _toda45_universal_statement()),
    ) == ()


def test_r3o_arbitrary_composition_is_not_a_cited_eta_image():
    lower, higher = _pi(4), _pi(5)
    bad = replace(higher, rhs=FiniteCyclicGroup(2, Composition(
        HomotopyElement(name="ν_5", dimension=5, source=8, target=5,
                        generator=GeneratorSymbol("ν", 5)),
        HomotopyElement(name="η_8", dimension=8, source=9, target=8,
                        generator=GeneratorSymbol("η", 8)),
    )))
    assert expand_cited_toda45_composite_transport(
        bad, (lower, _toda45_universal_statement()),
    ) == ()


def test_r3o_rejects_unproved_concrete_map_or_generator_image():
    lower, higher = _pi(4), _pi(5)
    expansion = expand_cited_toda45_composite_transport(
        higher, (lower, _toda45_universal_statement()),
    )[0]
    source, iso, image = expansion.subgoals
    fake = (
        ProofStep(conclusion=source, premises=(), rule=ProofRule.GIVEN),
        ProofStep(conclusion=iso, premises=(), rule=ProofRule.GIVEN),
        ProofStep(conclusion=image, premises=(), rule=ProofRule.GIVEN),
    )
    assert find_inference_matches_for_rule(expansion.rule, fake) == ()


def test_r3o_self_and_target_result_not_used_as_base():
    higher = _pi(5)
    assert expand_cited_toda45_composite_transport(
        higher, (higher, _toda45_universal_statement()),
    ) == ()
