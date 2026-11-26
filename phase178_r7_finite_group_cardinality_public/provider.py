"""Offer ordinary backward obligations from screened group presentations."""
from phase171_r2j_r4_r6_middle_cardinality.source import FiniteGroupCardinality
from phase177_r15_finite_cyclic_delta_injective_public.provider import presentation_candidates
from phase178_r6_finite_group_cardinality_isolated.rule import (
    expand_finite_cardinality_from_presentation,
)


def expand_from_presentations(goal, presentations):
    if type(goal) is not FiniteGroupCardinality:
        return ()
    options = []
    for claim in presentations(goal.group):
        for option in expand_finite_cardinality_from_presentation(goal, claim):
            if not any(old.rule.name == option.rule.name and old.subgoals == option.subgoals
                       for old in options):
                options.append(option)
    return tuple(options)


def build_public_finite_cardinality_provider(*, bridge, proof_target):
    def presentations(group):
        return presentation_candidates(group, bridge=bridge, proof_target=proof_target)

    def expand(goal):
        return expand_from_presentations(goal, presentations)

    return expand
