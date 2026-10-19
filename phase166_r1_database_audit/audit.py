"""Phase 166 R1: read-only inventory of legacy mathematical data."""
import argparse
import csv
import json
import sqlite3
from collections import Counter
from pathlib import Path

FILES = {'sphere': 'sphere(3).csv', 'gen': 'HyoujiGen.csv', 'relation': 'sphere_relation2.csv', 'bracket': 'TBtable.csv'}


def read_csv(path):
    with path.open(encoding='utf-8-sig', newline='') as stream:
        return list(csv.DictReader(stream))


def summarize(directory):
    rows = {key: read_csv(directory / filename) for key, filename in FILES.items()}
    with sqlite3.connect(f'file:{(directory / "sphere.db").resolve()}?mode=ro', uri=True) as connection:
        database_counts = {name: connection.execute(f'SELECT COUNT(*) FROM "{name}"').fetchone()[0] for name in ('sphere', 'gen', 'sphere_relation', 'TBtable')}
    relation = rows['relation']
    bracket = rows['bracket']
    result = {
        'phase': '166 R1',
        'read_only': True,
        'csv_rows': {key: len(value) for key, value in rows.items()},
        'database_rows': database_counts,
        'relation': {
            'source_nonempty': sum(bool(item['reference'].strip()) for item in relation),
            'source_missing': sum(not item['reference'].strip() for item in relation),
            'distinct_source_strings': len({item['reference'] for item in relation if item['reference'].strip()}),
            'n_missing': sum(not item['n'].strip() for item in relation),
            'composition_nonempty': sum(bool(item['composition'].strip()) for item in relation),
            'rep_linear_nonempty': sum(bool(item['rep_linear'].strip()) for item in relation),
            'complete_row_duplicates': len(relation) - len({tuple(item.items()) for item in relation}),
            'order_values': dict(sorted(Counter(item['order'] for item in relation).items())),
            'columns': list(relation[0]) if relation else [],
        },
        'bracket': {
            'source_nonempty': sum(bool(item['reference'].strip()) for item in bracket),
            'bracket_text_nonempty': sum(bool(item['TodaBracket'].strip()) for item in bracket),
        },
        'proof_permission': 'NONE_GRANTED: origin and citation eligibility require independent verification',
        'full_pytest_run': False,
    }
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--data-dir', type=Path, default=Path(__file__).resolve().parent / 'data')
    parser.add_argument('--output', type=Path, default=Path(__file__).resolve().parent / 'audit_result.json')
    args = parser.parse_args()
    result = summarize(args.data_dir)
    args.output.write_text(json.dumps(result, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == '__main__':
    main()
