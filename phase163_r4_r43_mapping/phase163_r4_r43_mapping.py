"""Phase 163 R4-R43: read-only TeX-to-reference mapping audit.

Reads the R4-R42 extraction; does not allocate IDs or mutate the registry.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
from collections import Counter
from pathlib import Path


def classify(item: dict, known_reference_ids: set[str]) -> dict:
    locator = item['locator_candidate']
    labels = item['labels']
    tags = item['tags']
    if locator is None:
        status = 'UNRESOLVED_SYMBOLIC_LABEL' if labels else ('UNRESOLVED_TAG' if tags else 'UNNUMBERED_ENVIRONMENT')
        reference_id = None
    else:
        reference_id = 'toda:' + locator
        status = 'EXISTING_REFERENCE' if reference_id in known_reference_ids else 'NEW_REFERENCE_CANDIDATE'
    return {
        'chapter': item['chapter'],
        'source_order': item['order'],
        'kind': item['kind'],
        'source_line': item['line'],
        'labels': labels,
        'tags': tags,
        'locator_candidate': locator,
        'existing_reference_id': reference_id if status == 'EXISTING_REFERENCE' else None,
        'proposed_reference_id': reference_id if status == 'NEW_REFERENCE_CANDIDATE' else None,
        'status': status,
        'sha256_tex_body': hashlib.sha256(item['tex'].encode('utf-8')).hexdigest(),
        'source_verified': False,
        'structured': False,
        'tex_registered': False,
    }


def build_mapping(extraction: dict, known_reference_ids: set[str], *,
                  registry_lookup: str = 'AVAILABLE') -> dict:
    if extraction.get('phase') != '163 R4-R42' or extraction.get('mode') != 'READ_ONLY_EXTRACTION':
        raise ValueError('expected R4-R42 read-only extraction')
    if extraction.get('missing_sources'):
        raise ValueError('R4-R42 extraction has missing TeX sources')
    rows = [classify(item, known_reference_ids)
            for chapter in extraction['chapters'] for item in chapter['items']]
    if len(rows) != extraction['item_count']:
        raise ValueError('inconsistent extraction item_count')
    ordered = [(row['chapter'], row['source_order']) for row in rows]
    if ordered != sorted(ordered) or len(ordered) != len(set(ordered)):
        raise ValueError('duplicate or unordered chapter/source positions')
    by_locator: dict[str, list[dict]] = {}
    for row in rows:
        if row['locator_candidate']:
            by_locator.setdefault(row['locator_candidate'], []).append(row)
    duplicates = {key: [(row['chapter'], row['source_line']) for row in matches]
                  for key, matches in by_locator.items() if len(matches) > 1}
    present = {row['existing_reference_id'] for row in rows if row['existing_reference_id']}
    return {
        'phase': '163 R4-R43', 'mode': 'READ_ONLY_MAPPING',
        'registry_lookup': registry_lookup,
        'source_sha256': {str(c['chapter']): c['sha256'] for c in extraction['chapters']},
        'item_count': len(rows), 'status_counts': dict(sorted(Counter(row['status'] for row in rows).items())),
        'matched_existing_reference_count': len(present),
        'unmatched_existing_reference_ids': sorted(known_reference_ids - present),
        'duplicate_locator_candidates': duplicates,
        'rows': rows, 'registration_applied': False, 'id_allocated': False,
        'proof_search_connected': False,
    }


def check_sources(extraction: dict, inputs_dir: Path) -> None:
    for chapter in extraction['chapters']:
        source = inputs_dir / chapter['source_file']
        if not source.is_file():
            raise FileNotFoundError(f'missing source: {source}')
        digest = hashlib.sha256(source.read_bytes()).hexdigest()
        if digest != chapter['sha256']:
            raise ValueError(f'changed TeX source: {source}')


def write_output(report: dict, output: Path) -> None:
    output.mkdir(parents=True, exist_ok=True)
    (output / 'mapping.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    columns = ['chapter', 'source_order', 'kind', 'source_line', 'status',
               'locator_candidate', 'existing_reference_id', 'proposed_reference_id',
               'labels', 'tags', 'sha256_tex_body', 'tex_registered', 'structured', 'source_verified']
    with (output / 'mapping.csv').open('w', encoding='utf-8-sig', newline='') as stream:
        writer = csv.DictWriter(stream, fieldnames=columns)
        writer.writeheader()
        for row in report['rows']:
            writer.writerow({key: json.dumps(row[key], ensure_ascii=False) if key in {'labels', 'tags'} else row[key]
                             for key in columns})
    lines = ['# Phase 163 R4-R43 mapping audit', '',
             f"- Detected environments: {report['item_count']}",
             f"- Existing references matched: {report['matched_existing_reference_count']}",
             f"- Registry lookup: {report['registry_lookup']}",
             '- No ID allocated; no Registry or TeX modified.', '',
             '## Classification counts', '']
    lines.extend(f'- {key}: {value}' for key, value in report['status_counts'].items())
    lines.extend(['', '## Unresolved items', '', '| Chapter | Order | Kind | Line | Labels | Status |',
                  '|---:|---:|---|---:|---|---|'])
    for row in report['rows']:
        if row['status'].startswith('UNRESOLVED') or row['status'] == 'UNNUMBERED_ENVIRONMENT':
            lines.append(f"| {row['chapter']} | {row['source_order']} | {row['kind']} | {row['source_line']} | {', '.join(row['labels'])} | {row['status']} |")
    lines.extend(['', '## Existing registry entries absent from extracted environments', ''])
    lines.extend(f'- `{reference_id}`' for reference_id in report['unmatched_existing_reference_ids'])
    (output / 'report.md').write_text('\n'.join(lines) + '\n', encoding='utf-8')


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument('--extraction', type=Path, required=True)
    parser.add_argument('--inputs', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    extraction = json.loads(args.extraction.read_text(encoding='utf-8'))
    check_sources(extraction, args.inputs)
    try:
        from phase163_r4_registry_bridge import build_registry_bridge
        registry = build_registry_bridge().registry
        ids = set(registry._references)
        lookup = 'AVAILABLE'
    except (ImportError, ModuleNotFoundError) as exc:
        raise SystemExit(f'Current registry is required for R4-R43 ID matching: {exc}') from exc
    report = build_mapping(extraction, ids, registry_lookup=lookup)
    write_output(report, args.output)
    print(json.dumps({k: v for k, v in report.items() if k != 'rows'}, ensure_ascii=False, indent=2))
    print(f'R4-R43 mapping written to {args.output / "mapping.json"}')
    print('No registration or ID allocation performed. Full pytest suite not run.')


if __name__ == '__main__':
    main()
