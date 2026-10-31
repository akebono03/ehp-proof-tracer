"""Suppress only redundant, proved suspension equalities in complete prose.

This is a display projection. It never constructs a proof, changes a ProofStep,
infers a new relation, or uses rendered strings to assert equality. A verified
and cited generator-suspension premise must remain visibly represented.
"""
from __future__ import annotations

from expression import HomotopyElement, Suspension
from homotopy_groups import TodaSuspensionMap
from phase165_r14_r14_diagonal_and_prop42 import GeneratorSuspension
from phase168_r3_27_typed_statement_projection import typed_sentence
from phase168_r3_3_proof_narrative_model import root_ancestor_step_indices
from proof import ProofRule, Relation, RelationType


def same_typed_generator(left: object, right: object) -> bool:
    """Compare registered generator identity, degree and endpoints, not spelling.

    The repository can spell one eta generator with either a Unicode or
    underscore subscript. This structural check is family-independent and
    grants no mathematical equality outside an existing verified ProofStep.
    """
    return (
        isinstance(left, HomotopyElement)
        and isinstance(right, HomotopyElement)
        and left.generator is not None
        and left.generator == right.generator
        and left.dimension == right.dimension
        and left.source == right.source
        and left.target == right.target
    )


def redundant_suspension_relation_indices(
    model: object,
    display_order: tuple[int, ...],
    already_hidden: set[int] | frozenset[int] = frozenset(),
) -> frozenset[int]:
    """Identify exact suspension-equality and symmetry steps safe to omit.

    A source GeneratorSuspension must be an inference in the completed root
    ancestry, have a visible typed sentence, and depend on an actually cited
    GIVEN. Both follow-up relations must be uncited INFERENCE steps and have
    precisely the checked typed premises. Nothing is removed from the model.
    Other equality chains and hidden/uncited source sentences remain intact.
    """
    steps = getattr(model, "steps", None)
    numbers = getattr(model, "step_citation_numbers", None)
    root_index = getattr(model, "root_index", None)
    if (not isinstance(steps, tuple) or not isinstance(numbers, tuple)
            or len(steps) != len(numbers) or type(root_index) is not int):
        return frozenset()
    try:
        ancestry = root_ancestor_step_indices(steps, root_index)
    except ValueError:
        return frozenset()
    order = tuple(display_order)
    if (any(type(index) is not int or index not in ancestry for index in order)
            or len(set(order)) != len(order)):
        return frozenset()
    eligible = set(order).difference(already_hidden)

    def unique_index(node: object) -> int | None:
        same_identity = [index for index, step in enumerate(steps) if step is node]
        if len(same_identity) == 1:
            return same_identity[0]
        if same_identity:
            return None
        same_value = [index for index, step in enumerate(steps) if step == node]
        return same_value[0] if len(same_value) == 1 else None

    def has_cited_given_ancestor(node: object) -> bool:
        pending = [node]
        visited: set[int] = set()
        while pending:
            step = pending.pop()
            if id(step) in visited:
                continue
            visited.add(id(step))
            index = unique_index(step)
            if index is None or index not in ancestry:
                return False
            if step.rule is ProofRule.GIVEN and numbers[index]:
                return True
            pending.extend(step.premises)
        return False

    redundant: set[int] = set()
    direct_indices: set[int] = set()
    for index in order:
        step = steps[index]
        relation = step.conclusion
        if (index not in eligible or index == root_index
                or step.rule is not ProofRule.INFERENCE
                or numbers[index]
                or len(step.premises) != 1
                or not isinstance(relation, Relation)
                or relation.relation_type is not RelationType.EQUALITY):
            continue
        parent = step.premises[0]
        parent_index = unique_index(parent)
        if parent_index is None or parent_index not in ancestry:
            continue
        generator = parent.conclusion
        if (parent_index in eligible
                and parent.rule is ProofRule.INFERENCE
                and isinstance(generator, GeneratorSuspension)
                and isinstance(generator.map, TodaSuspensionMap)
                and typed_sentence(generator, parent) is not None
                and has_cited_given_ancestor(parent)
                and isinstance(relation.lhs, Suspension)
                and same_typed_generator(
                    relation.lhs.expression, generator.source_generator,
                )
                and same_typed_generator(
                    relation.rhs, generator.target_generator,
                )):
            redundant.add(index)
            direct_indices.add(index)

    for index in order:
        step = steps[index]
        relation = step.conclusion
        if (index not in eligible or index == root_index
                or step.rule is not ProofRule.INFERENCE
                or numbers[index]
                or len(step.premises) != 1
                or not isinstance(relation, Relation)
                or relation.relation_type is not RelationType.EQUALITY):
            continue
        parent = step.premises[0]
        parent_index = unique_index(parent)
        if parent_index not in direct_indices:
            continue
        previous = parent.conclusion
        if (parent.rule is ProofRule.INFERENCE
                and isinstance(previous, Relation)
                and previous.relation_type is RelationType.EQUALITY
                and relation.lhs == previous.rhs
                and relation.rhs == previous.lhs):
            redundant.add(index)
    return frozenset(redundant)
