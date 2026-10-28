"""Read-only comparison contract for already-verified transport projections.

This module does not create a ProofStep or claim an equivalence between two
independent derivations.  It describes the common observable safety contract.
"""
from __future__ import annotations

from dataclasses import dataclass

from homotopy_groups import (
    DirectSumGroup,
    FiniteCyclicGroup,
    FreeCyclicGroup,
    TodaIteratedSuspensionMap,
)
from phase165_r14_r14_diagonal_and_prop42 import GeneratorSuspension
from phase165_r14_r6_generic_iso import GeneratorImage
from proof import ProofRule, Relation, RelationType
from toda_rules import Toda45IsomorphismStatement


@dataclass(frozen=True)
class AuditCase:
    n: int
    k: int
    category: str
    expected_components: int
    expected_exponent: int

    @property
    def group(self) -> str:
        return f"pi_{self.n + self.k}^{self.n}"


CASES = (
    AuditCase(22, 6, "finite_cyclic", 1, 14),
    AuditCase(22, 10, "finite_cyclic", 1, 10),
    AuditCase(15, 8, "direct_sum", 2, 5),
    AuditCase(24, 9, "direct_sum", 3, 13),
)


def structure_components(structure: object) -> tuple[object, ...] | None:
    """Extract only explicitly represented cyclic summands, never infer them."""
    if isinstance(structure, (FiniteCyclicGroup, FreeCyclicGroup)):
        return (structure,)
    if isinstance(structure, DirectSumGroup):
        groups = structure.summands
        if (isinstance(groups, tuple) and len(groups) >= 2
                and all(isinstance(x, (FiniteCyclicGroup, FreeCyclicGroup))
                        for x in groups)):
            return groups
    return None


def inspect_shared_contract(model: object, order: tuple[int, ...],
                            display: object, case: AuditCase) -> dict:
    """Reject any projection hiding cited or externally consumed evidence.

    Trust-boundary verification must already have been called by the caller.
    This is an independent *presentation* integrity check, not certification.
    """
    steps = getattr(model, "steps", None)
    links = getattr(model, "step_citation_numbers", None)
    root_index = getattr(model, "root_index", None)
    if (not isinstance(steps, tuple) or not isinstance(links, tuple)
            or len(links) != len(steps) or not isinstance(order, tuple)
            or len(order) != len(set(order))
            or any(type(i) is not int or i < 0 or i >= len(steps) for i in order)
            or type(root_index) is not int or root_index not in order):
        raise ValueError("invalid verified-model presentation index contract")
    root = steps[root_index]
    if (root.rule is not ProofRule.INFERENCE
            or not isinstance(root.conclusion, Relation)
            or root.conclusion.relation_type is not RelationType.EQUALITY
            or len(root.premises) < 3):
        raise ValueError("transport must be a typed inferred group root")
    prior_step, iso_step, *images = root.premises
    if (not isinstance(prior_step.conclusion, Relation)
            or prior_step.conclusion.relation_type is not RelationType.EQUALITY
            or iso_step.rule is not ProofRule.INFERENCE
            or not isinstance(iso_step.conclusion, Toda45IsomorphismStatement)
            or not isinstance(iso_step.conclusion.map, TodaIteratedSuspensionMap)):
        raise ValueError("prior relation and proved Toda (4.5) are required")
    src, dst = prior_step.conclusion, root.conclusion
    mapping = iso_step.conclusion.map
    source_parts = structure_components(src.rhs)
    target_parts = structure_components(dst.rhs)
    if (source_parts is None or target_parts is None
            or len(source_parts) != case.expected_components
            or len(target_parts) != case.expected_components
            or type(mapping.exponent) is not int
            or mapping.exponent != case.expected_exponent
            or mapping.exponent < 2
            or mapping.source_group != src.lhs
            or mapping.target_group != dst.lhs
            or len(images) != mapping.exponent * len(source_parts)
            or any(type(left) is not type(right)
                   or getattr(left, "order", None) != getattr(right, "order", None)
                   for left, right in zip(source_parts, target_parts))):
        raise ValueError("component count, group types or suspension dimensions differ")
    if (case.category == "finite_cyclic"
            and not (len(source_parts) == 1
                     and isinstance(source_parts[0], FiniteCyclicGroup))):
        raise ValueError("not the reviewed finite-cyclic presentation route")
    if case.category == "direct_sum" and not isinstance(dst.rhs, DirectSumGroup):
        raise ValueError("not the reviewed direct-sum presentation route")
    for step in images:
        if step.rule is not ProofRule.INFERENCE or not isinstance(step.conclusion, GeneratorImage):
            raise ValueError("every generator image must be proved")
    if getattr(display, "root_index", None) != root_index:
        raise ValueError("projection moved the root")
    hidden = getattr(display, "hidden_indices", None)
    if (not isinstance(hidden, tuple) or not hidden
            or len(hidden) != len(set(hidden))
            or any(type(i) is not int or i == root_index or i not in order
                   for i in hidden)):
        raise ValueError("invalid or empty hidden step set")
    hidden_set = set(hidden)
    for index in hidden:
        step = steps[index]
        if (step.rule is not ProofRule.INFERENCE or links[index]
                or not isinstance(step.conclusion, (GeneratorImage, GeneratorSuspension))):
            raise ValueError("a GIVEN, cited, or non-generator step would be hidden")
        consumers = {
            j for j, candidate in enumerate(steps)
            if any(parent is step for parent in candidate.premises)
        }
        if not consumers or not consumers.issubset(hidden_set | {root_index}):
            raise ValueError("hidden step has an uncovered external consumer")
    references = {x.number for x in model.citations}
    projected = getattr(display, "citation_numbers", None)
    if (not isinstance(projected, tuple) or not projected
            or not set(projected).issubset(references)):
        raise ValueError("projection must retain registered source citations")
    return {
        "group": case.group,
        "category": case.category,
        "components": len(source_parts),
        "suspensions": mapping.exponent,
        "root_generator_images": len(images),
        "hidden_inference_steps": len(hidden),
        "registered_citation_numbers": sorted(references),
        "projection_citation_numbers": list(projected),
        "projection_output_shape": type(display).__name__,
        "shared_contract": "PASS",
    }
