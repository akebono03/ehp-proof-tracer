"""Typed candidate discovery for free cyclic group goals (no certified premises)."""
from __future__ import annotations

from dataclasses import dataclass

from homotopy_groups import FreeCyclicGroup, TodaHopfInvariantMap, TodaPrimaryGroup
from phase165_r3_recursive_search import GoalExpansion
from phase165_r14_r6_generic_iso import (
    GeneratorImage,
    MapIsomorphism,
    free_cyclic_transport_rule,
)
from proof import InferenceRule, PremisePattern, Relation, RelationType


@dataclass(frozen=True)
class CandidateMap:
    map: TodaHopfInvariantMap
    status: str = "STRUCTURAL_CANDIDATE_NOT_VERIFIED"


def discover_hopf_map_candidates(goal: object) -> tuple[CandidateMap, ...]:
    """Enumerate EHP Hopf map signatures by dimensions, not group-specific cases.

    A candidate map is not a mathematical assertion or an eligible proof leaf.
    """
    if not isinstance(goal, Relation) or goal.relation_type is not RelationType.EQUALITY:
        return ()
    group = goal.lhs
    if not isinstance(group, TodaPrimaryGroup) or not isinstance(goal.rhs, FreeCyclicGroup):
        return ()
    q, n = group.group_dimension, group.sphere_dimension
    if type(q) is not int or type(n) is not int or n < 2 or q < n:
        return ()
    return (CandidateMap(TodaHopfInvariantMap(
        source_group=group,
        target_group=TodaPrimaryGroup(group_dimension=q, sphere_dimension=2*n-1),
    )),)


def _check_inverse_transport(premises):
    iso, target, image = (step.conclusion for step in premises)
    return (
        iso.map == image.map
        and getattr(iso.map, 'source_group', None) is not None
        and iso.map.target_group == target.lhs
        and target.relation_type is RelationType.EQUALITY
        and isinstance(target.rhs, FreeCyclicGroup)
        and target.rhs.generator == image.target_generator
    )


def _build_inverse_transport(premises):
    iso, target, image = (step.conclusion for step in premises)
    return Relation(
        lhs=iso.map.source_group,
        rhs=FreeCyclicGroup(generator=image.source_generator),
        relation_type=RelationType.EQUALITY,
    )


def inverse_free_cyclic_transport_rule() -> InferenceRule:
    """Transport target group's generator back across a proved isomorphism."""
    return InferenceRule(
        name='generic inverse free cyclic transport',
        premise_patterns=(
            PremisePattern(statement_type=MapIsomorphism),
            PremisePattern(statement_type=Relation, relation_type=RelationType.EQUALITY),
            PremisePattern(statement_type=GeneratorImage),
        ),
        match_guard=_check_inverse_transport,
        conclusion_builder=_build_inverse_transport,
    )


def expand_discovered_group_goal(
    goal: object,
    *,
    generator_images: tuple[GeneratorImage, ...] = (),
    target_group_claims: tuple[Relation, ...] = (),
) -> tuple[GoalExpansion, ...]:
    """Use independently supplied typed premise candidates; do not certify them.

    Subgoals must later be resolved only by the standard registry prover.
    """
    if not isinstance(generator_images, tuple) or not isinstance(target_group_claims, tuple):
        raise TypeError('candidate catalogs must be tuples')
    results = []
    for candidate in discover_hopf_map_candidates(goal):
        h = candidate.map
        for image in generator_images:
            if not isinstance(image, GeneratorImage):
                raise TypeError('image catalog must contain GeneratorImage')
            if image.map != h or image.source_generator != goal.rhs.generator:
                continue
            for target in target_group_claims:
                if not isinstance(target, Relation):
                    raise TypeError('target claims must be Relation')
                if (
                    target.lhs == h.target_group
                    and target.relation_type is RelationType.EQUALITY
                    and isinstance(target.rhs, FreeCyclicGroup)
                    and target.rhs.generator == image.target_generator
                ):
                    results.append(GoalExpansion(
                        inverse_free_cyclic_transport_rule(),
                        (MapIsomorphism(h), target, image),
                    ))
    return tuple(results)


def audit_hopf_discovery(goal: object) -> dict:
    candidates = discover_hopf_map_candidates(goal)
    return {
        'phase': '165 R14-R7',
        'goal': repr(goal),
        'hopf_structural_candidate_count': len(candidates),
        'candidate_maps': [repr(candidate.map) for candidate in candidates],
        'candidate_status': 'NOT_CERTIFIED',
        'root_expansions_without_registered_premises': len(expand_discovered_group_goal(goal)),
        'proof_steps_created': 0,
        'verified_generator_images': 0,
        'full_pytest_run': False,
        'status': 'HOPF_MAP_CANDIDATE_FOUND_PREMISES_MISSING' if candidates else 'NO_MAP_CANDIDATE',
    }
