"""Source-first public access to the EXISTING general two-summand EHP quotient rule.

Database rows are used only to propose earlier group-structure subgoals.
No proof, Delta value, E-image, surjectivity or group conclusion is asserted.
Two conditional alternatives are intentionally retained: the actual Delta
image must be independently proved before one can complete the quotient.
"""
from __future__ import annotations

from collections.abc import Callable

from homotopy_groups import (
    DirectSumGroup,
    FiniteCyclicGroup,
    TodaDeltaMap,
    TodaPrimaryGroup,
    TodaSuspensionMap,
)
from phase165_r12_r2_quotient_rules import CyclicStructureStatement
from phase165_r14_r6_generic_iso import GeneratorImage
from phase165_r3_recursive_search import GoalExpansion
from phase169_r10e4_ordered_db_prior.db_prior import (
    exact_prior_database_result,
    precedes_db_goal,
)
from phase175_r4r3_two_summand_quotient.rule import (
    expand_two_summand_quotient,
)
from proof import Relation, RelationType


def ordered_summand_inputs(
    goal: object,
    *,
    proof_target: object,
    database_lookup: Callable[[int, int], object] = exact_prior_database_result,
) -> tuple[Relation, Relation] | None:
    """Retrieve only two explicit, genuinely earlier typed DB candidates.

    The rows themselves are NOT ProofSteps. The canonical resolver must still
    admit and verify their independent earlier provenance during search.
    This function has no target-specific dimension branch or generator label.
    """
    if (
        type(goal) is not CyclicStructureStatement
        or type(goal.group) is not TodaPrimaryGroup
        or type(goal.order) is not int
        or goal.order != 2
        or type(proof_target) is not Relation
        or proof_target.relation_type is not RelationType.EQUALITY
        or proof_target.lhs != goal.group
        or proof_target.rhs != FiniteCyclicGroup(2, goal.generator)
    ):
        return None
    q, n = goal.group.group_dimension, goal.group.sphere_dimension
    if not all(type(x) is int for x in (q, n)) or n < 3 or q <= n:
        return None
    middle_n, middle_k = n - 1, q - n
    delta_n, delta_k = 2 * n - 1, (q + 1) - (2 * n - 1)
    if (
        middle_k < 0 or delta_k < 0
        or not precedes_db_goal(middle_n, middle_k, n, q - n)
        or not precedes_db_goal(delta_n, delta_k, n, q - n)
    ):
        return None
    middle = database_lookup(middle_n, middle_k)
    source = database_lookup(delta_n, delta_k)
    if (
        type(middle) is not Relation
        or middle.relation_type is not RelationType.EQUALITY
        or middle.lhs != TodaPrimaryGroup(q - 1, n - 1)
        or type(middle.rhs) is not DirectSumGroup
        or type(middle.rhs.summands) is not tuple
        or len(middle.rhs.summands) != 2
        or any(type(part) is not FiniteCyclicGroup or part.order != 2
               for part in middle.rhs.summands)
        or middle.rhs.summands[0].generator == middle.rhs.summands[1].generator
        or type(source) is not Relation
        or source.relation_type is not RelationType.EQUALITY
        or source.lhs != TodaPrimaryGroup(q + 1, 2 * n - 1)
        or type(source.rhs) is not FiniteCyclicGroup
        or source.rhs.order != 2
    ):
        return None
    return middle, source


def expand_public_two_summand_quotient(
    goal: object,
    *,
    proof_target: object,
    database_lookup: Callable[[int, int], object] = exact_prior_database_result,
) -> tuple[GoalExpansion, ...]:
    """Offer both valid conditional quotient routes, without proving either.

    The published source Delta value and the suspension image must be proved
    by separate typed rules. The correct killed summand is NOT chosen from
    the requested result; both possibilities remain conditional subgoals.
    """
    sources = ordered_summand_inputs(
        goal, proof_target=proof_target, database_lookup=database_lookup,
    )
    if sources is None:
        return ()
    middle, delta_source = sources
    source_group, middle_group = delta_source.lhs, middle.lhs
    delta_map = TodaDeltaMap(source_group, middle_group)
    e_map = TodaSuspensionMap(middle_group, goal.group)
    parts = middle.rhs.summands
    results: list[GoalExpansion] = []
    for killed_index in (0, 1):
        killed = parts[killed_index].generator
        survivor = parts[1 - killed_index].generator
        delta_image = GeneratorImage(
            map=delta_map,
            source_generator=delta_source.rhs.generator,
            target_generator=killed,
        )
        e_image = GeneratorImage(
            map=e_map,
            source_generator=survivor,
            target_generator=goal.generator,
        )
        candidates = expand_two_summand_quotient(
            goal, middle, delta_source, delta_image, e_image,
        )
        for candidate in candidates:
            if candidate not in results:
                results.append(candidate)
    return tuple(results)


def build_public_two_summand_quotient_provider(*, proof_target: object):
    """Inject an ordinary backward candidate into the shared provider chain."""
    def expand(goal: object) -> tuple[GoalExpansion, ...]:
        return expand_public_two_summand_quotient(
            goal, proof_target=proof_target,
        )

    return expand
