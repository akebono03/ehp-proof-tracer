from __future__ import annotations

import json
from dataclasses import fields, is_dataclass
from pathlib import Path

from phase168_r3_38_frozen_fulltext_audit import audit as frozen
from phase168_r3_39f_frozen_comparison import audit as prior

OUT = Path(__file__).resolve().parent / 'output'
CASES = (("pi3_2", 2, 1), ("pi4_3", 3, 1), ("pi5_4", 4, 1))


def describe(value, depth=0):
    if value is None or isinstance(value, (str, int, float, bool)):
        return value
    if depth >= 3:
        return {'type': type(value).__name__, 'repr': str(value)[:400]}
    if isinstance(value, (list, tuple)):
        return [describe(v, depth + 1) for v in value[:30]]
    if is_dataclass(value):
        return {'type': type(value).__name__, 'fields': {
            f.name: describe(getattr(value, f.name), depth + 1) for f in fields(value)
        }}
    return {'type': type(value).__name__, 'repr': str(value)[:400]}


def main():
    OUT.mkdir(exist_ok=True)
    frozen.OUT = OUT
    report = []
    for name, n, k in CASES:
        comparison = frozen.compare(name, n, k)
        current = (OUT / f'{name}_current.md').read_text(encoding='utf-8')
        _, proof = frozen.sections(current)
        report.append({
            'case': name,
            'checks': prior.assess(name, proof),
            'diff': comparison['comparison'],
            'reference': comparison['reference_entries'],
        })
    (OUT / 'audit.json').write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')
    for row in report:
        print(row['case'], 'checks:', sum(i['present'] for i in row['checks']), '/', len(row['checks']))
    print('OUTPUT:', OUT)


if __name__ == '__main__':
    main()
