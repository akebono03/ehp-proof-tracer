"""Shared Phase 165 typed backward-search path. Never replay saved proofs.

Typed source claims may be reused across goals; a source's role as a leaf
is not a license to use an untyped archive or an earlier derived proof.
"""
from __future__ import annotations

from dataclasses import replace
from pathlib import Path

from homotopy_groups import FreeCyclicGroup, TodaPrimaryGroup
from phase163_r4_registry_bridge import RegistryBridgeResult
from phase165_r14_r6_generic_iso import GeneratorImage, MapIsomorphism, expand_generic_iso_goal
from phase165_r14_r9_ehp_exactness import expand_generic_ehp_hopf_goal
from phase165_r14_r11_delta_zero import expand_delta_zero_from_suspension_iso
from phase165_r14_r14_diagonal_and_prop42 import expand_diagonal_suspension
from phase165_r14_r33_final_group import reverse_free_cyclic_transport_rule
from phase165_r52_r23_existing_rule_adapter import expand_existing_pi43_rules
from phase165_r3_recursive_search import GoalExpansion
from phase165_r52_r2_search_adapter import search_registered_partial_proof
from phase165_r52_partial_proof import GroupStructureStatus, ProofSearchStatus
from proof import ProofRule, ProofStep, Relation, RelationType
from unified_statement_registry import (
    AssertionOrigin, UnifiedStatementRegistry,
)


def build_shared_typed_bridge(*, sources: tuple[RegistryBridgeResult, ...] | None = None) -> RegistryBridgeResult:
    """Merge eligible typed statements without importing derived group proofs.

    The R38 adopted-Tex *source assertions* are currently the first available
    rigorously linked typed leaves. They are shared with every query, not
    selected because the requested group is pi3^2.
    """
    if sources is None:
        from phase165_r9_production_wiring import discover_goal_search_inputs
        from phase165_r14_r38_direct_registry import build_adopted_typed_reference_registry
        production = discover_goal_search_inputs().bridge
        adopted_tex = Path(__file__).resolve().with_name("phase165_r14_r39_toda51.tex")
        from phase165_r52_r13_reference_registration import build_adopted_prop51_reference
        sources = (production, build_adopted_typed_reference_registry(adopted_tex),
                   build_adopted_prop51_reference())
    registry = UnifiedStatementRegistry()
    links = []
    records = []
    for index, source in enumerate(sources):
        if not isinstance(source, RegistryBridgeResult):
            raise TypeError("source must be RegistryBridgeResult")
        prefix = f"shared:{index}:"
        for ref in source.registry._references.values():
            registry.add_reference(replace(ref, reference_id=prefix + ref.reference_id))
        for assertion in source.registry._assertions.values():
            if assertion.origin is AssertionOrigin.PROOF_INTERNAL:
                continue
            registry.add_assertion(replace(
                assertion, assertion_id=prefix + assertion.assertion_id,
                reference_id=prefix + assertion.reference_id,
                dependencies=tuple(prefix + dep for dep in assertion.dependencies),
            ))
        eligible_ids = {
            a.assertion_id for a in source.registry._assertions.values()
            if a.origin is AssertionOrigin.FIXED_STATEMENT
        }
        for link in source.proof_links:
            if link.assertion_id not in eligible_ids:
                continue
            if link.step is not None and (
                link.step.rule is not ProofRule.GIVEN
                or link.step.conclusion != source.registry.assertion(link.assertion_id).content
            ):
                raise ValueError("source link is not a typed fixed Reference")
            links.append(replace(link, assertion_id=prefix + link.assertion_id))
        records.extend(
            replace(record, assertion_id=prefix + record.assertion_id)
            if record.assertion_id is not None else record
            for record in source.records
        )
    from phase165_r52_r12_component_bridge import expand_cited_given_components
    return expand_cited_given_components(
        RegistryBridgeResult(registry, tuple(records), tuple(links))
    )


def shared_expansion_provider(bridge: RegistryBridgeResult, extra_providers: tuple = ()):
    """Build backward proposals from typed source witnesses and common rules."""
    if not isinstance(bridge, RegistryBridgeResult):
        raise TypeError("bridge must be RegistryBridgeResult")
    available = []
    for link in bridge.proof_links:
        if link.step is None or link.step.rule is not ProofRule.GIVEN:
            continue
        assertion = bridge.registry.assertion(link.assertion_id)
        if assertion.origin is AssertionOrigin.FIXED_STATEMENT:
            available.append(link.step.conclusion)
    def expand(goal: object) -> tuple[GoalExpansion, ...]:
        options = []
        if (isinstance(goal, Relation)
                and goal.relation_type is RelationType.EQUALITY
                and isinstance(goal.rhs, FreeCyclicGroup)
                and isinstance(goal.lhs, TodaPrimaryGroup)):
            for image in available:
                if not isinstance(image, GeneratorImage):
                    continue
                if (getattr(image.map, "source_group", None) != goal.lhs
                        or image.source_generator != goal.rhs.generator):
                    continue
                options.append(GoalExpansion(
                    reverse_free_cyclic_transport_rule(),
                    (MapIsomorphism(image.map),
                     Relation(image.map.target_group,
                              FreeCyclicGroup(image.target_generator)),
                     image),
                ))
        for provider in (
            expand_generic_iso_goal,
            expand_generic_ehp_hopf_goal,
            expand_delta_zero_from_suspension_iso,
            expand_diagonal_suspension,
            expand_existing_pi43_rules,
            *extra_providers,
        ):
            new = provider(goal)
            if not isinstance(new, tuple) or not all(isinstance(x, GoalExpansion) for x in new):
                raise TypeError("expansion provider contract violated")
            options.extend(new)
        return tuple(options)
    return expand


def search_shared_group_goal(*, n: int, k: int, group_structure: object,
                              bridge: RegistryBridgeResult | None = None,
                              expansion_provider=None,
                              citing_assertion_id: str | None = None,
                              verified_assertion_ids: tuple[str, ...] = (), completed_internal_proofs: tuple = (), proof_use_order=None):
    """Run canonical search under a screened Reference context.

    Older calls retain their signature. R15 ordering is applied to sources
    outside the explicitly adopted-Tex policy; no IDs are auto-verified.
    """
    from phase165_r52_r16_web_citation_gate import screen_shared_proof_context

    if bridge is None:
        bridge = build_shared_typed_bridge()
    goal = Relation(TodaPrimaryGroup(n + k, n), group_structure)
    assertions = tuple(bridge.registry._assertions.values())
    if not assertions:
        raise ValueError("shared typed registry is empty")
    context_id = citing_assertion_id or assertions[0].assertion_id
    proof_context = screen_shared_proof_context(
        bridge, goal=goal, citing_assertion_id=context_id,
        verified_assertion_ids=verified_assertion_ids,
    )
    if proof_use_order == "registered":
        from phase165_r52_r19_prop51_binding import resolve_registered_proof_use_order
        proof_use_order = resolve_registered_proof_use_order(proof_context, goal)
    if proof_use_order is not None:
        from phase165_r52_r18_proof_order import restrict_by_proof_use_order
        proof_context = restrict_by_proof_use_order(
            proof_context, goal=goal, policy=proof_use_order,
        )
    if expansion_provider is None:
        expansion_provider = shared_expansion_provider(proof_context)
    return search_registered_partial_proof(
        n=n, k=k, goal=goal, bridge=proof_context,
        citing_assertion_id=context_id,
        expansion_provider=expansion_provider,
        lookup_mode="typed_reference",
        structure_status=GroupStructureStatus.UNKNOWN,
        completed_internal_proofs=completed_internal_proofs,
    )
