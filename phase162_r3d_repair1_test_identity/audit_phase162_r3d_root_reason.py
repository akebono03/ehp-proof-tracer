"""Phase 162 R3-D: audit actual R2 root inference and public Narrative placement.

This is a *scoped* structural / textual audit. It cannot certify 67 inference
explanations, or infer mathematical entailment from text substring matches.
No historical narrative, fixed mathematical conclusion, or alternative proof is
used as input to the renderer.
"""

import json
from pathlib import Path

from audit_phase162_r3b_existing_renderer import build_r3b_presentation
from expression import MapApplication, MapSymbol, Suspension
from homotopy_groups import FiniteCyclicGroup, TodaSuspensionIsomorphismStatement
from proof import ProofRule, Relation, RelationType
from repository_element_presentation import render_repository_conclusion_latex
from toda_group_proof_narrative_renderer import render_toda_group_proof_narrative_markdown
from toda_group_structure_transport_reason import render_group_structure_transport_reason


OUTPUT_DIR = Path('phase162_r3d_output')


def _root_premise_contract(root, presentation):
    """Check actual identity-linked premises and mathematical transport shape."""
    if root is not presentation.root_step:
        raise AssertionError('Presentation root identity changed')
    if root.rule is not ProofRule.INFERENCE:
        raise AssertionError('Root is not an inference')
    if root.inference_rule is None or root.inference_rule.name != 'phase162_group_structure_transport':
        raise AssertionError('Unexpected root inference rule')
    if len(root.premises) != 3:
        raise AssertionError('Root does not contain three premises')

    iso_step, source_step, image_step = root.premises
    iso, source, image = (step.conclusion for step in root.premises)
    if not isinstance(iso, TodaSuspensionIsomorphismStatement):
        raise AssertionError('The first premise is not an isomorphism')
    if not (isinstance(source, Relation) and source.relation_type is RelationType.EQUALITY
            and isinstance(source.rhs, FiniteCyclicGroup)
            and source.lhs == iso.map.source_group):
        raise AssertionError('The source-group premise is inconsistent')
    if not (isinstance(image, Relation) and image.relation_type is RelationType.EQUALITY
            and image.lhs in (
                Suspension(expression=source.rhs.generator),
                MapApplication(map=MapSymbol(name='E'), expression=source.rhs.generator),
            )):
        raise AssertionError('The generator image premise is inconsistent')
    expected = Relation(
        lhs=iso.map.target_group,
        rhs=FiniteCyclicGroup(order=source.rhs.order, generator=image.rhs),
        relation_type=RelationType.EQUALITY,
    )
    if root.conclusion != expected:
        raise AssertionError('Root conclusion is not the specified transport')

    edges = {(id(e.parent_step), e.premise_index, id(e.premise_step)) for e in presentation.edges}
    for index, premise in enumerate(root.premises):
        if (id(root), index, id(premise)) not in edges:
            raise AssertionError(f'Root premise edge {index} is absent or copied')
    return (iso_step, source_step, image_step)


def audit_root_reason(presentation, markdown):
    """Audit meaning of the root premises separately from textual placement."""
    root = presentation.root_step
    premises = _root_premise_contract(root, presentation)
    reason = render_group_structure_transport_reason(root)
    if not isinstance(reason, str) or not reason.strip():
        raise AssertionError('The root inference did not produce a reason')
    if not isinstance(markdown, str):
        raise TypeError('markdown must be a string')

    proof_header = '## 証明'
    proof_start = markdown.find(proof_header)
    proof_end = markdown.rfind('□')
    reason_pos = markdown.find(reason)
    reason_count = markdown.count(reason)
    final_marker = '以上より,'
    final_pos = markdown.rfind(final_marker)
    if proof_start < 0 or proof_end < 0:
        raise AssertionError('Public Markdown proof section or QED is absent')
    if reason_count != 1:
        raise AssertionError(f'Root reasoning occurs {reason_count} times, expected once')
    if not (proof_start < reason_pos < final_pos < proof_end):
        raise AssertionError('Root reason is not immediately upstream of final conclusion')
    between = markdown[reason_pos + len(reason):final_pos]
    if between.strip():
        raise AssertionError('Unrelated proof prose occurs between reason and final conclusion')

    root_latex = render_repository_conclusion_latex(root.conclusion)
    if not root_latex or root_latex not in markdown[final_pos:proof_end]:
        raise AssertionError('Final conclusion is missing or no longer agrees with root')

    # The renderer's prose is generated from these objects. Checking their
    # identities and equations is meaningful; matching substrings alone is not
    # a proof of semantic completeness.
    premise_types = [type(s.conclusion).__name__ for s in premises]
    return {
        'status': 'ROOT_REASON_STRUCTURE_AND_PLACEMENT_VERIFIED',
        'full_proof_semantic_certification': False,
        'root_reason_semantic_basis': 'three validated ProofStep premises',
        'root_rule': root.inference_rule.name,
        'root_premise_types': premise_types,
        'root_edges_identity_preserved': True,
        'root_transport_equation_verified': True,
        'reason_occurrences': reason_count,
        'reason_before_final_conclusion': True,
        'reason_adjacent_to_final_conclusion': True,
        'final_conclusion_matches_root': True,
        'reason_characters': len(reason),
        'markdown_characters': len(markdown),
        'known_limitation': (
            'The public renderer inserts this verified root reason using a '
            'text marker, not a general inference-aware placement algorithm. '
            'Other inference explanations, prose coherence, and deduplication '
            'remain unverified.'
        ),
    }


def perform_r3d_audit(output_dir=OUTPUT_DIR):
    """Build a fresh R2 proof and audit the unmodified production Markdown."""
    _, presentation = build_r3b_presentation()
    rendered = render_toda_group_proof_narrative_markdown(presentation)
    result = audit_root_reason(presentation, rendered)
    result['node_count'] = len(presentation.nodes)
    result['edge_count'] = len(presentation.edges)
    result['inference_count'] = sum(n.proof_step.rule is ProofRule.INFERENCE for n in presentation.nodes)
    result['given_count'] = sum(n.proof_step.rule is ProofRule.GIVEN for n in presentation.nodes)
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    (output_path / 'r2_public_narrative_raw.md').write_bytes(rendered.encode('utf-8'))
    (output_path / 'root_reason_audit.json').write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + '\n', encoding='utf-8'
    )
    return result, rendered


def main():
    result, _ = perform_r3d_audit()
    print(json.dumps(result, ensure_ascii=False, indent=2))
    print('Public Markdown:', (OUTPUT_DIR / 'r2_public_narrative_raw.md').resolve())
    print('Audit report:', (OUTPUT_DIR / 'root_reason_audit.json').resolve())


if __name__ == '__main__':
    main()
