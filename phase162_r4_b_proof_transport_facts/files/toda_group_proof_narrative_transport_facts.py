"""Proof-tree facts for generic finite-cyclic suspension transport.

No rendering, inference, reference guessing, or mutation is performed here.
"""

from dataclasses import dataclass

from expression import IteratedSuspension
from homotopy_groups import FiniteCyclicGroup
from proof import ProofStep, Relation, RelationType
from toda_rules import Toda45IsomorphismStatement


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
    """Locate an actual connected transport-and-generator-bridge derivation.

    Return None when any required premise is absent. In particular, the
    renderer must not manufacture a missing suspension isomorphism.
    """
    if not isinstance(root, ProofStep):
        raise TypeError("root must be a ProofStep")
    if not isinstance(root.conclusion, Relation):
        return None
    if root.conclusion.relation_type != RelationType.EQUALITY:
        return None
    if not isinstance(root.conclusion.rhs, FiniteCyclicGroup):
        return None

    for step in _walk_steps(root):
        if not isinstance(step.conclusion, Relation):
            continue
        transported = step.conclusion
        if transported.relation_type != RelationType.EQUALITY:
            continue
        if not isinstance(transported.rhs, FiniteCyclicGroup):
            continue
        suspended_generator = transported.rhs.generator
        if not isinstance(suspended_generator, IteratedSuspension):
            continue
        for source in step.premises:
            source_statement = source.conclusion
            if not isinstance(source_statement, Relation):
                continue
            if source_statement.relation_type != RelationType.EQUALITY:
                continue
            if not isinstance(source_statement.rhs, FiniteCyclicGroup):
                continue
            if source_statement.rhs.order != transported.rhs.order:
                continue
            if source_statement.rhs.generator != suspended_generator.expression:
                continue
            for iso in step.premises:
                if not isinstance(iso.conclusion, Toda45IsomorphismStatement):
                    continue
                if iso.conclusion.map.exponent != suspended_generator.exponent:
                    continue
                for bridge in _walk_steps(root):
                    statement = bridge.conclusion
                    if not isinstance(statement, Relation):
                        continue
                    if statement.relation_type != RelationType.EQUALITY:
                        continue
                    if statement.lhs != suspended_generator:
                        continue
                    if statement.rhs != root.conclusion.rhs.generator:
                        continue
                    return SuspensionTransportFacts(
                        target_step=root,
                        transported_group_step=step,
                        source_group_step=source,
                        isomorphism_step=iso,
                        generator_bridge_step=bridge,
                    )
    return None
