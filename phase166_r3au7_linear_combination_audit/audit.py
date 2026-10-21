"""Read-only inspection of the 23 multi-coefficient sphere.csv rows."""
from __future__ import annotations

import argparse
import csv
import json
from collections import Counter, defaultdict
from pathlib import Path


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open(encoding='utf-8-sig', newline='') as handle:
        return list(csv.DictReader(handle))


def parse_integers(value: str) -> list[int] | None:
    try:
        return [int(item) for item in (value or '').split()]
    except ValueError:
        return None


def inspect(rows: list[dict[str, str]]) -> tuple[dict, list[dict]]:
    groups = defaultdict(dict)
    for row in rows:
        if not (row.get('n') or '').strip() or not (row.get('k') or '').strip():
            continue
        try:
            key = (int(row['n']), int(row['k']))
            group_id = int(row['id'])
        except (ValueError, TypeError, KeyError):
            continue
        groups[key].setdefault(group_id, []).append(row)
    details = []
    status_counts = Counter()
    for csv_line, row in enumerate(rows, start=2):
        coefficients = parse_integers(row.get('gen_coe', ''))
        if coefficients is None:
            continue
        terms = [(index, coe) for index, coe in enumerate(coefficients) if coe]
        if len(terms) < 2:
            continue
        try:
            key = (int(row['n']), int(row['k']))
            current_id = int(row['id'])
        except (ValueError, KeyError):
            continue
        matching = groups[key]
        targets = []
        for index, coe in terms:
            candidates = matching.get(index, [])
            if not candidates:
                state = 'MISSING_COMPONENT_ID'
            elif len(candidates) > 1:
                state = 'DUPLICATE_COMPONENT_ID'
            else:
                state = 'MATCHED_BY_ID'
            targets.append({
                'position_zero_based': index,
                'coefficient': coe,
                'target_component_id': index,
                'status': state,
                'target_Element': candidates[0].get('Element', '') if len(candidates) == 1 else '',
                'target_generator_reference_optional': candidates[0].get('generator', '') if len(candidates) == 1 else '',
                'self_reference': index == current_id,
            })
            status_counts[state] += 1
        details.append({
            'csv_line': csv_line, 'n': key[0], 'k': key[1],
            'component_id': current_id,
            'orders': row.get('orders', ''),
            'Element': row.get('Element', ''),
            'gen_coe': row.get('gen_coe', ''),
            'reference_generator_optional': row.get('generator', ''),
            'nonzero_terms': len(terms),
            'coefficient_terms_by_id': json.dumps(targets, ensure_ascii=False),
            'all_component_ids_present': all(t['status'] == 'MATCHED_BY_ID' for t in targets),
            'contains_self_reference': any(t['self_reference'] for t in targets),
            'meaning_certified': False,
            'typed_expression_built': False,
        })
    summary = {
        'phase': '166 R3-AU-7',
        'total_input_rows': len(rows),
        'multi_nonzero_rows': len(details),
        'nonzero_coefficient_terms': sum(x['nonzero_terms'] for x in details),
        'component_lookup_status': dict(sorted(status_counts.items())),
        'rows_with_all_component_ids_present': sum(x['all_component_ids_present'] for x in details),
        'rows_with_self_reference': sum(x['contains_self_reference'] for x in details),
        'zero_vector_rows_intentionally_out_of_scope': True,
        'reference_generator_optional': True,
        'matching_rule': 'zero-based nonzero coefficient position is matched to same (n,k) component id (hypothesis under audit)',
        'meaning_certified': False,
        'typed_expression_built': False,
        'production_code_modified': False,
        'full_pytest_run': False,
    }
    return summary, details


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument('--repo', type=Path, default=Path.cwd())
    parser.add_argument('--output', type=Path, default=Path(__file__).resolve().parent / 'results')
    args = parser.parse_args()
    candidates = [args.repo / 'data' / 'sphere.csv', args.repo / 'sphere.csv']
    source = next((item for item in candidates if item.is_file()), None)
    if source is None:
        raise FileNotFoundError('sphere.csv not found in repository data/ or root')
    summary, details = inspect(read_rows(source))
    summary['source_csv'] = str(source)
    args.output.mkdir(parents=True, exist_ok=True)
    (args.output / 'summary.json').write_text(json.dumps(summary, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    with (args.output / 'multi_coefficient_rows.csv').open('w', encoding='utf-8-sig', newline='') as stream:
        fields = ['csv_line', 'n', 'k', 'component_id', 'orders', 'Element', 'gen_coe',
                  'reference_generator_optional', 'nonzero_terms', 'coefficient_terms_by_id',
                  'all_component_ids_present', 'contains_self_reference', 'meaning_certified',
                  'typed_expression_built']
        writer = csv.DictWriter(stream, fieldnames=fields)
        writer.writeheader()
        writer.writerows(details)
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
