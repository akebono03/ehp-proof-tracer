"""General backward provider: a proved finite cyclic summand has order m.

Every proposal is conditional on proving its complete group presentation.
Only an earlier, explicit DB prior or a source-screened/previously completed
presentation may be proposed. This provider never creates ProofSteps or GIVEN.
"""
from __future__ import annotations

from collections.abc import Callable

from homotopy_groups import TodaPrimaryGroup
from phase165_r3_recursive_search import GoalExpansion
from phase169_r10e4_ordered_db_prior.db_prior import (
    exact_prior_database_result, group_coordinates, precedes_db_goal,
)
from phase175_r4r5_eta7_annihilator_isolated.rule import (
    expand_finite_cyclic_order_zero, order_zero_premise,
)
from proof import ProofRule, Relation, RelationType
from unified_statement_registry import AssertionOrigin


def eligible_order_zero_sources(
    goal: object, *, bridge: object, proof_target: object,
    prior_conclusions: tuple = (),
) -> tuple[Relation, ...]:
    """Find source-bound candidates; their ProofSteps remain search obligations.

    The root's original typed group statement is the only proof-use order
    anchor. DB rows for the source group are re-read; stable fallback and
    unscreened citations are never accepted as evidence.
    """
    if not isinstance(prior_conclusions, tuple):
        raise TypeError("prior_conclusions must be a tuple")
    root = group_coordinates(proof_target)
    requested = order_zero_premise(goal)
    if root is None or requested is None:
        return ()
    source = group_coordinates(requested)
    if source is None or not precedes_db_goal(*source, *root):
        return ()

    candidates: list[Relation] = []

    def include(statement: object) -> None:
        if (isinstance(statement, Relation)
                and statement.relation_type is RelationType.EQUALITY
                and group_coordinates(statement) == source
                and order_zero_premise(goal, statement) == statement
                and statement not in candidates):
            candidates.append(statement)

    # These are completed, ordered internal proof conclusions, never created here.
    for statement in prior_conclusions:
        include(statement)

    # Only citation-screened fixed source statements may be used as candidates.
    registry = getattr(bridge, "registry", None)
    links = getattr(bridge, "proof_links", ())
    if registry is not None:
        for link in links:
            step = getattr(link, "step", None)
            if step is None or step.rule is not ProofRule.GIVEN:
                continue
            assertion = registry.assertion(link.assertion_id)
            if (assertion.origin is AssertionOrigin.FIXED_STATEMENT
                    and assertion.content == step.conclusion):
                include(step.conclusion)

    # The original exact-DB prior rule verifies/adopts this source in the
    # ordinary resolver; merely discovering the row is never a ProofStep.
    include(exact_prior_database_result(*source))
    return tuple(candidates)


def build_public_order_zero_provider(
    *, bridge: object, proof_target: object, prior_conclusions: tuple = (),
) -> Callable[[object], tuple[GoalExpansion, ...]]:
    """Expose one generic inference to every shared backward-search root.

    The canonical resolver rechecks an actual earlier DB row or accepted source
    ProofStep, then applies the R4R5R2 InferenceRule. No target-specific branch.
    """
    if not isinstance(prior_conclusions, tuple):
        raise TypeError("prior_conclusions must be a tuple")

    def expand(goal: object) -> tuple[GoalExpansion, ...]:
        candidates = eligible_order_zero_sources(
            goal, bridge=bridge, proof_target=proof_target,
            prior_conclusions=prior_conclusions,
        )
        if not candidates:
            return ()
        return expand_finite_cyclic_order_zero(goal, candidates)

    return expand
