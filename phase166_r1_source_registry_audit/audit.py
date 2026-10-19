"""Read-only Phase 166 R1 source/registry audit; never grants proof rights."""
import csv
import json
import re
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
HERE = Path(__file__).resolve().parent
CSV_FILE = HERE / 'sphere_relation2.csv'

PREFIXES = (
    ('external_tag', re.compile(r'^\s*\[[^]]+\]')),
    ('toda_proposition', re.compile(r'^\s*(?:Prop(?:osition)?\.?\s*)(\d+)\.(\d+)(?:\b|\s|,)\s*', re.I)),
    ('toda_lemma', re.compile(r'^\s*(?:Lem(?:ma)?\.?\s*)(\d+)\.(\d+)(?:\b|\s|,)\s*', re.I)),
    ('toda_equation', re.compile(r'^\s*\((\d+)\.(\d+)\)')),
    ('page_reference', re.compile(r'^\s*p\.?\s*\d+\b', re.I)),
)


def classify(value):
    source = (value or '').strip()
    if not source:
        return 'missing', ''
    for kind, pattern in PREFIXES:
        match = pattern.match(source)
        if match:
            if kind == 'toda_proposition':
                return kind, f'Proposition {match.group(1)}.{match.group(2)}'
            if kind == 'toda_lemma':
                return kind, f'Lemma {match.group(1)}.{match.group(2)}'
            if kind == 'toda_equation':
                return kind, f'({match.group(1)}.{match.group(2)})'
            return kind, ''
    return 'other_unparsed', ''


def load_rows(path):
    with path.open(encoding='utf-8-sig', newline='') as stream:
        return list(csv.DictReader(stream))


def get_registry():
    """Use production discovery, not an invented static statement inventory."""
    try:
        from phase165_r4_production_connection import discover_production_registry
        bridge = discover_production_registry().bridge
        return bridge, None
    except (ImportError, ModuleNotFoundError, AttributeError, ValueError, TypeError, RuntimeError) as exc:
        return None, f'{type(exc).__name__}: {exc}'


def inspect(rows, bridge):
    refs = {}
    if bridge is not None:
        for ref in bridge.registry._references.values():
            refs.setdefault(ref.locator.strip(), []).append(ref)
    details = []
    counts = Counter()
    for number, row in enumerate(rows, start=2):
        source = (row.get('reference') or '').strip()
        category, locator = classify(source)
        matches = refs.get(locator, ()) if locator else ()
        assert_ids = []
        for ref in matches:
            assert_ids.extend(a.assertion_id for a in bridge.registry.assertions_for(ref.reference_id))
        # Locator-level candidates do not establish assertion-level equality.
        status = ('locator_candidates_only' if matches else
                  'unmatched_locator' if locator else 'unparsed_or_missing')
        counts[category] += 1
        details.append({
            'csv_line': number,
            'n': row.get('n', ''),
            'k': row.get('k', ''),
            'source_text': source,
            'category': category,
            'proposed_locator': locator,
            'match_status': status,
            'reference_ids': [x.reference_id for x in matches],
            'candidate_assertion_ids': assert_ids,
            'typed_relation_verified': False,
            'mathematical_equivalence_verified': False,
            'citation_eligible': False,
            'proof_step_granted': False,
        })
    return details, counts


def main():
    rows = load_rows(CSV_FILE)
    bridge, error = get_registry()
    details, counts = inspect(rows, bridge)
    output = {
        'phase': '166 R1 source-registry audit',
        'read_only': True,
        'rows': len(rows),
        'classified': dict(sorted(counts.items())),
        'registry_available': bridge is not None,
        'registry_error': error,
        'candidate_locator_rows': sum(bool(row['reference_ids']) for row in details),
        'candidate_assertion_rows': sum(bool(row['candidate_assertion_ids']) for row in details),
        'verified_relation_rows': 0,
        'granted_proof_steps': 0,
        'policy': 'A locator match is not a proof or an asserted equality; citation rights remain denied.',
        'full_pytest_run': False,
    }
    (HERE / 'audit_result.json').write_text(json.dumps(output, ensure_ascii=False, indent=2), encoding='utf-8')
    with (HERE / 'row_matches.csv').open('w', encoding='utf-8-sig', newline='') as stream:
        writer = csv.DictWriter(stream, fieldnames=details[0].keys())
        writer.writeheader()
        for row in details:
            writer.writerow({k: json.dumps(v, ensure_ascii=False) if isinstance(v, list) else v for k, v in row.items()})
    print(json.dumps(output, ensure_ascii=False, indent=2))
    if error:
        print('ERROR: Production registry unavailable; candidate matching NOT performed.')
        return 2
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
