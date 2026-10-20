from __future__ import annotations

import json
from collections import Counter
from dataclasses import asdict
from pathlib import Path

from phase165_r52_r9_shared_math import build_shared_typed_bridge
from phase165_r5_manifest_bridge import DEFAULT_MANIFEST
from unified_statement_registry import AssertionOrigin
from proof import ProofRule

TARGETS = (
    'shared:1:adopted:ref:3',
    'shared:1:adopted:ref:7',
    'shared:1:adopted:ref:8',
    'shared:1:adopted:ref:9',
    'shared:5:adopted:reference:prop42:general',
    'shared:7:adopted:reference:toda5:eta_family_definition',
)


def source_details(bridge, reference_id):
    reference = bridge.registry.reference(reference_id)
    assertions = bridge.registry.assertions_for(reference_id)
    return {
        'reference_id': reference_id,
        'locator': reference.locator,
        'source_id': reference.source_id,
        'kind': reference.kind.value,
        'publication_position': reference.publication_position,
        'assertions': [
            {'assertion_id': a.assertion_id, 'origin': a.origin.value, 'kind': a.kind.value,
             'content_type': type(a.content).__name__, 'content_repr': repr(a.content)[:800],
             'component_position': a.component_position,
             'has_given_link': any(l.assertion_id == a.assertion_id and l.step is not None and l.step.rule is ProofRule.GIVEN for l in bridge.proof_links)}
            for a in assertions
        ],
    }


def main():
    from phase166_r3l_reference_order import connect_all_reference_orders
    bridge = build_shared_typed_bridge()
    connected, report = connect_all_reference_orders(bridge)
    manifest = json.loads(Path(DEFAULT_MANIFEST).read_text(encoding='utf-8-sig'))
    source_rows = manifest['assertions']
    by_reference = {}
    for row in source_rows:
        by_reference.setdefault(row['reference_id'], []).append(row)
    known_ids = set(by_reference)
    references = list(connected.registry._references.values())
    unmapped = [r for r in references if r.publication_position is None and r.reference_id not in TARGETS]
    classifications = []
    for r in unmapped:
        items = connected.registry.assertions_for(r.reference_id)
        counts = Counter(a.origin.value for a in items)
        if not items:
            category = 'no_assertions'
        elif all(a.origin is AssertionOrigin.SOURCE_ARCHIVE for a in items):
            category = 'source_archive_only'
        elif any(a.origin is AssertionOrigin.FIXED_STATEMENT for a in items):
            category = 'typed_fixed_statement'
        else:
            category = 'other'
        classifications.append({
            'reference_id': r.reference_id, 'locator': r.locator,
            'source_id': r.source_id, 'category': category,
            'origin_counts': dict(counts),
            'assertion_types': sorted({type(a.content).__name__ for a in items}),
        })
    output = {
        'phase': '166-R3M', 'read_only': True, 'full_pytest_run': False,
        'total_references': len(references),
        'ordered_references': sum(r.publication_position is not None for r in references),
        'unresolved_six': [source_details(connected, r) for r in TARGETS],
        'unmapped_classification_counts': dict(Counter(i['category'] for i in classifications)),
        'unmapped_references': classifications,
        'manifest_references': len(known_ids),
        'manifest_prop42_candidates': [{'reference_id': rid, 'position': rows[0]['publication_position']} for rid,rows in by_reference.items() if any('Proposition 4.2' in str(v) for row in rows for v in row.values())],
        'manifest_eta_definition_candidates': [{'reference_id': rid, 'position': rows[0]['publication_position']} for rid,rows in by_reference.items() if any('eta' in str(v).lower() and 'definition' in str(v).lower() for row in rows for v in row.values())],
        'resolution_policy': 'source identity must be explicitly checked; matching locator alone is insufficient',
    }
    path = Path('phase166_r3m_source_order_audit_results.json')
    path.write_text(json.dumps(output, ensure_ascii=False, indent=2, default=str), encoding='utf-8')
    print(json.dumps({k:v for k,v in output.items() if k not in ('unresolved_six','unmapped_references')}, ensure_ascii=False, indent=2))
    print('UNRESOLVED SIX:')
    for entry in output['unresolved_six']:
        print(json.dumps({'reference_id': entry['reference_id'], 'locator':entry['locator'], 'source_id':entry['source_id'], 'types':[a['content_type'] for a in entry['assertions']]},ensure_ascii=False))
    print('AUDIT SAVED:',path.resolve())


if __name__ == '__main__':
    main()
