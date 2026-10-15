"""Phase 162 R3-B: unmodified production Renderer audit of the R2 ancestry.

No prior Markdown, handwritten proof prose, or pi_5^3-specific renderer is used.
The statement-level checks below are *diagnostic*, not a proof that every
mathematical inference is adequately explained in the final narrative.
"""

import json
from collections import Counter
from pathlib import Path

from audit_phase162_r3a_presentation import build_r2_fixture
from proof import ProofRule
from proof_repository import ProofRepositoryEntry
from toda_group_result import normalize_toda_group_result
from toda_group_result_proof_replay import build_complete_toda_group_result_proof_replay
from toda_group_proof_presentation import build_toda_group_proof_presentation
from toda_group_proof_narrative_renderer import render_toda_group_proof_narrative_markdown
from toda_group_proof_generic_narrative_renderer import _render_generic_narrative_step
from toda_proof_dependency import extract_toda_recursive_proof_provenance


OUTPUT_DIR = Path('phase162_r3b_output')


def build_r3b_presentation():
    """Construct the R2 root anew, preserving every original ProofStep object."""
    r2 = build_r2_fixture()
    root = r2.reconstruction.final_step
    entry = ProofRepositoryEntry(
        key='phase162_r3b_audit_pi5_3', step=root, phase='162'
    )
    group = normalize_toda_group_result(entry)
    replay = build_complete_toda_group_result_proof_replay(group)
    presentation = build_toda_group_proof_presentation(replay)
    provenance = extract_toda_recursive_proof_provenance(group)

    expected_nodes = {id(n.proof_step) for n in provenance.nodes}
    actual_nodes = {id(n.proof_step) for n in presentation.nodes}
    expected_edges = {
        (id(e.parent_step), id(e.premise_step), e.premise_index)
        for e in provenance.edges
    }
    actual_edges = {
        (id(e.parent_step), id(e.premise_step), e.premise_index)
        for e in presentation.edges
    }
    assert root is presentation.root_step
    assert group.proof_step is entry.step
    assert replay.root_step is root
    assert len(actual_nodes) == len(presentation.nodes)
    assert len(actual_edges) == len(presentation.edges)
    assert expected_nodes == actual_nodes, 'R2 ancestry nodes changed'
    assert expected_edges == actual_edges, 'R2 ancestry edges changed'
    assert all(
        e.parent_step.premises[e.premise_index] is e.premise_step
        for e in presentation.edges
    )
    assert len(root.premises) == 3
    assert root.premises[1] is r2.source_structure_step
    assert root.premises[2] is r2.generator_image_step
    return r2, presentation


def _diagnose_individual_steps(presentation, raw_markdown):
    """Observe generic fact support without conflating it with explanation."""
    rows = []
    for index, node in enumerate(presentation.nodes):
        step = node.proof_step
        rule_name = step.inference_rule.name if step.inference_rule else None
        error = None
        try:
            fact = _render_generic_narrative_step(step)
        except Exception as exc:
            fact = None
            error = f'{type(exc).__name__}: {exc}'
        # This is only an indication that a literal individual fact appears;
        # it cannot attribute paragraphs or justify the inference mathematically.
        is_internal_fallback = fact in (
            None, '', rule_name, f'`{type(step.conclusion).__name__}`'
        )
        observed = bool(fact and not is_internal_fallback and fact in raw_markdown)
        rows.append({
            'index': index,
            'depth': node.depth,
            'role': node.role.value,
            'proof_rule': step.rule.value,
            'statement_type': type(step.conclusion).__name__,
            'inference_rule_name': rule_name,
            'premise_count': len(step.premises),
            'generic_fact': fact,
            'generic_fact_error': error,
            'generic_fact_fallback': is_internal_fallback,
            'literal_fact_observed_in_markdown': observed,
            'reason_explanation_verified': False,
            'reason_explanation_status': 'NOT_AUDITED',
        })
    return rows


def perform_r3b_audit(output_dir=OUTPUT_DIR):
    """Render exactly once via the existing public general Renderer."""
    r2, presentation = build_r3b_presentation()
    raw_markdown = render_toda_group_proof_narrative_markdown(presentation)
    if not isinstance(raw_markdown, str):
        raise TypeError('Production Renderer did not return str')
    if not raw_markdown.strip():
        raise ValueError('Production Renderer returned empty Markdown')

    # Save returned Markdown verbatim; do not postprocess the output.
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    markdown_path = output_dir / 'r2_production_narrative_raw.md'
    markdown_path.write_bytes(raw_markdown.encode('utf-8'))
    rows = _diagnose_individual_steps(presentation, raw_markdown)
    counts = Counter(row['proof_rule'] for row in rows)
    fallback_rows = [row['index'] for row in rows if row['generic_fact_fallback']]
    missing_literal_rows = [
        row['index'] for row in rows
        if row['proof_rule'] == ProofRule.INFERENCE.value
        and not row['literal_fact_observed_in_markdown']
    ]
    report = {
        'status': 'RENDERED_NOT_SEMANTICALLY_CERTIFIED',
        'source': 'phase162_r2_final_step_via_existing_presentation',
        'renderer': 'render_toda_group_proof_narrative_markdown',
        'historical_markdown_used_as_input': False,
        'specialized_pi5_3_prose_added': False,
        'node_count': len(presentation.nodes),
        'edge_count': len(presentation.edges),
        'max_depth': presentation.max_depth,
        'given_count': counts[ProofRule.GIVEN.value],
        'inference_count': counts[ProofRule.INFERENCE.value],
        'root_rule': presentation.root_step.inference_rule.name,
        'root_premises': [type(s.conclusion).__name__ for s in presentation.root_step.premises],
        'raw_markdown_characters': len(raw_markdown),
        'raw_markdown_lines': len(raw_markdown.splitlines()),
        'generic_fact_fallback_indices': fallback_rows,
        'inference_fact_not_literally_observed_indices': missing_literal_rows,
        'reason_explanation_verified_count': 0,
        'reason_explanation_audit_status': 'NOT_AUDITED',
        'limitations': [
            'Literal presence of a rendered fact does not demonstrate a valid reasoning explanation.',
            'A missing literal snippet can be due to formatting, deduplication, reference selection, or unsupported rendering.',
            'No conclusion about individual mathematical reasoning coverage is asserted by this audit.',
        ],
    }
    (output_dir / 'renderer_audit.json').write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8'
    )
    (output_dir / 'step_diagnostics.json').write_text(
        json.dumps(rows, ensure_ascii=False, indent=2) + '\n', encoding='utf-8'
    )
    return report, raw_markdown, rows


def main():
    report, _, _ = perform_r3b_audit()
    print(json.dumps(report, ensure_ascii=False, indent=2))
    print('Raw production Markdown:', (OUTPUT_DIR / 'r2_production_narrative_raw.md').resolve())
    print('Per-step diagnostics:', (OUTPUT_DIR / 'step_diagnostics.json').resolve())


if __name__ == '__main__':
    main()
