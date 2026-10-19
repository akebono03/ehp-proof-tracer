"""Phase 166 R2: read-only generator/group correspondence inventory."""
from __future__ import annotations
import argparse
import csv
import json
from collections import Counter, defaultdict
from pathlib import Path


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open('r', encoding='utf-8-sig', newline='') as stream:
        return list(csv.DictReader(stream))


def parse_ids(value: str) -> tuple[int, ...] | None:
    try:
        return tuple(int(part) for part in value.split()) if value.strip() else ()
    except ValueError:
        return None


def inspect(generator_rows: list[dict[str, str]], sphere_rows: list[dict[str, str]]) -> tuple[dict, list[dict]]:
    ids: dict[int, list[dict]] = defaultdict(list)
    for record in generator_rows:
        try:
            ids[int(record['id'])].append(record)
        except (ValueError, KeyError):
            continue
    output: list[dict] = []
    counts = Counter()
    for index, row in enumerate(sphere_rows, start=2):
        raw = row.get('Element', '')
        elements = parse_ids(raw)
        if elements is None:
            status = 'INVALID_ELEMENT_ENCODING'
            resolved = []
            counts[status] += 1
        else:
            resolved = [ids.get(i, []) for i in elements]
            if not elements:
                status = 'EMPTY_ELEMENT'
            elif any(len(found) == 0 for found in resolved):
                status = 'UNKNOWN_GENERATOR_ID'
            elif any(len(found) > 1 for found in resolved):
                status = 'DUPLICATE_GENERATOR_ID'
            else:
                status = 'GENERATOR_IDS_RESOLVED_NOT_CERTIFIED'
            counts[status] += 1
        mismatch = False
        if status == 'GENERATOR_IDS_RESOLVED_NOT_CERTIFIED' and len(elements) == 1:
            gen = resolved[0][0]
            # k,n describe the base generator; suspensions/composites can shift degree.
            # Only flag obvious differences for manual review, never reject them as false.
            mismatch = (row.get('generator', '') == '' or gen.get('display', '') == '')
        output.append({
            'csv_line': index,
            'n': row.get('n', ''), 'k': row.get('k', ''),
            'component_id': row.get('id', ''),
            'generator_text': row.get('generator', ''),
            'element_ids': raw,
            'generator_base_names': ' | '.join('/'.join(g['display'] for g in hits) for hits in resolved),
            'status': status,
            'display_missing': mismatch,
            'mathematical_identity_confirmed': False,
            'proof_permission_granted': False,
        })
    focus = [r for r in output if (r['n'],r['k']) in {('2','1'),('3','1'),('3','2'),('3','3')}]
    summary = {
        'phase': '166 R2 generator/group correspondence', 'read_only': True,
        'generator_rows': len(generator_rows), 'sphere_rows': len(sphere_rows),
        'distinct_generator_ids': len(ids),
        'duplicate_generator_ids': sum(len(v)-1 for v in ids.values()),
        'status_counts': dict(sorted(counts.items())),
        'focus_rows': focus,
        'claim': 'Element identifier join only; no proof of generator identity, orders, suspensions or group structure',
        'mathematical_identity_confirmed': 0,
        'proof_permission_granted': 0, 'production_code_modified': False,
        'full_pytest_run': False,
    }
    return summary, output


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument('--repo', type=Path, default=Path.cwd())
    ap.add_argument('--output', type=Path, default=Path(__file__).resolve().parent / 'results')
    args = ap.parse_args()
    def locate(filename: str) -> Path:
        candidates = [args.repo / filename, args.repo / 'data' / filename, Path(__file__).resolve().parent.parent / filename]
        for candidate in candidates:
            if candidate.is_file():
                return candidate
        raise FileNotFoundError(f'{filename} not found; inspected: {candidates}')
    generators = read_csv(locate('HyoujiGen.csv'))
    sphere = read_csv(locate('sphere(3).csv'))
    summary, records = inspect(generators, sphere)
    args.output.mkdir(parents=True, exist_ok=True)
    (args.output / 'summary.json').write_text(json.dumps(summary, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    with (args.output / 'correspondence.csv').open('w', encoding='utf-8-sig', newline='') as stream:
        writer = csv.DictWriter(stream, fieldnames=list(records[0].keys()))
        writer.writeheader()
        writer.writerows(records)
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
