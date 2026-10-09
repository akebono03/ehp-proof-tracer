"""Connected proof-tree witnesses for suspension transport.

This module extracts existing ProofStep dependencies. It performs no
inference, concrete substitution, reference selection, or rendering.
"""

from dataclasses import dataclass

from expression import IteratedSuspension
from homotopy_groups import FiniteCyclicGroup
from proof import ProofStep, Relation, RelationType
from toda_rules import Toda45IsomorphismStatement
from toda_stable_group_transport import (
    _concrete_toda_group_matches_structural_group,
)


@dataclass(frozen=True)
class SuspensionTransportFacts:
    target_step: ProofStep
    transported_group_step: ProofStep
    source_group_step: ProofStep
    isomorphism_step: ProofStep
    generator_bridge_step: ProofStep


def _walk_steps(root: ProofStep) -> tuple[ProofStep, ...]:
    if not isinstance(root, ProofStep):
        raise TypeError("root must be a ProofStep")
    result = []
    visited = set()
    stack = [root]
    while stack:
        step = stack.pop()
        if id(step) in visited:
            continue
        visited.add(id(step))
        result.append(step)
        stack.extend(reversed(step.premises))
    return tuple(result)


def extract_suspension_transport_facts(
    root: ProofStep,
) -> SuspensionTransportFacts | None:
    """Find a connected symbolic transport and generator bridge.

    A concrete root may descend from a symbolic family statement. This
    function does NOT certify the symbolic-to-concrete specialization.
    A missing isomorphism or disconnected generator bridge fails closed.
    """
    if not isinstance(root, ProofStep):
        raise TypeError("root must be a ProofStep")
    if not isinstance(root.conclusion, Relation):
        return None
    if root.conclusion.relation_type != RelationType.EQUALITY:
        return None
    if not isinstance(root.conclusion.rhs, FiniteCyclicGroup):
        return None

    # The family-bridge inference consumes BOTH the transported group
    # and the suspended-generator equality as its own direct premises.
    for family_step in _walk_steps(root):
        family_relation = family_step.conclusion
        if not isinstance(family_relation, Relation):
            continue
        if family_relation.relation_type != RelationType.EQUALITY:
            continue
        if not isinstance(family_relation.rhs, FiniteCyclicGroup):
            continue

        for transported_step in family_step.premises:
            transported = transported_step.conclusion
            if not isinstance(transported, Relation):
                continue
            if transported.relation_type != RelationType.EQUALITY:
                continue
            if not isinstance(transported.rhs, FiniteCyclicGroup):
                continue
            suspended = transported.rhs.generator
            if not isinstance(suspended, IteratedSuspension):
                continue
            if transported.lhs != family_relation.lhs:
                continue
            if transported.rhs.order != family_relation.rhs.order:
                continue

            for bridge_step in family_step.premises:
                bridge = bridge_step.conclusion
                if not isinstance(bridge, Relation):
                    continue
                if bridge.relation_type != RelationType.EQUALITY:
                    continue
                if bridge.lhs != suspended:
                    continue
                if bridge.rhs != family_relation.rhs.generator:
                    continue

                for source_step in transported_step.premises:
                    source = source_step.conclusion
                    if not isinstance(source, Relation):
                        continue
                    if source.relation_type != RelationType.EQUALITY:
                        continue
                    if not isinstance(source.rhs, FiniteCyclicGroup):
                        continue
                    if source.rhs.order != transported.rhs.order:
                        continue
                    if source.rhs.generator != suspended.expression:
                        continue

                    for iso_step in transported_step.premises:
                        iso = iso_step.conclusion
                        if not isinstance(iso, Toda45IsomorphismStatement):
                            continue
                        if iso.map.exponent != suspended.exponent:
                            continue
                        if not _concrete_toda_group_matches_structural_group(
                            source.lhs, iso.map.source_group,
                        ):
                            continue
                        if iso.map.target_group != transported.lhs:
                            continue
                        return SuspensionTransportFacts(
                            target_step=root,
                            transported_group_step=transported_step,
                            source_group_step=source_step,
                            isomorphism_step=iso_step,
                            generator_bridge_step=bridge_step,
                        )
    return None
