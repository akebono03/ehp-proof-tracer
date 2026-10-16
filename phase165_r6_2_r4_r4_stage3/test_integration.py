from expression import MapSymbol
from proof import ExactnessStatement, ProofRule, ProofStep, find_inference_match, apply_inference_match
from phase165_r57_r26_generic_search_connection import build_generic_backward_expansion_provider
from phase165_r8_rule_provider import discover_inference_rules
from map_property_rules import (
    ImageZeroStatement, KernelWholeStatement, KernelZeroStatement, ImageWholeStatement,
    InjectiveMapStatement, SurjectiveMapStatement,
    exactness_and_zero_image_implies_zero_kernel_inference_rule,
    exactness_and_whole_kernel_implies_whole_image_inference_rule,
)


def given(value):
    return ProofStep(conclusion=value, premises=(), rule=ProofRule.GIVEN)


def test_zero_image_bridge_forward_and_inverse():
    a, b = MapSymbol(name="a"), MapSymbol(name="b")
    rule = exactness_and_zero_image_implies_zero_kernel_inference_rule()
    steps = (given(ExactnessStatement(a, b, True)), given(ImageZeroStatement(a)))
    match = find_inference_match(rule, steps)
    assert match is not None
    assert apply_inference_match(match).conclusion == KernelZeroStatement(b)
    proposals = build_generic_backward_expansion_provider((rule,))(KernelZeroStatement(b))
    # The predecessor map is free in the goal, so no unsupported choice is generated.
    assert proposals == ()


def test_whole_kernel_bridge_forward_and_inverse():
    a, b = MapSymbol(name="a"), MapSymbol(name="b")
    rule = exactness_and_whole_kernel_implies_whole_image_inference_rule()
    match = find_inference_match(rule, (given(ExactnessStatement(a, b, True)), given(KernelWholeStatement(b))))
    assert match is not None
    assert apply_inference_match(match).conclusion == ImageWholeStatement(a)
    assert build_generic_backward_expansion_provider((rule,))(ImageWholeStatement(a)) == ()


def test_rules_discovered_and_no_unbound_premises():
    rules, report = discover_inference_rules(("map_property_rules",))
    names = {r.name for r in rules}
    assert "exactness and zero image imply zero kernel" in names
    assert "exactness and whole kernel imply whole image" in names
    assert not build_generic_backward_expansion_provider(rules)(KernelZeroStatement(MapSymbol(name="b")))


def test_stage2_chain_still_generates():
    rules, report = discover_inference_rules(("map_property_rules",))
    f = MapSymbol(name="f")
    proposals = build_generic_backward_expansion_provider(rules)(InjectiveMapStatement(f))
    assert any(p.subgoals == (KernelZeroStatement(f),) for p in proposals)
    proposals = build_generic_backward_expansion_provider(rules)(SurjectiveMapStatement(f))
    assert any(p.subgoals == (ImageWholeStatement(f),) for p in proposals)
