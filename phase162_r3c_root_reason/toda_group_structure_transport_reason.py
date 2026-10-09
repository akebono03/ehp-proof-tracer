"""General mathematical explanation for verified finite-cyclic transport steps.

The input is a genuine inference ProofStep. No prior narrative text, target
sphere dimension, or canned group-specific proof is consulted.
"""

from expression import MapApplication, MapSymbol, Suspension
from homotopy_groups import FiniteCyclicGroup, TodaSuspensionIsomorphismStatement
from proof import ProofRule, ProofStep, Relation, RelationType
from repository_element_presentation import render_repository_conclusion_latex
from toda_proof_narrative_renderer import render_toda_proof_statement_latex


def render_group_structure_transport_reason(step: ProofStep) -> str | None:
    """Explain an exact three-premise cyclic transport; reject incoherent evidence."""
    if not isinstance(step, ProofStep):
        raise TypeError('step must be ProofStep')
    inference_rule = step.inference_rule
    if inference_rule is None or inference_rule.name != 'phase162_group_structure_transport':
        return None
    if step.rule is not ProofRule.INFERENCE or len(step.premises) != 3:
        raise ValueError('Transport step must be a three-premise inference')

    iso_step, structure_step, image_step = step.premises
    iso = iso_step.conclusion
    structure = structure_step.conclusion
    image = image_step.conclusion
    result = step.conclusion
    if not isinstance(iso, TodaSuspensionIsomorphismStatement):
        raise ValueError('First premise must be suspension isomorphism')
    if (
        not isinstance(structure, Relation)
        or structure.relation_type is not RelationType.EQUALITY
        or not isinstance(structure.rhs, FiniteCyclicGroup)
        or structure.lhs != iso.map.source_group
    ):
        raise ValueError('Second premise must be source finite-cyclic structure')
    if (
        not isinstance(image, Relation)
        or image.relation_type is not RelationType.EQUALITY
        or image.lhs not in (
            Suspension(expression=structure.rhs.generator),
            MapApplication(map=MapSymbol(name='E'), expression=structure.rhs.generator),
        )
    ):
        raise ValueError('Third premise must identify the image of the source generator')
    expected = Relation(
        lhs=iso.map.target_group,
        rhs=FiniteCyclicGroup(order=structure.rhs.order, generator=image.rhs),
        relation_type=RelationType.EQUALITY,
    )
    if result != expected:
        raise ValueError('Transport conclusion does not follow from recorded premises')

    iso_latex = render_toda_proof_statement_latex(iso)
    source_latex = render_repository_conclusion_latex(structure)
    image_latex = render_repository_conclusion_latex(image)
    if not all(isinstance(value, str) and value for value in (iso_latex, source_latex, image_latex)):
        raise ValueError('A transport premise cannot be rendered')
    return (
        '群構造の移送に必要な前提を確認する. '
        + '$' + iso_latex + '$ は同型であり, '
        + '$' + source_latex + '$ および '
        + '$' + image_latex + '$ が成り立つ. '
        + 'したがって, 同型写像によって位数と生成元が移され, '
        + '移送先は指定された生成元を持つ同じ位数の巡回群である.'
    )
