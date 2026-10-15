"""R26 focused tests; synthetic statements do not certify Toda mathematics."""
from dataclasses import dataclass

import pytest

from phase165_r3_recursive_search import GoalExpansion
from phase165_r57_r26_generic_search_connection import (
    build_generic_backward_expansion_provider,
    merge_backward_expansions,
)
from proof import InferenceRule, PatternVariable, PremisePattern


@dataclass(frozen=True)
class Claim:
    value: object


def test_r26_proposes_fully_bound_subgoals():
    x = PatternVariable("x")
    rule = InferenceRule(
        name="synthetic",
        conclusion_pattern=Claim(x),
        premise_patterns=(PremisePattern(statement_pattern=Claim(x)),),
    )
    provider = build_generic_backward_expansion_provider((rule,))
    assert provider(Claim(7)) == (GoalExpansion(rule, (Claim(7),)),)


def test_r26_rejects_unbound_premise_variable():
    x, y = PatternVariable("x"), PatternVariable("y")
    rule = InferenceRule(
        name="unbound", conclusion_pattern=Claim(x),
        premise_patterns=(PremisePattern(statement_pattern=Claim(y)),),
    )
    assert build_generic_backward_expansion_provider((rule,))(Claim(2)) == ()


def test_r26_rejects_opaque_builder_only_rule():
    rule = InferenceRule(
        name="builder only", conclusion_builder=lambda premises: Claim(5),
        premise_patterns=(PremisePattern(statement_pattern=Claim(3)),),
    )
    assert build_generic_backward_expansion_provider((rule,))(Claim(5)) == ()


def test_r26_candidate_does_not_prove_a_claim():
    x = PatternVariable("x")
    rule = InferenceRule(
        name="not a proof", conclusion_pattern=Claim(x),
        premise_patterns=(PremisePattern(statement_pattern=Claim(x)),),
    )
    expansion, = build_generic_backward_expansion_provider((rule,))(Claim(3))
    assert isinstance(expansion, GoalExpansion)
    assert not hasattr(expansion, "conclusion")


def test_r26_merger_suppresses_exact_duplicate_identity():
    rule = InferenceRule("reused")
    first = GoalExpansion(rule, (Claim(1),))
    assert merge_backward_expansions((first,), (first,)) == (first,)


def test_r26_merger_retains_distinct_derivations():
    a, b = InferenceRule("same name"), InferenceRule("same name")
    first = GoalExpansion(a, (Claim(1),))
    second = GoalExpansion(b, (Claim(1),))
    assert merge_backward_expansions((first,), (second,)) == (first, second)


def test_r26_invalid_input_rejected():
    with pytest.raises(TypeError):
        build_generic_backward_expansion_provider((object(),))
    with pytest.raises(TypeError):
        merge_backward_expansions([], ())
