"""Run against the actual installed repository after R4-4 stage 5."""

from expression import MapSymbol
from map_property_rules import (
    InjectiveMapStatement,
    IsomorphismStatement,
    SurjectiveMapStatement,
    injective_and_surjective_imply_isomorphism_inference_rule,
)
from phase165_r57_r26_generic_search_connection import build_generic_backward_expansion_provider
from phase165_r8_rule_provider import create_rule_expansion_provider, discover_inference_rules
from proof import ProofRule, ProofStep, apply_inference_match, find_inference_match


def test_stage5_forward_valid_same_map():
    f = MapSymbol(name="f")
    rule = injective_and_surjective_imply_isomorphism_inference_rule()
    premises = (
        ProofStep(conclusion=InjectiveMapStatement(map=f), premises=(), rule=ProofRule.GIVEN),
        ProofStep(conclusion=SurjectiveMapStatement(map=f), premises=(), rule=ProofRule.GIVEN),
    )
    match = find_inference_match(rule, premises)
    assert match is not None
    step = apply_inference_match(match)
    assert step.conclusion == IsomorphismStatement(map=f)
    assert step.premises == premises
    assert step.inference_rule is rule


def test_stage5_forward_rejects_distinct_maps():
    f = MapSymbol(name="f")
    g = MapSymbol(name="g")
    rule = injective_and_surjective_imply_isomorphism_inference_rule()
    premises = (
        ProofStep(conclusion=InjectiveMapStatement(map=f), premises=(), rule=ProofRule.GIVEN),
        ProofStep(conclusion=SurjectiveMapStatement(map=g), premises=(), rule=ProofRule.GIVEN),
    )
    assert find_inference_match(rule, premises) is None


def test_stage5_reverse_r8():
    f = MapSymbol(name="f")
    rule = injective_and_surjective_imply_isomorphism_inference_rule()
    expansions = create_rule_expansion_provider((rule,))(IsomorphismStatement(map=f))
    assert len(expansions) == 1
    assert expansions[0].subgoals == (InjectiveMapStatement(map=f), SurjectiveMapStatement(map=f))


def test_stage5_reverse_r26():
    f = MapSymbol(name="f")
    rule = injective_and_surjective_imply_isomorphism_inference_rule()
    expansions = build_generic_backward_expansion_provider((rule,))(IsomorphismStatement(map=f))
    assert len(expansions) == 1
    assert expansions[0].subgoals == (InjectiveMapStatement(map=f), SurjectiveMapStatement(map=f))


def test_stage5_discovered_by_shared_catalog():
    rules, _ = discover_inference_rules()
    assert any(rule.name == "injectivity and surjectivity imply isomorphism" for rule in rules)
