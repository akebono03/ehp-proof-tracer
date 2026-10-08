"""Save an honest recursive ProofStep narration trace and coverage report."""

import json
from pathlib import Path

from audit_phase162_r3b_existing_renderer import build_r3b_presentation
from phase162_r3f_recursive_renderer import render_phase162_r3f_recursive_markdown


def main() -> None:
    _, presentation = build_r3b_presentation()
    result = render_phase162_r3f_recursive_markdown(presentation)
    counts = {
        status: sum(r.reason_status == status for r in result.records)
        for status in ('GIVEN', 'EXPLAINED', 'UNEXPLAINED')
    }
    report = {
        'status': 'RECURSIVE_TRACE_NOT_FULLY_NARRATED',
        'root_rule': presentation.root_step.inference_rule.name,
        'node_count': len(result.records),
        'edge_count': result.checked_edge_count,
        'expected_node_count': len(presentation.nodes),
        'expected_edge_count': len(presentation.edges),
        'given_count': counts['GIVEN'],
        'inference_explained_count': counts['EXPLAINED'],
        'inference_unexplained_count': counts['UNEXPLAINED'],
        'all_nodes_once': len({id(r.step) for r in result.records}) == len(result.records),
        'dependency_first': all(all(i < r.index for i in r.premise_indices) for r in result.records),
        'root_is_last': result.records[-1].step is presentation.root_step,
        'historical_markdown_used_as_input': False,
        'public_renderer_changed': False,
        'full_proof_semantic_certification': False,
        'limitations': [
            'Only the Phase 162 group-structure transport root has a narrated inference reason.',
            'Other inference nodes are displayed as facts with an explicit unexplained status.',
            'The generic fact renderer can fall back to type or rule labels.',
            'Proof prose coherence, reference selection, and mathematical validity of all ancestry are not audited here.',
        ],
    }
    output = Path('phase162_r3f_output')
    output.mkdir(exist_ok=True)
    (output / 'recursive_proofstep_trace.md').write_text(result.markdown, encoding='utf-8')
    (output / 'recursive_trace_audit.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    (output / 'recursive_step_index.json').write_text(
        json.dumps([
            {'index': r.index, 'premise_indices': list(r.premise_indices), 'reason_status': r.reason_status,
             'statement_type': type(r.step.conclusion).__name__,
             'inference_rule': r.step.inference_rule.name if r.step.inference_rule is not None else None}
            for r in result.records
        ], ensure_ascii=False, indent=2) + '\n', encoding='utf-8'
    )
    print(json.dumps(report, ensure_ascii=False, indent=2))
    print('Trace Markdown:', (output / 'recursive_proofstep_trace.md').resolve())
    print('Audit report:', (output / 'recursive_trace_audit.json').resolve())


if __name__ == '__main__':
    main()
