"""Generic Lemma 5.7: proved doubled-suspension membership implies zero E-image.

The source statement is a single earlier citation. Membership is an
independent INFERENCE obligation and is never created as a GIVEN or assumed
because the element happens to be nu-prime.
"""
from __future__ import annotations

from dataclasses import dataclass

from expression import Composition, GeneratorSymbol, HomotopyElement, Zero
from homotopy_groups import FiniteCyclicGroup, TodaPrimaryGroup, TodaSuspensionMap
from phase165_r14_r6_generic_iso import GeneratorImage
from phase165_r3_recursive_search import GoalExpansion
from phase168_r2_8_3_generator_identity.identity import same_registered_group_presentation
from phase169_r10eq_r1_universal_stable_definition.definition import typed_element_span
from phase175_r3r6_lemma57_general.source import TodaLemma57GeneralCriterion
from proof import InferenceRule, PremisePattern, ProofRule

RULE_NAME = "Toda Lemma 5.7 general double-suspension criterion"


@dataclass(frozen=True)
class TodaLemma57DoubleSuspensionMembership:
    """Independent goal: E^2(alpha) belongs to 2 iota_5 o pi_(i+2)^5."""
    alpha: object


def lemma57_criterion_inputs(goal: object):
    """Check an arbitrary typed alpha in pi_i^3 and eta_2 o alpha in pi_i^2."""
    if not isinstance(goal, GeneratorImage):
        return None
    e = goal.map
    if not isinstance(e, TodaSuspensionMap) or not isinstance(goal.target_generator, Zero):
        return None
    if not isinstance(goal.source_generator, Composition):
        return None
    generator = goal.source_generator
    eta, alpha = generator.left, generator.right
    if not isinstance(eta, HomotopyElement):
        return None
    expected_eta = HomotopyElement(
        name="η₂", dimension=2, source=3, target=2,
        generator=GeneratorSymbol(family="η", index=2),
    )
    # Registered identity is a notation check, not a claim that either
    # displayed finite-cyclic group has been mathematically established.
    eta_identity = eta == expected_eta or same_registered_group_presentation(
        FiniteCyclicGroup(2, eta), FiniteCyclicGroup(2, expected_eta),
    )
    if not eta_identity:
        return None
    domain = e.source_group
    target = e.target_group
    if not isinstance(domain, TodaPrimaryGroup) or not isinstance(target, TodaPrimaryGroup):
        return None
    index = domain.group_dimension
    if (type(index) is not int or index < 3
            or domain != TodaPrimaryGroup(index, 2)
            or target != TodaPrimaryGroup(index + 1, 3)
            or typed_element_span(alpha) != (index, 3)
            or typed_element_span(generator) != (index, 2)):
        return None
    return TodaLemma57GeneralCriterion(), TodaLemma57DoubleSuspensionMembership(alpha)


def lemma57_zero_generator_rule(goal: GeneratorImage) -> InferenceRule:
    """Only a cited general GIVEN and a proved membership can justify E=0."""
    required = lemma57_criterion_inputs(goal)
    if required is None:
        raise ValueError("R3R6 invalid Lemma 5.7 zero-generator goal")

    def guard(premises, bindings):
        return (
            len(premises) == 2
            and premises[0].rule is ProofRule.GIVEN
            and premises[1].rule is ProofRule.INFERENCE
            and bool(premises[1].premises)
            and tuple(p.conclusion for p in premises) == required
            and lemma57_criterion_inputs(goal) == required
        )

    return InferenceRule(
        name=RULE_NAME,
        description=(
            "Toda Lemma 5.7: for alpha in pi_i(S^3), if the independently "
            "proved double suspension lies in 2 iota_5 o pi_(i+2)(S^5), "
            "then E(eta_2 o alpha)=0."
        ),
        premise_patterns=(
            PremisePattern(proof_rule=ProofRule.GIVEN, statement_type=TodaLemma57GeneralCriterion),
            PremisePattern(
                proof_rule=ProofRule.INFERENCE,
                statement_type=TodaLemma57DoubleSuspensionMembership,
                statement_pattern=required[1],
            ),
        ),
        match_guard=guard,
        conclusion_pattern=goal,
    )


def expand_cited_lemma57_zero_generator(goal: object, available: tuple[object, ...]):
    """Return only a backward proposal, never a ready-to-use proof step."""
    if not isinstance(available, tuple) or available.count(TodaLemma57GeneralCriterion()) != 1:
        return ()
    required = lemma57_criterion_inputs(goal)
    if required is None:
        return ()
    return (GoalExpansion(lemma57_zero_generator_rule(goal), required),)
