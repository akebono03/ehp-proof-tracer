"""Reuse screened presentations to select finite-cardinality obligations."""
from phase165_r14_r6_generic_iso import MapInjective
from phase177_r15_finite_cyclic_delta_injective_public.provider import presentation_candidates
from phase178_r6_finite_group_cardinality_isolated.rule import cardinality_from_presentation
from phase178_r8_finite_group_surjective_injective_isolated.rule import (
    expand_finite_surjective_injective, valid_finite_group_map,
)


def candidate_orders(group, presentations):
    orders = []
    for claim in presentations(group):
        cardinality = cardinality_from_presentation(claim)
        if (cardinality is not None and cardinality.group == group
                and cardinality.order not in orders):
            orders.append(cardinality.order)
    return tuple(orders)


def expand_from_presentations(goal, presentations):
    if type(goal) is not MapInjective or not valid_finite_group_map(goal.map):
        return ()
    source_orders = candidate_orders(goal.map.source_group, presentations)
    if not source_orders:
        return ()
    target_orders = candidate_orders(goal.map.target_group, presentations)
    return tuple(option for order in source_orders if order in target_orders
                 for option in expand_finite_surjective_injective(goal, order))


def build_public_finite_surjective_injective_provider(*, bridge, proof_target):
    def presentations(group):
        return presentation_candidates(group, bridge=bridge, proof_target=proof_target)

    def expand(goal):
        return expand_from_presentations(goal, presentations)

    return expand
