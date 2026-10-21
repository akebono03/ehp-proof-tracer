"""Read-only diagnostics for group-local gen_coe positions (Phase 166 R3-AU-6)."""
from __future__ import annotations
import argparse
import csv
import json
from collections import Counter, defaultdict
from pathlib import Path


def inspect(rows: list[dict[str, str]]) -> tuple[dict, list[dict]]:
    groups: dict[tuple[str, str], list[dict[str, str]]] = defaultdict(list)
    for row in rows:
        try:
            int(row['n']); int(row['k']); int(row['id'])
        except (ValueError, KeyError, TypeError):
            continue
        groups[(row['n'], row['k'])].append(row)
    records = []
    counts = Counter()
    for (n, k), parts in sorted(groups.items(), key=lambda x: (int(x[0][1]), int(x[0][0]))):
        parts = sorted(parts, key=lambda r: int(r['id']))
        ids = [int(part['id']) for part in parts]
        if len(set(ids)) != len(ids):
            counts['groups_with_duplicate_component_id'] += 1
        group_statuses = set()
        for index, part in enumerate(parts):
            try:
                pairs = json.loads(part['gen_coe_nonzero_positions_zero_based'])
                coe = [int(c) for c in part['gen_coe'].split()]
                valid = isinstance(pairs, list)
            except (ValueError, KeyError, TypeError, json.JSONDecodeError):
                pairs, coe, valid = [], [], False
            nonzero = [(int(i), int(c)) for i, c in pairs] if valid else []
            if not valid or len(coe) != 12:
                status = 'MALFORMED_OR_EMPTY'
            elif not nonzero:
                status = 'ZERO_VECTOR'
            elif len(nonzero) > 1:
                status = 'MULTIPLE_NONZERO'
            elif abs(nonzero[0][1]) != 1:
                status = 'SCALED_SINGLE'
            elif nonzero[0][0] == index:
                status = 'MATCHES_SORTED_POSITION'
            else:
                status = 'OTHER_UNIT_POSITION'
            counts['rows_' + status] += 1
            group_statuses.add(status)
            records.append({'n': n, 'k': k, 'component_id': part['id'],
                            'sorted_position_zero_based': index,
                            'group_component_ids_sorted': json.dumps(ids),
                            'coefficient_nonzero_position_and_value': json.dumps(nonzero),
                            'Element': part.get('Element', ''), 'classification': status,
                            'generator_reference_optional': part.get('reference_generator_optional', ''),
                            'coefficient_basis_mapping_certified': False})
        counts['groups_total'] += 1
        if any(status != 'MATCHES_SORTED_POSITION' for status in group_statuses):
            counts['groups_with_nonidentity_or_special_rows'] += 1
        if len(parts) > 1:
            counts['groups_with_multiple_rows'] += 1
    return {'phase': '166 R3-AU-6', 'source': 'R3-AU-5 all_rows.csv',
            'counts': dict(sorted(counts.items())),
            'scope': 'empirical group-local sorted-component-index versus nonzero gen_coe position',
            'mapping_certified': False, 'composition_degree_certified': False,
            'typed_expression_certified': False, 'generator_reference_is_optional': True,
            'production_code_modified': False, 'full_pytest_run': False}, records


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument('--repo', type=Path, default=Path.cwd())
    parser.add_argument('--source', type=Path)
    parser.add_argument('--output', type=Path, default=Path(__file__).resolve().parent / 'results')
    args = parser.parse_args()
    source = args.source or args.repo / 'phase166_r3au5_db_convention_audit' / 'results' / 'all_rows.csv'
    with source.open(encoding='utf-8-sig', newline='') as stream:
        summary, records = inspect(list(csv.DictReader(stream)))
    args.output.mkdir(parents=True, exist_ok=True)
    (args.output / 'summary.json').write_text(json.dumps(summary, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    with (args.output / 'all_mapping_rows.csv').open('w', encoding='utf-8-sig', newline='') as stream:
        writer = csv.DictWriter(stream, fieldnames=list(records[0]) if records else ['n','k','component_id'])
        writer.writeheader(); writer.writerows(records)
    with (args.output / 'exceptions_and_special_rows.csv').open('w', encoding='utf-8-sig', newline='') as stream:
        writer = csv.DictWriter(stream, fieldnames=list(records[0]) if records else ['n','k','component_id'])
        writer.writeheader(); writer.writerows(row for row in records if row['classification'] != 'MATCHES_SORTED_POSITION')
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
