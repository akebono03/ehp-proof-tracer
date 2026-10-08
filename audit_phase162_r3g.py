"""Report exact reuse of pre-existing proof reason rules."""

import json
from collections import Counter
from pathlib import Path

from audit_phase162_r3b_existing_renderer import build_r3b_presentation
from phase162_r3g_existing_reason_bridge import build_phase162_r3g_existing_reason_trace


def main() -> None:
    _, presentation = build_r3b_presentation()
    result = build_phase162_r3g_existing_reason_trace(presentation)
    statuses = Counter(record.reason_status for record in result.records)
    kinds = Counter(kind for _, kind in result.reason_kind_by_index)
    report = {
        'status': 'EXISTING_REASON_BRIDGE_AUDIT_NOT_COMPLETE_PROOF',
        'node_count': len(result.records),
        'edge_count': result.checked_edge_count,
        'given_count': statuses['GIVEN'],
        'explained_count': statuses['EXPLAINED'],
        'unexplained_count': statuses['UNEXPLAINED'],
        'explanation_kinds': dict(sorted(kinds.items())),
        'reason_step_indices': list(result.reason_kind_by_index),
        'all_nodes_once': len({id(record.step) for record in result.records}) == len(result.records),
        'dependency_first': all(
            premise_index < record.index
            for record in result.records
            for premise_index in record.premise_indices
        ),
        'root_is_last': result.records[-1].step is presentation.root_step,
        'historical_markdown_used_as_input': False,
        'public_renderer_changed': False,
        'full_proof_semantic_certification': False,
        'limitations': [
            'Only previously implemented, directly matched exactness-to-map-property and exactness-to-kernel reasons are reused.',
            'Existing reason sentences do not themselves constitute a new proof checker.',
            'Unexplained steps remain explicitly labeled; other reason kinds are not yet connected.',
        ],
    }
    output = Path('phase162_r3g_output')
    output.mkdir(exist_ok=True)
    (output / 'recursive_existing_reasons.md').write_text(result.markdown, encoding='utf-8')
    (output / 'existing_reason_audit.json').write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8'
    )
    print(json.dumps(report, ensure_ascii=False, indent=2))
    print('Narrative trace:', (output / 'recursive_existing_reasons.md').resolve())
    print('Audit report:', (output / 'existing_reason_audit.json').resolve())


if __name__ == '__main__':
    main()
