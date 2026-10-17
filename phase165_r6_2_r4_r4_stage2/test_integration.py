"""Targeted tests against the actual project inference engine."""
from expression import MapSymbol
from map_property_rules import (
    ImageWholeStatement, InjectiveMapStatement, KernelZeroStatement,
    SurjectiveMapStatement, kernel_zero_implies_injective_inference_rule,
    whole_image_implies_surjective_inference_rule,
)
from phase165_r8_rule_provider import create_rule_expansion_provider, discover_inference_rules
from phase165_r57_r26_generic_search_connection import build_generic_backward_expansion_provider
from proof import ProofRule, ProofStep, apply_inference_match, find_inference_match


def test_zero_kernel_backward_r8():
    f = MapSymbol(name="f")
    rule = kernel_zero_implies_injective_inference_rule()
    result = create_rule_expansion_provider((rule,))(InjectiveMapStatement(map=f))
    assert len(result) == 1
    assert result[0].subgoals == (KernelZeroStatement(map=f),)


def test_full_image_backward_r26():
    f = MapSymbol(name="f")
    rule = whole_image_implies_surjective_inference_rule()
    result = build_generic_backward_expansion_provider((rule,))(SurjectiveMapStatement(map=f))
    assert len(result) == 1
    assert result[0].subgoals == (ImageWholeStatement(map=f),)


def test_rule_forward_inference_still_verified():
    f = MapSymbol(name="f")
    rule = kernel_zero_implies_injective_inference_rule()
    given = ProofStep(conclusion=KernelZeroStatement(map=f), premises=(), rule=ProofRule.GIVEN)
    match = find_inference_match(rule, (given,))
    assert match is not None
    result = apply_inference_match(match)
    assert result.conclusion == InjectiveMapStatement(map=f)
    assert result.premises == (given,)


def test_rule_auto_discovered():
    rules, _ = discover_inference_rules()
    names = [rule.name for rule in rules]
    assert "zero kernel implies injectivity" in names
    assert "whole image implies surjectivity" in names


def test_no_cross_map_instantiation():
    f = MapSymbol(name="f")
    g = MapSymbol(name="g")
    rule = kernel_zero_implies_injective_inference_rule()
    result = create_rule_expansion_provider((rule,))(InjectiveMapStatement(map=f))
    assert result[0].subgoals != (KernelZeroStatement(map=g),)
