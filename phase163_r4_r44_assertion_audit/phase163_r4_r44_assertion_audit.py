"""Phase 163 R4-R44: read-only reference/Assertion/TeX reconciliation.

A reference-level match is NOT evidence of a component-level text match.
All existing Assertion IDs remain untouched. No IDs or verification flags are issued.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def audit(mapping: dict[str, Any], extraction: dict[str, Any], registry: Any) -> dict[str, Any]:
    """Create a complete read-only crosswalk; do not infer semantic equivalence."""
    _require(mapping.get('phase') == '163 R4-R43' and mapping.get('mode') == 'READ_ONLY_MAPPING',
             'R4-R43 read-only mapping required')
    _require(extraction.get('phase') == '163 R4-R42' and extraction.get('mode') == 'READ_ONLY_EXTRACTION',
             'R4-R42 read-only extraction required')
    _require(not extraction.get('missing_sources'), 'missing TeX sources')
    _require(mapping.get('registration_applied') is False and mapping.get('id_allocated') is False,
             'prior mapping is not read-only')
    _require(extraction.get('registration_applied') is False, 'prior extraction is not read-only')

    tex_items = {(item['chapter'], item['order']): item
                 for chapter in extraction['chapters'] for item in chapter['items']}
    _require(len(tex_items) == extraction['item_count'], 'duplicated extraction position')
    _require(mapping['item_count'] == len(mapping['rows']) == len(tex_items), 'item count mismatch')
    _require(not mapping.get('duplicate_locator_candidates'), 'duplicate locator candidates')
    expected_sources = {str(group['chapter']): group['sha256'] for group in extraction['chapters']}
    _require(mapping['source_sha256'] == expected_sources, 'TeX source fingerprints differ')
    ref_entries = registry._references
    assertion_entries = registry._assertions
    mapped_positions: set[tuple[int, int]] = set()
    mapped_refs: dict[str, dict[str, Any]] = {}
    source_rows = []
    for row in mapping['rows']:
        pos = (row['chapter'], row['source_order'])
        _require(pos in tex_items and pos not in mapped_positions, f'invalid mapping position: {pos}')
        mapped_positions.add(pos)
        item = tex_items[pos]
        _require(row['kind'] == item['kind'] and row['source_line'] == item['line'],
                 f'item identity mismatch: {pos}')
        _require(row['labels'] == item['labels'] and row['tags'] == item['tags']
                 and row['locator_candidate'] == item['locator_candidate'],
                 f'locator mismatch: {pos}')
        _require(row['sha256_tex_body'] == hashlib.sha256(item['tex'].encode('utf-8')).hexdigest(),
                 f'TeX body changed: {pos}')
        _require(not row['tex_registered'] and not row['structured'] and not row['source_verified'],
                 f'unsupported R4-R43 status: {pos}')
        rid = row['existing_reference_id']
        if row['status'] == 'EXISTING_REFERENCE':
            _require(isinstance(rid, str) and rid in ref_entries, f'unknown reference: {pos}')
            _require(rid not in mapped_refs, f'duplicate reference match: {rid}')
            _require(ref_entries[rid].locator == row['locator_candidate'],
                     f'reference locator mismatch: {rid}')
            mapped_refs[rid] = row
        else:
            _require(rid is None, f'unexpected existing reference ID: {pos}')
        source_rows.append({
            'chapter': row['chapter'], 'source_order': row['source_order'],
            'source_line': row['source_line'], 'kind': row['kind'],
            'locator_candidate': row['locator_candidate'],
            'labels': row['labels'], 'existing_reference_id': rid,
            'proposed_reference_id': row['proposed_reference_id'],
            'mapping_status': row['status'],
            'unit': 'REFERENCE_WHOLE_ENVIRONMENT',
            'tex_body': item['tex'], 'sha256_tex_body': row['sha256_tex_body'],
            'tex_registered': False, 'structured': False, 'source_verified': False,
        })
    _require(mapped_positions == set(tex_items), 'mapping omits extraction items')
    _require(set(ref_entries) == set(mapped_refs), 'registry references not exactly mapped')

    assertions_by_ref: dict[str, list[Any]] = defaultdict(list)
    for assertion_id, entry in assertion_entries.items():
        _require(assertion_id == entry.assertion_id, 'assertion dictionary key mismatch')
        _require(entry.reference_id in ref_entries, f'unknown assertion reference: {assertion_id}')
        assertions_by_ref[entry.reference_id].append(entry)

    assertion_rows = []
    for rid in sorted(mapped_refs, key=lambda key: (
            mapped_refs[key]['chapter'], mapped_refs[key]['source_order'])):
        match = mapped_refs[rid]
        assertions = assertions_by_ref.get(rid, [])
        known_positions = [x.component_position for x in assertions if x.component_position is not None]
        _require(len(known_positions) == len(set(known_positions)),
                 f'duplicate component_position in {rid}')
        for entry in assertions:
            assertion_rows.append({
                'reference_id': rid, 'assertion_id': entry.assertion_id,
                'chapter': match['chapter'], 'source_order': match['source_order'],
                'source_line': match['source_line'],
                'component_position_existing': entry.component_position,
                'component_order_confirmed_from_tex': False,
                'scope_existing': entry.scope if isinstance(entry.scope, (str, int, float, bool, type(None))) else repr(entry.scope),
                'assertion_kind': entry.kind.value,
                'assertion_origin': entry.origin.value,
                'content_type': type(entry.content).__name__,
                'match_level': 'REFERENCE_ONLY',
                'tex_span_identified': False,
                'requires_semantic_review': True,
                'existing_id_preserved': True,
                'tex_registered': False,
                'source_verified': False,
            })
    _require(len(assertion_rows) == len(assertion_entries), 'some assertions were lost')
    _require({row['assertion_id'] for row in assertion_rows} == set(assertion_entries),
             'assertion ID set mismatch')
    candidates = [x for x in source_rows if x['mapping_status'] == 'NEW_REFERENCE_CANDIDATE']
    unresolved = [x for x in source_rows if x['mapping_status'] in {
        'UNNUMBERED_ENVIRONMENT', 'UNRESOLVED_SYMBOLIC_LABEL', 'UNRESOLVED_TAG'}]
    return {
        'phase': '163 R4-R44', 'mode': 'READ_ONLY_ASSERTION_CROSSWALK',
        'source_sha256': expected_sources,
        'source_count': len(source_rows),
        'existing_reference_count': len(mapped_refs),
        'existing_assertion_count': len(assertion_rows),
        'assertion_match_levels': dict(Counter(row['match_level'] for row in assertion_rows)),
        'component_positions_existing_count': sum(row['component_position_existing'] is not None for row in assertion_rows),
        'component_positions_unknown_count': sum(row['component_position_existing'] is None for row in assertion_rows),
        'new_reference_candidate_count': len(candidates),
        'unresolved_locator_count': len(unresolved),
        'reference_units': source_rows,
        'assertion_crosswalk': assertion_rows,
        'registration_applied': False, 'id_allocated': False,
        'proof_search_connected': False,
    }


def validate_tex_sources(extraction: dict[str, Any], inputs: Path) -> None:
    for chapter in extraction['chapters']:
        path = inputs / chapter['source_file']
        if not path.is_file():
            raise FileNotFoundError(f'missing TeX source: {path}')
        if hashlib.sha256(path.read_bytes()).hexdigest() != chapter['sha256']:
            raise ValueError(f'changed TeX source: {path}')


def write_report(report: dict[str, Any], output: Path) -> None:
    output.mkdir(parents=True, exist_ok=True)
    (output / 'crosswalk.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    with (output / 'assertions.csv').open('w', encoding='utf-8-sig', newline='') as stream:
        fields = list(report['assertion_crosswalk'][0]) if report['assertion_crosswalk'] else [
            'reference_id', 'assertion_id', 'match_level']
        writer = csv.DictWriter(stream, fieldnames=fields)
        writer.writeheader()
        writer.writerows(report['assertion_crosswalk'])
    with (output / 'reference_units.csv').open('w', encoding='utf-8-sig', newline='') as stream:
        fields = ['chapter', 'source_order', 'source_line', 'kind', 'locator_candidate',
                  'existing_reference_id', 'proposed_reference_id', 'mapping_status',
                  'unit', 'sha256_tex_body', 'tex_registered', 'structured', 'source_verified']
        writer = csv.DictWriter(stream, fieldnames=fields)
        writer.writeheader()
        writer.writerows({key: row[key] for key in fields} for row in report['reference_units'])
    counts = Counter(row['reference_id'] for row in report['assertion_crosswalk'])
    lines = [
        '# Phase 163 R4-R44 Assertion crosswalk', '',
        f"- TeX environments: {report['source_count']}",
        f"- Existing references: {report['existing_reference_count']}",
        f"- Existing assertions: {report['existing_assertion_count']}",
        f"- New reference candidates: {report['new_reference_candidate_count']}",
        f"- Unresolved locators: {report['unresolved_locator_count']}",
        f"- Existing component positions present: {report['component_positions_existing_count']}",
        f"- Existing component positions unknown: {report['component_positions_unknown_count']}",
        '- Existing assertion ↔ TeX span semantic equivalence is NOT verified.',
        '- All TeX registration/structured/source-verified flags remain false.',
        '- No registration, ID issuance, proof-search connection, or project source edits.',
        '', '## Assertion count by reference', '',
        '| Reference ID | Assertion count |', '|---|---:|',
    ]
    lines.extend(f'| `{rid}` | {count} |' for rid, count in sorted(counts.items()))
    lines += ['', '## Pending decisions', '',
              '1. Verify each existing component against the exact TeX span; do not infer correspondence from its name.',
              '2. Treat a whole TeX environment as a reference unit, separate from any component assertions.',
              '3. Preserve unnumbered and symbolic-label environments with chapter/source order; do not invent bibliographic numbering.',
              '4. Review definitions outside standard TeX environments before claiming complete chapter registration.', '']
    (output / 'report.md').write_text('\n'.join(lines), encoding='utf-8')


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument('--mapping', type=Path, required=True)
    parser.add_argument('--extraction', type=Path, required=True)
    parser.add_argument('--inputs', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    mapping = json.loads(args.mapping.read_text(encoding='utf-8'))
    extraction = json.loads(args.extraction.read_text(encoding='utf-8'))
    validate_tex_sources(extraction, args.inputs)
    from phase163_r4_registry_bridge import build_registry_bridge
    result = audit(mapping, extraction, build_registry_bridge().registry)
    write_report(result, args.output)
    print(json.dumps({key: value for key, value in result.items()
                      if key not in {'reference_units', 'assertion_crosswalk'}},
                     ensure_ascii=False, indent=2))
    print(f'R4-R44 output: {args.output / "crosswalk.json"}')
    print('No Registry or TeX modified. Full pytest suite not run.')


if __name__ == '__main__':
    main()
