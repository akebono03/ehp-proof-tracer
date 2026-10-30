"""Backward symmetry for an independently provable, cited eta–Hopf chain.

This module supplies *obligations*, not inferred ProofSteps or new GIVENs.
Only equality orientations from typed, screened Toda Definition/Propositions
are offered; arbitrary equalities never acquire a symmetric expansion.
"""
from __future__ import annotations

from expression import Composition, MapApplication, Suspension
from map_facts import EHP_H_MAP
from phase165_r3_recursive_search import GoalExpansion
from phase171_r2h_prop22_cited_hopf.source import expand_cited_prop22_right_formula
from phase171_r2i_eta_hopf_bridge.source import (
    eligible_eta_hopf_chains,
    expand_cited_eta_hopf_power,
)
from proof import Relation, RelationType
from relation_rules import equality_symmetry_inference_rule


def reverse_equality(goal: object) -> Relation | None:
    """Make the reverse typed equality, without asserting or proving it."""
    if not isinstance(goal, Relation) or goal.relation_type is not RelationType.EQUALITY:
        return None
    if goal.lhs == goal.rhs:
        return None
    return Relation(goal.rhs, goal.lhs, RelationType.EQUALITY)


def cited_chain_forward_equalities(available: tuple[object, ...]) -> tuple[Relation, ...]:
    """Select only concrete forward steps reachable from screened references.

    These remain unproved goals until canonical recursive search reconstructs
    the original R2I and Proposition 2.2 derivations.
    """
    if not isinstance(available, tuple):
        raise TypeError("screened fixed-statement conclusions must be a tuple")
    found: list[Relation] = []
    for chain in eligible_eta_hopf_chains(available):
        formula = Relation(
            MapApplication(
                EHP_H_MAP,
                Composition(chain.alpha, Suspension(chain.beta)),
            ),
            Composition(
                MapApplication(EHP_H_MAP, chain.alpha),
                Suspension(chain.beta),
            ),
            RelationType.EQUALITY,
        )
        for forward in (
            chain.alpha_composition,
            chain.hopf_composition,
            chain.cited_hopf,
            chain.intermediate,
            chain.beta_composition,
            chain.conclusion,
            formula,
        ):
            original = (
                expand_cited_eta_hopf_power(forward, available)
                + expand_cited_prop22_right_formula(forward, available)
            )
            if len(original) != 1:
                continue
            if forward not in found:
                found.append(forward)
    return tuple(found)


def expand_reverse_cited_eta_hopf_equalities(
    goal: object, available: tuple[object, ...],
) -> tuple[GoalExpansion, ...]:
    """Require the forward equality as a genuine, recursively proved premise.

    No generic symmetry of arbitrary database equalities is introduced.
    Source availability merely permits a search route; it is not evidence.
    """
    if not isinstance(available, tuple):
        raise TypeError("available must be a tuple")
    if not isinstance(goal, Relation) or goal.relation_type is not RelationType.EQUALITY:
        return ()
    forwards = tuple(
        forward for forward in cited_chain_forward_equalities(available)
        if reverse_equality(forward) == goal
    )
    if len(forwards) != 1:
        return ()
    return (GoalExpansion(equality_symmetry_inference_rule(), (forwards[0],)),)
