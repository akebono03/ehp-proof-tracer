"""R12-R8: inventory permitted typed source anchors for generic quotient search.

No invented source facts, map facts, target structures, or proof steps.
Proof-use screening must precede calling the collector.
"""
from __future__ import annotations

from dataclasses import dataclass

from phase163_r4_registry_bridge import RegistryBridgeResult
from proof import ProofRule, ProofStep
from unified_statement_registry import AssertionOrigin


@dataclass(frozen=True)
class TypedSourceAnchor:
    assertion_id: str
    conclusion: object
    step: ProofStep


def collect_permitted_typed_source_anchors(
    screened_bridge: RegistryBridgeResult,
) -> tuple[TypedSourceAnchor, ...]:
    """Return only the actual cited GIVEN leaves of an already screened bridge.

    This does not infer permission from the registry or a citation label.
    The caller must apply the citation and dependency-order gates first.
    """
    if not isinstance(screened_bridge, RegistryBridgeResult):
        raise TypeError("screened_bridge must be RegistryBridgeResult")
    result: list[TypedSourceAnchor] = []
    seen: set[str] = set()
    for link in screened_bridge.proof_links:
        assertion = screened_bridge.registry.assertion(link.assertion_id)
        step = link.step
        if (assertion.origin is not AssertionOrigin.FIXED_STATEMENT
                or not isinstance(step, ProofStep)
                or step.rule is not ProofRule.GIVEN
                or step.premises
                or type(step.conclusion) is not type(assertion.content)
                or step.conclusion != assertion.content):
            continue
        if assertion.assertion_id in seen:
            raise ValueError("duplicate typed proof witness: " + assertion.assertion_id)
        seen.add(assertion.assertion_id)
        result.append(TypedSourceAnchor(assertion.assertion_id, assertion.content, step))
    return tuple(result)


def audit_real_pi43_quotient_connection() -> dict[str, object]:
    """Observe the R7-screened source context; do not certify the goal."""
    from map_property_rules import SurjectiveMapStatement
    from phase165_prop51_claim_order import pi4_3_goal
    from phase165_r12_r2_quotient_rules import (
        CyclicStructureStatement, HomomorphismPresentationStatement,
        KernelMultipleStatement, QuotientIsomorphismStatement,
    )
    from phase165_r52_r16_web_citation_gate import screen_shared_proof_context
    from phase165_r52_r9_shared_math import build_shared_typed_bridge
    from phase165_r6_2_r4_seeded_goals import generate_seeded_backward_goals
    from phase165_r6_2_unified_registry_r1.unified_backward_rule_registry import build_unified_backward_rule_registry
    from proof import Relation
    from toda_rules import TodaDeltaImageUpToSignStatement, TodaProp42ExactnessStatement

    bridge = build_shared_typed_bridge()
    target = pi4_3_goal()
    match = tuple(a for a in bridge.registry._assertions.values()
                  if a.assertion_id.endswith(":toda:adopted:prop5.1:pi4_3")
                  and a.content == target)
    if len(match) != 1:
        raise ValueError("registered Proposition 5.1 claim 4 target not uniquely found")
    screened = screen_shared_proof_context(
        bridge, goal=target, citing_assertion_id=match[0].assertion_id,
    )
    anchors = collect_permitted_typed_source_anchors(screened)
    classes = (HomomorphismPresentationStatement, KernelMultipleStatement,
               SurjectiveMapStatement, QuotientIsomorphismStatement,
               CyclicStructureStatement, Relation, TodaDeltaImageUpToSignStatement,
               TodaProp42ExactnessStatement)
    counts = {cls.__name__: sum(isinstance(a.conclusion, cls) for a in anchors)
              for cls in classes}
    cyclic_goal = CyclicStructureStatement(
        target.lhs, target.rhs.generator, target.rhs.order,
    )
    registry, _ = build_unified_backward_rule_registry()
    proposals = generate_seeded_backward_goals(
        cyclic_goal, registry.rules(), tuple(a.step for a in anchors),
    )
    # An expansion is a proposal, never a proof. Presence of Relation and Delta
    # source facts cannot automatically establish kernel/surjectivity.
    return {
        "phase": "165 R12-R8",
        "mode": "R7_SCREENED_TYPED_SOURCE_CONNECTION_AUDIT",
        "registered_rules": len(registry.rules()),
        "r7_permitted_given_count": len(anchors),
        "permitted_assertion_ids": [a.assertion_id for a in anchors],
        "relevant_source_type_counts": counts,
        "cyclic_goal_seeded_proposal_count": len(proposals),
        "cyclic_goal_seeded_subgoals": [repr(p.subgoals) for p in proposals],
        "requires_internal_derivation": [
            "HomomorphismPresentationStatement", "KernelMultipleStatement",
            "SurjectiveMapStatement", "CyclicStructureStatement(source_group)",
        ],
        "target_as_given": any(a.conclusion == target for a in anchors),
        "pi43_proof_certified": False,
        "full_pytest_run": False,
        "note": "Only actual screened typed GIVEN witnesses are enumerated; derived statements require canonical inference ProofSteps.",
    }
