"""Build the Phase 162 root transport proof from its ProofStep graph.

Only the final inference is narrated here. Its three premises are displayed as
verified derived facts; their recursive derivations are NOT narrated by this
renderer. The existing full recursive presentation remains available separately.
"""

from homotopy_groups import TodaSuspensionIsomorphismStatement
from proof import ProofStep, Relation
from repository_element_presentation import render_repository_conclusion_latex
from toda_group_proof_presentation import TodaGroupProofPresentation
from toda_group_structure_transport_reason import (
    _render_transport_relation_latex,
    render_group_structure_transport_reason,
)
from toda_proof_narrative_renderer import render_toda_primary_group_latex


def render_phase162_r3e_structured_root_markdown(
    presentation: TodaGroupProofPresentation,
) -> str | None:
    """Narrate the root inference in graph order, never inserting into Markdown.

    Return None for unrelated roots. Verify identity-linked Presentation edges,
    the three-premise transport contract, and conclusion rendering.
    """
    if not isinstance(presentation, TodaGroupProofPresentation):
        raise TypeError('presentation must be TodaGroupProofPresentation')

    root = presentation.root_step
    if not isinstance(root, ProofStep):
        raise TypeError('presentation root must be ProofStep')
    reason = render_group_structure_transport_reason(root)
    if reason is None:
        return None

    if len(root.premises) != 3:
        raise ValueError('Root transport requires exactly three premises')
    edge_keys = {
        (id(edge.parent_step), edge.premise_index, id(edge.premise_step))
        for edge in presentation.edges
    }
    for index, premise in enumerate(root.premises):
        if (id(root), index, id(premise)) not in edge_keys:
            raise ValueError('Root transport premise edge is absent or not identical')

    iso, structure, image = (premise.conclusion for premise in root.premises)
    if not isinstance(iso, TodaSuspensionIsomorphismStatement):
        raise ValueError('Transport isomorphism premise is absent')
    if not isinstance(structure, Relation) or not isinstance(image, Relation):
        raise ValueError('Transport relations are absent')
    if not isinstance(root.conclusion, Relation):
        raise ValueError('Transport conclusion is not a relation')

    iso_latex = (
        'E: '
        + render_toda_primary_group_latex(iso.map.source_group)
        + r' \xrightarrow{\cong} '
        + render_toda_primary_group_latex(iso.map.target_group)
    )
    structure_latex = _render_transport_relation_latex(structure)
    image_latex = _render_transport_relation_latex(image)
    result_latex = render_repository_conclusion_latex(root.conclusion)
    if not isinstance(result_latex, str) or not result_latex.strip():
        raise ValueError('Root transport conclusion cannot be rendered')

    # The explicit ordered premises come from the graph, not prewritten proof text.
    # This deliberately does not claim to narrate the recursive 123-node ancestry.
    lines = [
        '# Group proof narrative',
        '',
        '## 証明対象',
        '',
        r'\[',
        result_latex + '.',
        r'\]',
        '',
        '## 証明',
        '',
        '以下の3つの事実は, それぞれの依存する証明から得られている.',
        '',
        '$' + iso_latex + '$.',
        '',
        '$' + structure_latex + '$.',
        '',
        '$' + image_latex + '$.',
        '',
        reason,
        '',
        '以上より, $' + result_latex + '$.',
        '',
        '□',
        '',
    ]
    return '\n'.join(lines)
