"""Project a proved 1-stem eta-notation transport into the R10A display contract.

This module changes *presentation only*. All mathematical statements are
existing checked ProofSteps. No source is inferred from an element name alone.
"""
from __future__ import annotations

from expression import IteratedSuspension
from homotopy_groups import (
    FiniteCyclicGroup,
    TodaIteratedSuspensionMap,
    TodaPrimaryGroup,
    TodaSuspensionMap,
)
from phase165_r12_r20_eta_definition import TodaEtaFamilyGeneralDefinition
from phase165_r14_r14_diagonal_and_prop42 import GeneratorSuspension
from phase165_r12_r21_eta_generator_chain import _eta_pair
from phase168_r3_27_typed_statement_projection import (
    element_tex,
    project_stable_eta_notation_transition,
)
from phase169_r10a_verified_stable_chain_projection.projection import (
    VerifiedStableImageChainDisplay,
)
from proof import ProofRule, Relation, RelationType
from toda_rules import Toda45IsomorphismStatement


def project_verified_one_stem_notation_chain(
    model: object, order: tuple[int, ...],
) -> VerifiedStableImageChainDisplay | None:
    """Use the existing certified eta normalization, suppress redundant prose.

    The earlier stable cyclic group, cited Toda isomorphism, and general eta
    definition must be *actual* proof premises. The 1-step end witness is
    suppressed only if it is a cited-definition-derived instance of the same
    endpoint, never by comparison of display labels alone.
    """
    steps = getattr(model, "steps", ())
    root_index = getattr(model, "root_index", None)
    if (not isinstance(steps, tuple)
            or type(root_index) is not int
            or root_index < 0 or root_index >= len(steps)
            or root_index not in order
            or len(getattr(model, "step_citation_numbers", ())) != len(steps)):
        return None
    by_identity = {id(step): index for index, step in enumerate(steps)}
    if len(by_identity) != len(steps):
        return None
    root = steps[root_index]
    if (root.rule is not ProofRule.INFERENCE
            or not isinstance(root.conclusion, Relation)
            or root.conclusion.relation_type is not RelationType.EQUALITY
            or not isinstance(root.conclusion.lhs, TodaPrimaryGroup)
            or not isinstance(root.conclusion.rhs, FiniteCyclicGroup)
            or len(root.premises) != 2
            or project_stable_eta_notation_transition(model, root_index) is None):
        return None
    transported_step, definition_step = root.premises
    transported_index = by_identity.get(id(transported_step))
    definition_index = by_identity.get(id(definition_step))
    if (transported_index is None or definition_index is None
            or transported_index not in order
            or transported_index == root_index
            or model.step_citation_numbers[transported_index]
            or transported_step.rule is not ProofRule.INFERENCE
            or definition_step.rule is not ProofRule.GIVEN
            or not isinstance(definition_step.conclusion, TodaEtaFamilyGeneralDefinition)
            or not model.step_citation_numbers[definition_index]
            or any(
                consumer_index != root_index
                for consumer_index, consumer in enumerate(steps)
                if any(parent is transported_step for parent in consumer.premises)
            )):
        return None
    transported = transported_step.conclusion
    suspended = transported.rhs.generator
    r = suspended.exponent
    source = suspended.expression
    target = root.conclusion.rhs.generator
    source_tex, target_tex = element_tex(source), element_tex(target)
    source_n = getattr(source, "target", None)
    target_n = root.conclusion.lhs.sphere_dimension
    if (type(r) is not int or r < 2
            or type(source_n) is not int or source_n < 3
            or type(target_n) is not int or target_n != source_n + r
            or transported.lhs != root.conclusion.lhs
            or transported.rhs.order != root.conclusion.rhs.order
            or not source_tex or not target_tex
            or len(transported_step.premises) != 2):
        return None
    base_step, iso_step = transported_step.premises
    if (not isinstance(base_step.conclusion, Relation)
            or not isinstance(base_step.conclusion.lhs, TodaPrimaryGroup)
            or base_step.conclusion.relation_type is not RelationType.EQUALITY
            or not isinstance(base_step.conclusion.rhs, FiniteCyclicGroup)
            or base_step.conclusion.rhs.order != transported.rhs.order
            or base_step.conclusion.rhs.generator != source
            or base_step.conclusion.lhs != TodaPrimaryGroup(source_n + 1, source_n)
            or iso_step.rule is not ProofRule.INFERENCE
            or not isinstance(iso_step.conclusion, Toda45IsomorphismStatement)
            or iso_step.conclusion.map != TodaIteratedSuspensionMap(
                exponent=r,
                source_group=base_step.conclusion.lhs,
                target_group=root.conclusion.lhs,
            )):
        return None

    def has_same_general_given_ancestor(step: object) -> bool:
        pending = [step]
        visited = set()
        while pending:
            ancestor = pending.pop()
            if id(ancestor) in visited:
                continue
            visited.add(id(ancestor))
            if (ancestor.rule is ProofRule.GIVEN
                    and ancestor.conclusion == definition_step.conclusion):
                return True
            pending.extend(ancestor.premises)
        return False

    hidden = {transported_index}
    for index in order:
        step = steps[index]
        witness = step.conclusion
        if (index == root_index or index == transported_index
                or step.rule is not ProofRule.INFERENCE
                or model.step_citation_numbers[index]
                or not isinstance(witness, GeneratorSuspension)
                or not isinstance(witness.map, TodaSuspensionMap)
                or witness.map.target_group != root.conclusion.lhs
                or _eta_pair(witness) is None
                or element_tex(witness.target_generator) != target_tex
                or not has_same_general_given_ancestor(step)):
            continue
        hidden.add(index)
    return VerifiedStableImageChainDisplay(
        root_index=root_index,
        exponent=r,
        source_tex=source_tex,
        target_tex=target_tex,
        hidden_indices=tuple(sorted(hidden)),
        citation_numbers=tuple(model.step_citation_numbers[definition_index]),
    )
