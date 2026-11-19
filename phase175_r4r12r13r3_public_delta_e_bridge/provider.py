"""Public conditional bridge for R13R2 inference rules; no new proof leaves.

All literature and group premises remain backward subgoals to be resolved by
normal source-first proof search. The provider does not assert any goal.
"""
from __future__ import annotations

from homotopy_groups import FreeCyclicGroup, TodaDeltaMap, TodaPrimaryGroup
from phase165_r14_r6_generic_iso import MapInjective
from phase165_r3_recursive_search import GoalExpansion
from phase169_r10e4_ordered_db_prior.db_prior import exact_prior_database_result
from phase175_r4r10_cited_58_prop25_public.source import (
    CitedToda58SignedDelta,
    canonical_toda58,
)
from phase175_r4r12r13r2_delta_injective_e_surjective.rule import (
    expand_delta_injective_from_free_coordinate,
    expand_e_surjective_from_delta_injective,
)
from proof import ProofRule, Relation, RelationType
from unified_statement_registry import AssertionOrigin


def screened_toda58_available(bridge: object) -> bool:
    """Require an actual matching, citation-eligible GIVEN in the bridge."""
    registry = getattr(bridge, "registry", None)
    links = getattr(bridge, "proof_links", None)
    if registry is None or links is None:
        return False
    witnesses = []
    for link in links:
        step = getattr(link, "step", None)
        if step is None or step.rule is not ProofRule.GIVEN or step.premises:
            continue
        assertion = registry.assertion(link.assertion_id)
        claim = step.conclusion
        if (
            assertion.origin is AssertionOrigin.FIXED_STATEMENT
            and assertion.content == claim
            and type(claim) is CitedToda58SignedDelta
            and claim.locator == "(5.8)"
            and claim.statement == canonical_toda58()
        ):
            witnesses.append(claim)
    return len(witnesses) == 1


def delta_free_coordinate_proposals(
    goal: object,
    *,
    cited58: bool,
    database_lookup=exact_prior_database_result,
) -> tuple[GoalExpansion, ...]:
    """Offer an unproved route only for a uniquely cited signed source formula.

    π₉⁹ is a *goal* to be proved from a separate citation, never a fabricated
    given. π₇⁴ is also a goal; its existing DB row is not promoted here.
    """
    if not cited58 or not isinstance(goal, MapInjective) or not isinstance(goal.map, TodaDeltaMap):
        return ()
    signed = canonical_toda58()
    if goal.map != signed.map:
        return ()
    source = Relation(
        lhs=goal.map.source_group,
        rhs=FreeCyclicGroup(signed.element),
        relation_type=RelationType.EQUALITY,
    )
    # DB n=4,k=3 is an earlier group, not the queried π₉⁵ target.
    target = database_lookup(4, 3)
    if not isinstance(target, Relation) or target.lhs != TodaPrimaryGroup(7, 4):
        return ()
    return expand_delta_injective_from_free_coordinate(goal, source, target, signed)


def build_public_delta_e_provider(bridge: object):
    """Connect existing R13R2 rules without introducing new mathematical rules."""
    has_source = screened_toda58_available(bridge)

    def expand(goal: object) -> tuple[GoalExpansion, ...]:
        return (
            delta_free_coordinate_proposals(goal, cited58=has_source)
            + expand_e_surjective_from_delta_injective(goal)
        )

    return expand
