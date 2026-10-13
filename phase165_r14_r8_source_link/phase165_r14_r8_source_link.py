"""Toda (5.1) and Prop.5.1 candidate premises for registered backward search.

Source mapping is not mathematical certification. The searcher must resolve
all three premises from verified, linked registry assertions independently.
"""
from __future__ import annotations
from dataclasses import dataclass

from homotopy_groups import TodaPrimaryGroup
from hopf_facts import ETA_2, IOTA_3, ETA_2_HOPF_INVARIANT_FACT
from phase165_r14_r2_toda51 import TODA_51_SCHEMAS, instantiate_toda51_clause
from phase165_r14_r3_source_scope import collect_toda51_scope
from phase165_r14_r6_generic_iso import GeneratorImage
from phase165_r14_r7_map_discovery import (
    discover_hopf_map_candidates, expand_discovered_group_goal,
)
from proof import Relation, RelationType


@dataclass(frozen=True)
class UnverifiedSourceCandidate:
    claim: object
    locator: str
    source_key: str
    status: str = "SOURCE_MAPPED_NOT_CERTIFIED"


def find_pi33_source_candidate(goal: object, bridge: object) -> tuple[UnverifiedSourceCandidate, ...]:
    """Bind diagonal group schema to archived (5.1) without granting eligibility."""
    scope = collect_toda51_scope(bridge)
    if scope["adjacent_source_status"] != "USER_SUPPLIED_NOT_ARCHIVE_VERIFIED":
        raise ValueError("unexpected adjacent source provenance")
    found = []
    for candidate in discover_hopf_map_candidates(goal):
        group = candidate.map.target_group
        if (type(group.group_dimension) is not int
                or group.group_dimension != group.sphere_dimension):
            continue
        claim = instantiate_toda51_clause(TODA_51_SCHEMAS[1], group.sphere_dimension)
        found.append(UnverifiedSourceCandidate(claim, "(5.1)",
                                               "pi_n_n_cyclic"))
    return tuple(found)


def find_eta2_hopf_source_candidate(goal: object) -> tuple[UnverifiedSourceCandidate, ...]:
    """Map existing Hopf fact with its ACTUAL Prop.5.1 locator, not (5.1)."""
    matches = []
    for candidate in discover_hopf_map_candidates(goal):
        h = candidate.map
        fact = ETA_2_HOPF_INVARIANT_FACT
        if (goal.rhs.generator == ETA_2
                and h.source_group == TodaPrimaryGroup(3, 2)
                and h.target_group == TodaPrimaryGroup(3, 3)
                and fact.expression == ETA_2 and fact.value == IOTA_3
                and fact.source.locator == "Proposition 5.1"):
            matches.append(UnverifiedSourceCandidate(
                GeneratorImage(h, ETA_2, IOTA_3),
                "Proposition 5.1", "H(eta_2)=iota_3",
            ))
    return tuple(matches)


def expand_source_mapped_group_goal(goal: object, bridge: object):
    """Provide obligations only; ordinary registered prover remains fail-closed."""
    groups = find_pi33_source_candidate(goal, bridge)
    images = find_eta2_hopf_source_candidate(goal)
    return expand_discovered_group_goal(
        goal,
        generator_images=tuple(item.claim for item in images),
        target_group_claims=tuple(item.claim for item in groups),
    )


def audit_source_link(goal: object, bridge: object) -> dict:
    groups = find_pi33_source_candidate(goal, bridge)
    images = find_eta2_hopf_source_candidate(goal)
    expanded = expand_source_mapped_group_goal(goal, bridge)
    return {
        "phase": "165 R14-R8",
        "goal": repr(goal),
        "source_group_candidates": len(groups),
        "source_generator_image_candidates": len(images),
        "source_group_locator": groups[0].locator if groups else None,
        "generator_image_locator": images[0].locator if images else None,
        "root_expansions": len(expanded),
        "root_subgoals": [repr(x) for e in expanded for x in e.subgoals],
        "source_certified": False,
        "eligible_new_leaves": 0,
        "proof_steps_created": 0,
        "legacy_proof_used": False,
        "full_pytest_run": False,
        "status": "ROOT_OBLIGATIONS_MAPPED_NOT_CERTIFIED" if expanded else "SOURCE_MAPPING_INCOMPLETE",
    }
