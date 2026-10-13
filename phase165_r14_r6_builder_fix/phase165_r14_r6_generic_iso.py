"""Generic map isomorphism and cyclic-structure transport inference rules.

Rules do not assert EHP exactness or provide registered proof leaves.
"""
from __future__ import annotations
from dataclasses import dataclass
from typing import Any

from proof import InferenceRule, PremisePattern, ProofStep, find_inference_matches_for_rule
from phase165_r3_recursive_search import GoalExpansion
from homotopy_groups import FreeCyclicGroup
from proof import Relation, RelationType


@dataclass(frozen=True)
class MapInjective:
    map: Any


@dataclass(frozen=True)
class MapSurjective:
    map: Any


@dataclass(frozen=True)
class MapIsomorphism:
    map: Any


@dataclass(frozen=True)
class GeneratorImage:
    map: Any
    source_generator: Any
    target_generator: Any


def _same_map(premises, bindings):
    return premises[0].conclusion.map == premises[1].conclusion.map


def _build_isomorphism(premises):
    return MapIsomorphism(premises[0].conclusion.map)


def map_isomorphism_rule():
    return InferenceRule(
        name="generic injective and surjective imply isomorphism",
        premise_patterns=(
            PremisePattern(statement_type=MapInjective),
            PremisePattern(statement_type=MapSurjective),
        ),
        match_guard=_same_map,
        conclusion_builder=_build_isomorphism,
    )


def _valid_transfer(premises, bindings):
    iso, source, image = (item.conclusion for item in premises)
    return (
        iso.map == image.map
        and getattr(iso.map, "source_group", None) == source.lhs
        and getattr(iso.map, "target_group", None) is not None
        and source.relation_type is RelationType.EQUALITY
        and isinstance(source.rhs, FreeCyclicGroup)
        and source.rhs.generator == image.source_generator
    )


def _build_transfer(premises):
    iso, source, image = (item.conclusion for item in premises)
    return Relation(
        lhs=iso.map.target_group,
        rhs=FreeCyclicGroup(generator=image.target_generator),
        relation_type=RelationType.EQUALITY,
    )


def free_cyclic_transport_rule():
    return InferenceRule(
        name="generic free cyclic structure transported over isomorphism",
        premise_patterns=(
            PremisePattern(statement_type=MapIsomorphism),
            PremisePattern(statement_type=Relation, relation_type=RelationType.EQUALITY),
            PremisePattern(statement_type=GeneratorImage),
        ),
        match_guard=_valid_transfer,
        conclusion_builder=_build_transfer,
    )


def expand_generic_iso_goal(goal: object) -> tuple[GoalExpansion, ...]:
    """Generic backward expansion. Never construct theorem leaves."""
    if isinstance(goal, MapIsomorphism):
        return (GoalExpansion(
            map_isomorphism_rule(),
            (MapInjective(goal.map), MapSurjective(goal.map)),
        ),)
    if (isinstance(goal, Relation)
            and goal.relation_type is RelationType.EQUALITY
            and isinstance(goal.rhs, FreeCyclicGroup)):
        # An isomorphism cannot be inferred from a group-structure goal alone.
        # The map and its source generator must be supplied by an independently
        # registered rule/candidate catalog. Returning () is intentionally safe.
        return ()
    return ()


def audit_generic_iso(goal) -> dict:
    options = expand_generic_iso_goal(goal)
    return {
        "phase": "165 R14-R6",
        "goal": repr(goal),
        "generic_rules_defined": 2,
        "root_expansions": len(options),
        "root_status": "UNRESOLVED_NEEDS_REGISTERED_MAP_AND_PREMISES" if not options else "EXPANSION_AVAILABLE",
        "ehp_exactness_evidence_added": False,
        "new_certified_statements": 0,
        "proof_steps_created_for_toda": 0,
        "legacy_proof_used": False,
        "full_pytest_run": False,
    }
