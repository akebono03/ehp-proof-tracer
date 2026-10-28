"""Project an existing typed Proof Tree, without asserting new mathematics.

Only a complete, directly rooted multi-suspension inference with an exact
Toda (4.5) witness and a verified chain of GeneratorImage premises qualifies.
No DB access, family-name guessing, new GIVEN, or ProofStep modification occurs.
"""
from __future__ import annotations

from dataclasses import dataclass

from homotopy_groups import (
    FiniteCyclicGroup,
    TodaIteratedSuspensionMap,
    TodaPrimaryGroup,
    TodaSuspensionMap,
)
from phase165_r14_r14_diagonal_and_prop42 import GeneratorSuspension
from phase165_r14_r6_generic_iso import GeneratorImage
from phase168_r3_27_typed_statement_projection import element_tex
from proof import ProofRule, Relation, RelationType
from toda_rules import Toda45IsomorphismStatement


@dataclass(frozen=True)
class VerifiedStableImageChainDisplay:
    root_index: int
    exponent: int
    source_tex: str
    target_tex: str
    hidden_indices: tuple[int, ...]
    citation_numbers: tuple[int, ...]


def project_verified_stable_image_chain(
    model: object, order: tuple[int, ...],
) -> VerifiedStableImageChainDisplay | None:
    """Compress only rooted, checked, at-least-three-fold proven image chains.

    A presentation cannot create or verify proof steps: the caller supplies the
    already-verified model.  This function additionally checks the exact source,
    isomorphism, every image map, every generator endpoint and references.
    Return None rather than removing a statement with a separate consumer.
    """
    steps = getattr(model, "steps", ())
    root_index = getattr(model, "root_index", None)
    if (not isinstance(steps, (tuple, list))
            or type(root_index) is not int
            or root_index < 0 or root_index >= len(steps)
            or root_index not in order):
        return None
    root = steps[root_index]
    if (root.rule is not ProofRule.INFERENCE
            or not isinstance(root.conclusion, Relation)
            or root.conclusion.relation_type is not RelationType.EQUALITY
            or not isinstance(root.conclusion.lhs, TodaPrimaryGroup)
            or not isinstance(root.conclusion.rhs, FiniteCyclicGroup)
            or len(root.premises) < 5):
        return None
    source_step, iso_step, *images = root.premises
    if (not isinstance(source_step.conclusion, Relation)
            or source_step.conclusion.relation_type is not RelationType.EQUALITY
            or not isinstance(source_step.conclusion.lhs, TodaPrimaryGroup)
            or not isinstance(source_step.conclusion.rhs, FiniteCyclicGroup)
            or source_step.conclusion.rhs.order != root.conclusion.rhs.order
            or iso_step.rule is not ProofRule.INFERENCE
            or not isinstance(iso_step.conclusion, Toda45IsomorphismStatement)
            or not isinstance(iso_step.conclusion.map, TodaIteratedSuspensionMap)):
        return None
    src = source_step.conclusion
    dst = root.conclusion
    n, q = src.lhs.sphere_dimension, src.lhs.group_dimension
    m, p = dst.lhs.sphere_dimension, dst.lhs.group_dimension
    r = len(images)
    if (not all(type(v) is int for v in (n, q, m, p))
            or n < 2 or q < n or n < q - n + 2
            or m - n != r or p - q != r
            or iso_step.conclusion.map != TodaIteratedSuspensionMap(
                exponent=r, source_group=src.lhs, target_group=dst.lhs,
            )):
        return None

    by_identity = {id(step): index for index, step in enumerate(steps)}
    if len(by_identity) != len(steps):
        return None
    image_indices = []
    expected_generator = src.rhs.generator
    for i, image_step in enumerate(images):
        image_index = by_identity.get(id(image_step))
        image = image_step.conclusion
        if (image_index is None or image_index not in order
                or image_index == root_index
                or image_step.rule is not ProofRule.INFERENCE
                or not isinstance(image, GeneratorImage)
                or not isinstance(image.map, TodaSuspensionMap)
                or image.map != TodaSuspensionMap(
                    TodaPrimaryGroup(q + i, n + i),
                    TodaPrimaryGroup(q + i + 1, n + i + 1),
                )
                or image.source_generator != expected_generator):
            return None
        expected_generator = image.target_generator
        image_indices.append(image_index)
    if expected_generator != dst.rhs.generator or len(set(image_indices)) != r:
        return None
    for image_index in image_indices:
        image_step = steps[image_index]
        if any(
            consumer_index != root_index
            for consumer_index, consumer in enumerate(steps)
            if any(parent is image_step for parent in consumer.premises)
        ):
            return None
    source_tex, target_tex = element_tex(src.rhs.generator), element_tex(dst.rhs.generator)
    if not source_tex or not target_tex:
        return None

    hidden = set(image_indices)
    # An eta-family suspension step can be shared by adjacent composite images.
    # Hide it only when ALL of its actual consumers are the collapsed images,
    # and the individual step has no direct citation to preserve.
    for index, candidate in enumerate(steps):
        if (index not in order or index == root_index
                or candidate.rule is not ProofRule.INFERENCE
                or not isinstance(candidate.conclusion, GeneratorSuspension)
                or model.step_citation_numbers[index]):
            continue
        consumers = {
            consumer_index
            for consumer_index, consumer in enumerate(steps)
            if any(parent is candidate for parent in consumer.premises)
        }
        if consumers and consumers.issubset(hidden):
            hidden.add(index)

    # Citations are copied from actual linked GIVEN ancestors of the image
    # proofs, not inferred from the symbols eta/nu/sigma or from rule names.
    cited = set()
    for image_step in images:
        pending = [image_step]
        visited = set()
        while pending:
            candidate = pending.pop()
            if id(candidate) in visited:
                continue
            visited.add(id(candidate))
            index = by_identity.get(id(candidate))
            if index is not None and candidate.rule is ProofRule.GIVEN:
                cited.update(model.step_citation_numbers[index])
            pending.extend(candidate.premises)
    citation_numbers = tuple(
        citation.number for citation in model.citations if citation.number in cited
    )
    # Never replace individually cited evidence with an uncited displayed claim.
    if not citation_numbers:
        return None
    return VerifiedStableImageChainDisplay(
        root_index=root_index,
        exponent=r,
        source_tex=source_tex,
        target_tex=target_tex,
        hidden_indices=tuple(sorted(hidden)),
        citation_numbers=citation_numbers,
    )
