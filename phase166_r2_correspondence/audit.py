"""Phase 166 R2: non-mutating relationship/citation correspondence audit."""
from __future__ import annotations
import csv
import json
import re
import sys
from collections import Counter
from dataclasses import fields, is_dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
HERE = Path(__file__).resolve().parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from phase166_r1_source_registry_audit.audit import classify


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding='utf-8-sig', newline='') as f:
        return list(csv.DictReader(f))


def _meaningful(value: object) -> bool:
    return str(value if value is not None else '').strip().lower() not in ('', 'nan', 'none')


def _kind(value: object) -> str:
    if is_dataclass(value) and not isinstance(value, type):
        return type(value).__module__ + '.' + type(value).__name__
    return type(value).__module__ + '.' + type(value).__name__


def _locator_index(bridge: object) -> dict[str, list[object]]:
    results: dict[str, list[object]] = {}
    for item in bridge.registry._references.values():
        results.setdefault(item.locator.strip(), []).append(item)
    return results


def analyze(rows: list[dict[str, str]], bridge: object) -> tuple[list[dict[str, object]], dict[str, object]]:
    index = _locator_index(bridge)
    details: list[dict[str, object]] = []
    counts: Counter[str] = Counter()
    for number, row in enumerate(rows, start=2):
        category, locator = classify(row.get('reference', ''))
        references = index.get(locator, []) if locator else []
        candidates = [(ref, a) for ref in references for a in bridge.registry.assertions_for(ref.reference_id)]
        typed_candidates = [(ref, a) for ref, a in candidates if is_dataclass(a.content) and not isinstance(a.content, type)]
        if not references:
            status = 'NO_LOCATOR_MATCH' if locator else 'NO_PARSED_LOCATOR'
        elif not candidates:
            status = 'REFERENCE_ONLY'
        elif not typed_candidates:
            status = 'ASSERTION_NOT_STRUCTURED'
        else:
            status = 'TYPED_ASSERTION_CANDIDATE'
        counts[status] += 1
        details.append({
            'csv_line': number,
            'source_text': row.get('reference', ''),
            'category': category,
            'locator': locator,
            'n': row.get('n', ''),
            'k': row.get('k', ''),
            'composition': row.get('composition', ''),
            'rep_linear': row.get('rep_linear', ''),
            'has_composition_and_rep_linear': _meaningful(row.get('composition')) and _meaningful(row.get('rep_linear')),
            'reference_ids': [ref.reference_id for ref in references],
            'assertion_ids': [a.assertion_id for _, a in candidates],
            'assertion_content_types': [_kind(a.content) for _, a in candidates],
            'origin_values': [str(a.origin.value) for _, a in candidates],
            'typed_assertion_ids': [a.assertion_id for _, a in typed_candidates],
            'correspondence_status': status,
            'mathematical_identity_confirmed': False,
            'relation_type_confirmed': False,
            'generator_typing_confirmed': False,
            'proof_permission_granted': False,
        })
    summary = {
        'phase': '166 R2', 'mode': 'read_only', 'total_rows': len(rows),
        'status_counts': dict(sorted(counts.items())),
        'locator_matched_rows': sum(bool(x['reference_ids']) for x in details),
        'assertion_candidate_rows': sum(bool(x['assertion_ids']) for x in details),
        'typed_assertion_candidate_rows': sum(bool(x['typed_assertion_ids']) for x in details),
        'potential_expression_pair_rows': sum(x['has_composition_and_rep_linear'] for x in details),
        'mathematical_identity_confirmed': 0, 'proof_permission_granted': 0,
        'production_code_modified': False, 'full_pytest_run': False,
        'interpretation': 'Candidate links are not certified mathematical identities. Source text and display expressions are not parsed into typed Relations.',
    }
    return details, summary


def main() -> int:
    # A missing production registry is an audit failure, not a passing empty match.
    from phase165_r4_production_connection import discover_production_registry
    bridge = discover_production_registry().bridge
    source = ROOT / 'phase166_r1_source_registry_audit' / 'sphere_relation2.csv'
    if not source.is_file():
        source = ROOT / 'sphere_relation2.csv'
    if not source.is_file():
        raise FileNotFoundError('sphere_relation2.csv not found in R1 folder or project root')
    rows = read_csv(source)
    if len(rows) != 687:
        raise ValueError(f'Expected 687 source rows for this R2 audit, got {len(rows)}')
    details, summary = analyze(rows, bridge)
    out_dir = HERE / 'results'
    out_dir.mkdir(exist_ok=True)
    with (out_dir / 'correspondence.csv').open('w', encoding='utf-8-sig', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=details[0].keys())
        writer.writeheader()
        for item in details:
            writer.writerow({k: json.dumps(v, ensure_ascii=False) if isinstance(v, list) else v for k, v in item.items()})
    (out_dir / 'summary.json').write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
