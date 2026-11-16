"""Extract the explicit cited Lemma 5.7 consequence via an inference.

Unlike the conditional generalization of Lemma 5.7, this clause is stated
separately in the lemma itself. No Lemma 5.4 hypothesis is needed to quote it.
The two spellings of nu-prime are reconciled only by checked registered IDs.
"""
from __future__ import annotations

from expression import Composition, GeneratorSymbol, HomotopyElement, Zero
from homotopy_groups import FiniteCyclicGroup, TodaPrimaryGroup, TodaSuspensionMap
from phase165_r14_r6_generic_iso import GeneratorImage
from phase165_r3_recursive_search import GoalExpansion
from phase168_r2_8_3_generator_identity.identity import same_registered_group_presentation
from phase169_r10eq_r1_universal_stable_definition.definition import typed_element_span
from phase175_r3r9_lemma57_explicit_public.source import TodaLemma57ExplicitNuPrimeZero
from proof import InferenceRule, PremisePattern, ProofRule

RULE_NAME = "extract explicit nu-prime zero-suspension clause of Toda Lemma 5.7"


def exact_lemma57_zero_image_goal(goal: object) -> bool:
    """Check the full map, zero, eta_2 and uniquely registered nu-prime ID."""
    if not isinstance(goal, GeneratorImage):
        return False
    expected_map = TodaSuspensionMap(
        TodaPrimaryGroup(6, 2), TodaPrimaryGroup(7, 3),
    )
    if goal.map != expected_map or not isinstance(goal.target_generator, Zero):
        return False
    if not isinstance(goal.source_generator, Composition):
        return False
    eta, nu_prime = goal.source_generator.left, goal.source_generator.right
    if typed_element_span(eta) != (3, 2) or typed_element_span(nu_prime) != (6, 3):
        return False
    eta_cited = HomotopyElement(
        "η₂", 2, source=3, target=2,
        generator=GeneratorSymbol("η", 2),
    )
    nu_cited = HomotopyElement(
        "ν′", 3, source=6, target=3,
        generator=GeneratorSymbol("ν", decoration="′"),
    )
    eta_match = eta == eta_cited or same_registered_group_presentation(
        FiniteCyclicGroup(2, eta), FiniteCyclicGroup(2, eta_cited),
    )
    nu_match = nu_prime == nu_cited or same_registered_group_presentation(
        FiniteCyclicGroup(4, nu_prime), FiniteCyclicGroup(4, nu_cited),
    )
    return bool(eta_match and nu_match)


def lemma57_explicit_zero_rule(goal: GeneratorImage) -> InferenceRule:
    """Require exactly the screened GIVEN for the lemma's explicit clause."""
    if not exact_lemma57_zero_image_goal(goal):
        raise ValueError("R3R9_GOAL_NOT_EXACT_LEMMA57_SPECIAL_CLAUSE")
    source = TodaLemma57ExplicitNuPrimeZero()

    def guard(premises, bindings):
        return (
            len(premises) == 1
            and premises[0].rule is ProofRule.GIVEN
            and not premises[0].premises
            and premises[0].conclusion == source
            and exact_lemma57_zero_image_goal(goal)
        )

    return InferenceRule(
        name=RULE_NAME,
        description=(
            "Read the independently explicit 'in particular' clause "
            "E(eta_2 o nu-prime)=0 from cited Toda Lemma 5.7. "
            "No Lemma 5.4 condition is needed at this citation boundary."
        ),
        premise_patterns=(PremisePattern(
            proof_rule=ProofRule.GIVEN,
            statement_type=TodaLemma57ExplicitNuPrimeZero,
            statement_pattern=source,
        ),),
        conclusion_pattern=goal,
        match_guard=guard,
    )


def expand_cited_lemma57_explicit_zero(
    goal: object, available: tuple[object, ...],
) -> tuple[GoalExpansion, ...]:
    """Offer one backward proposal; do not fabricate a completed ProofStep."""
    if (
        not isinstance(available, tuple)
        or available.count(TodaLemma57ExplicitNuPrimeZero()) != 1
        or not exact_lemma57_zero_image_goal(goal)
    ):
        return ()
    return (GoalExpansion(
        rule=lemma57_explicit_zero_rule(goal),
        subgoals=(TodaLemma57ExplicitNuPrimeZero(),),
    ),)
