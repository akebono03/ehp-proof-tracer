"""Isolated source extraction and degree-generic even-factor membership.

The source extraction is the literal Lemma 5.4 identity, not a new theorem.
The independent mathematical implication works for any typed alpha in pi_i^3:
E^2(alpha) = 2 beta, beta in pi_(i+2)^5, implies the Lemma 5.7 hypothesis.
No result is made a GIVEN by these backward expansions.
"""
from __future__ import annotations

from expression import GeneratorSymbol, HomotopyElement, IteratedSuspension, Multiple
from homotopy_groups import FiniteCyclicGroup
from phase165_r3_recursive_search import GoalExpansion
from phase168_r2_8_3_generator_identity.identity import same_registered_group_presentation
from phase169_r10eq_r1_universal_stable_definition.definition import typed_element_span
from phase173_r4_r1_lemma54_source_bridge.source import (
    TodaLemma54TypedSource,
    canonical_hopf_relation,
)
from phase175_r3r6_lemma57_general.rule import TodaLemma57DoubleSuspensionMembership
from proof import (
    InferenceRule,
    LiteratureReference,
    PremisePattern,
    ProofRule,
    Relation,
    RelationType,
)

SOURCE_RULE_NAME = "Toda Lemma 5.4 verified double-suspension clause extraction"
FACTOR_RULE_NAME = "even double-suspension factor implies Lemma 5.7 membership"


def canonical_nu_prime() -> HomotopyElement:
    """Use the already source-registered (5.3) nu-prime representative."""
    return HomotopyElement(
        name="ν′", dimension=3, source=6, target=3,
        generator=GeneratorSymbol(family="ν", decoration="′"),
    )


def cited_lemma54_double_relation() -> Relation:
    """Encode precisely 2 E nu_4 = E^2 nu-prime from Lemma 5.4."""
    nu4 = canonical_hopf_relation().lhs.expression
    nu_prime = canonical_nu_prime()
    return Relation(
        lhs=Multiple(2, IteratedSuspension(nu4, 1)),
        rhs=IteratedSuspension(nu_prime, 2),
        relation_type=RelationType.EQUALITY,
    )


def _same_typed_alpha_identity(left: object, right: object) -> bool:
    """Allow only an identical typed class or a uniquely registered generator ID.

    FiniteCyclicGroup here is an identity-matching wrapper; no group order is
    inferred or used as a theorem by this check.
    """
    if typed_element_span(left) != typed_element_span(right):
        return False
    if left == right:
        return True
    if typed_element_span(left) != (6, 3):
        return False
    return same_registered_group_presentation(
        FiniteCyclicGroup(4, left), FiniteCyclicGroup(4, right),
    )


def lemma54_double_rule(goal: Relation) -> InferenceRule:
    """Require an actual screened Lemma 5.4 GIVEN to extract the cited clause."""
    if goal != cited_lemma54_double_relation():
        raise ValueError("R3R7 Lemma 5.4 double relation does not match source")
    source = TodaLemma54TypedSource()

    def guard(premises, bindings):
        return (
            len(premises) == 1
            and premises[0].rule is ProofRule.GIVEN
            and premises[0].conclusion == source
            and cited_lemma54_double_relation() == goal
        )

    return InferenceRule(
        name=SOURCE_RULE_NAME,
        description=(
            "Extract only 2E(nu_4)=E^2(nu-prime) from the independently "
            "screened, full cited Lemma 5.4. No direct group GIVEN."
        ),
        premise_patterns=(PremisePattern(
            proof_rule=ProofRule.GIVEN,
            statement_type=TodaLemma54TypedSource,
            statement_pattern=source,
        ),),
        conclusion_pattern=goal,
        match_guard=guard,
        literature_reference=LiteratureReference(
            label="Toda Lemma 5.4", locator="Lemma 5.4",
        ),
    )


def expand_cited_lemma54_double(
    goal: object, available: tuple[object, ...],
) -> tuple[GoalExpansion, ...]:
    """Do not offer an extracted relation without one exact screened source."""
    if (not isinstance(available, tuple)
            or goal != cited_lemma54_double_relation()
            or available.count(TodaLemma54TypedSource()) != 1):
        return ()
    return (GoalExpansion(lemma54_double_rule(goal), (TodaLemma54TypedSource(),)),)


def even_factorization_inputs(
    goal: object, relation: object,
) -> tuple[Relation] | None:
    """Check the general equation E^2(alpha)=2 beta, either direction.

    The formal source must have type pi_i^3 and beta must have type
    pi_(i+2)^5. Only a checked equality, not the assertion of beta's
    existence, supplies this evidence.
    """
    if not isinstance(goal, TodaLemma57DoubleSuspensionMembership):
        return None
    alpha = goal.alpha
    span = typed_element_span(alpha)
    if span is None or span[1] != 3 or span[0] < 3:
        return None
    i = span[0]
    if not isinstance(relation, Relation) or relation.relation_type is not RelationType.EQUALITY:
        return None
    for left, right in ((relation.lhs, relation.rhs), (relation.rhs, relation.lhs)):
        if not (isinstance(left, Multiple) and left.coefficient == 2
                and typed_element_span(left.expression) == (i + 2, 5)
                and isinstance(right, IteratedSuspension)
                and right.exponent == 2
                and _same_typed_alpha_identity(right.expression, alpha)):
            continue
        return (relation,)
    return None


def even_factor_membership_rule(
    goal: TodaLemma57DoubleSuspensionMembership, relation: Relation,
) -> InferenceRule:
    """Make a genuine INFERENCE from the earlier proved doubled equality."""
    required = even_factorization_inputs(goal, relation)
    if required is None:
        raise ValueError("R3R7 invalid double-suspension factorization")

    def guard(premises, bindings):
        return (
            len(premises) == 1
            and premises[0].rule is ProofRule.INFERENCE
            and bool(premises[0].premises)
            and premises[0].conclusion == relation
            and even_factorization_inputs(goal, relation) == required
        )

    return InferenceRule(
        name=FACTOR_RULE_NAME,
        description=(
            "For alpha in pi_i(S^3), a proved equality E^2(alpha)=2 beta "
            "with beta in pi_(i+2)(S^5) gives E^2(alpha) in "
            "2 iota_5 o pi_(i+2)(S^5); the identity iota_5 acts trivially."
        ),
        premise_patterns=(PremisePattern(
            proof_rule=ProofRule.INFERENCE,
            statement_type=Relation,
            relation_type=RelationType.EQUALITY,
            statement_pattern=relation,
        ),),
        conclusion_pattern=goal,
        match_guard=guard,
    )


def expand_even_factor_membership(
    goal: object, candidate_relations: tuple[object, ...],
) -> tuple[GoalExpansion, ...]:
    """General backward rule: only concrete, typed factorization candidates."""
    if not isinstance(candidate_relations, tuple):
        return ()
    result: list[GoalExpansion] = []
    for relation in candidate_relations:
        if even_factorization_inputs(goal, relation) is None:
            continue
        if any(existing.subgoals == (relation,) for existing in result):
            continue
        result.append(GoalExpansion(
            even_factor_membership_rule(goal, relation), (relation,),
        ))
    return tuple(result)
