"""Test the real typed backward rules, including the proof-parent boundary."""
from __future__ import annotations

from dataclasses import replace
from types import SimpleNamespace

import pytest

from expression import GeneratorSymbol, HomotopyElement, IteratedSuspension, Multiple
from proof import ProofRule, Relation, RelationType, find_inference_matches_for_rule
from phase173_r4_r1_lemma54_source_bridge.source import TodaLemma54TypedSource
from phase175_r3r6_lemma57_general.rule import TodaLemma57DoubleSuspensionMembership
from phase175_r3r7_lemma54_membership.rule import (
    FACTOR_RULE_NAME,
    SOURCE_RULE_NAME,
    canonical_nu_prime,
    cited_lemma54_double_relation,
    even_factorization_inputs,
    even_factor_membership_rule,
    expand_cited_lemma54_double,
    expand_even_factor_membership,
    lemma54_double_rule,
)


def test_source_double_relation_uses_true_sphere_degrees() -> None:
    from phase169_r10eq_r1_universal_stable_definition.definition import typed_element_span

    relation = cited_lemma54_double_relation()
    assert relation.relation_type is RelationType.EQUALITY
    assert relation.lhs.coefficient == 2
    assert relation.lhs.expression.exponent == 1
    assert typed_element_span(relation.lhs) == (8, 5)
    assert typed_element_span(relation.rhs) == (8, 5)
    assert relation.rhs.expression == canonical_nu_prime()


def test_source_extraction_requires_unique_cited_given() -> None:
    relation = cited_lemma54_double_relation()
    source = TodaLemma54TypedSource()
    assert expand_cited_lemma54_double(relation, ()) == ()
    assert expand_cited_lemma54_double(relation, (source, source)) == ()
    proposals = expand_cited_lemma54_double(relation, (source,))
    assert len(proposals) == 1
    assert proposals[0].rule.name == SOURCE_RULE_NAME
    assert proposals[0].subgoals == (source,)
    rule = lemma54_double_rule(relation)
    good = SimpleNamespace(rule=ProofRule.GIVEN, conclusion=source)
    wrong = SimpleNamespace(rule=ProofRule.INFERENCE, conclusion=source)
    assert rule.match_guard((good,), {}) is True
    assert rule.match_guard((wrong,), {}) is False


def test_inferred_double_equality_yields_membership_without_new_given() -> None:
    relation = cited_lemma54_double_relation()
    goal = TodaLemma57DoubleSuspensionMembership(canonical_nu_prime())
    assert even_factorization_inputs(goal, relation) == (relation,)
    options = expand_even_factor_membership(goal, (relation, relation))
    assert len(options) == 1
    assert options[0].subgoals == (relation,)
    assert options[0].rule.name == FACTOR_RULE_NAME
    rule = even_factor_membership_rule(goal, relation)
    given_source = SimpleNamespace(rule=ProofRule.GIVEN, conclusion=TodaLemma54TypedSource())
    inferred_relation = SimpleNamespace(
        rule=ProofRule.INFERENCE, conclusion=relation, premises=(given_source,),
    )
    no_proof = SimpleNamespace(rule=ProofRule.INFERENCE, conclusion=relation, premises=())
    direct_given = SimpleNamespace(rule=ProofRule.GIVEN, conclusion=relation, premises=())
    assert rule.match_guard((inferred_relation,), {}) is True
    assert rule.match_guard((no_proof,), {}) is False
    assert rule.match_guard((direct_given,), {}) is False


def test_accepted_db_alias_uses_registered_identity_not_display_name() -> None:
    db_alias = HomotopyElement(
        name="ν'", dimension=3, source=6, target=3,
        generator=GeneratorSymbol(r"\nu'"),
    )
    goal = TodaLemma57DoubleSuspensionMembership(db_alias)
    assert even_factorization_inputs(goal, cited_lemma54_double_relation()) is not None
    spoofed = HomotopyElement(
        name="ν′", dimension=3, source=6, target=3,
        generator=GeneratorSymbol("unregistered-nu-prime"),
    )
    assert even_factorization_inputs(
        TodaLemma57DoubleSuspensionMembership(spoofed),
        cited_lemma54_double_relation(),
    ) is None


def test_wrong_factor_degree_and_non_two_coefficients_rejected() -> None:
    relation = cited_lemma54_double_relation()
    goal = TodaLemma57DoubleSuspensionMembership(canonical_nu_prime())
    wrong_factor = HomotopyElement(
        name="ν₄", dimension=4, source=7, target=4,
        generator=GeneratorSymbol("ν", index=4),
    )
    assert even_factorization_inputs(
        goal, replace(relation, lhs=Multiple(2, wrong_factor)),
    ) is None
    assert even_factorization_inputs(
        goal, replace(relation, lhs=Multiple(3, relation.lhs.expression)),
    ) is None
    assert even_factorization_inputs(
        goal, replace(relation, rhs=IteratedSuspension(canonical_nu_prime(), 1)),
    ) is None
    assert even_factorization_inputs(goal, replace(relation, relation_type=RelationType.ORDER)) is None


def test_general_rule_accepts_other_degree_compatible_elements() -> None:
    arbitrary = HomotopyElement(
        name="alpha", dimension=3, source=9, target=3,
        generator=GeneratorSymbol("arbitrary"),
    )
    beta = HomotopyElement(
        name="beta", dimension=5, source=11, target=5,
        generator=GeneratorSymbol("arbitrary_half"),
    )
    relation = Relation(
        IteratedSuspension(arbitrary, 2), Multiple(2, beta),
        RelationType.EQUALITY,
    )
    goal = TodaLemma57DoubleSuspensionMembership(arbitrary)
    assert even_factorization_inputs(goal, relation) == (relation,)
    assert len(expand_even_factor_membership(goal, (relation,))) == 1


def test_actual_inference_matching_refuses_missing_parent() -> None:
    from proof import InferenceRule, ProofStep

    equation = cited_lemma54_double_relation()
    goal = TodaLemma57DoubleSuspensionMembership(canonical_nu_prime())
    given = ProofStep(TodaLemma54TypedSource(), (), ProofRule.GIVEN)
    inferred = ProofStep(
        equation, (given,), ProofRule.INFERENCE,
        inference_rule=InferenceRule("test fixture, not a live proof"),
    )
    rule = even_factor_membership_rule(goal, equation)
    assert len(find_inference_matches_for_rule(rule, (inferred,))) == 1
    assert find_inference_matches_for_rule(rule, ()) == ()
    assert find_inference_matches_for_rule(
        rule, (ProofStep(equation, (), ProofRule.GIVEN),),
    ) == ()
