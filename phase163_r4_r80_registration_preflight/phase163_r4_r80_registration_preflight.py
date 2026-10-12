"""Phase 163 R4-R80: conservative fixed-statement registration preflight.

This script does not allocate production IDs or mutate the registry.
"""
from __future__ import annotations

import hashlib
import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
INPUT = ROOT / 'phase163_r4_r79_output' / 'fixed_statement_preview.json'
OUTPUT = ROOT / 'phase163_r4_r80_output'
SOURCES = ROOT / 'phase163_r4_r42_tex_extract' / 'inputs'

# These are editorial assertion identifiers, not permanent IDs.
ORDER = {
    'prop:1-6': ['last_argument_additivity', 'middle_argument_additivity', 'first_argument_additivity'],
    'thm:2.4': ['odd_dimension_case', 'even_dimension_case'],
    'prop:2.5': ['delta_composition', 'whitehead_product_case'],
    'prop:4.2': ['ehp_exact_sequence'],
}
SHARED_SCOPE = {
    'prop:1-6': 'Variables and mapping spaces are introduced on source lines 967-968 and apply to all three cases; each case has its own alternative conditions.',
    'thm:2.4': 'Prime p, m>1, and chosen continuous map h with cell-homeomorphism property on source lines 485-490 apply to both cases.',
    'prop:2.5': 'Conditions replacing inclusions by equalities occur on source lines 971-974 and govern both displayed relations.',
    'prop:4.2': 'The exact sequence is displayed as equation (4.4) inside Proposition 4.2; retain the equation label as an alias, not a duplicate assertion.',
}
EXTRA_CHECKS = {
    ('thm:2.4', 'even_dimension_case'): ['i<(p+1)m-1', '全ての $i$', '$p$-成分'],
    ('prop:2.5', 'whitehead_product_case'): ['m$ が奇数', 'j<3m-1', '2\\)-primary'],
    ('prop:1-6', 'first_argument_additivity'): ['が成り立つ. $n', 'n\\ge 1'],
}


def sha256(text: str) -> str:
    return hashlib.sha256(text.encode('utf-8')).hexdigest()


def item_suffix(item: dict) -> str:
    return item['assertion_id'].rsplit(':', 1)[-1]


def build_review(source: dict, source_root: Path) -> dict:
    fixed = source['fixed_statement_previews']
    assert len(fixed) == 8
    records = []
    seen = set()
    for owner, suffixes in ORDER.items():
        entries = [x for x in fixed if x['owner'] == owner]
        assert len(entries) == len(suffixes), owner
        by_suffix = {item_suffix(e): e for e in entries}
        assert set(by_suffix) == set(suffixes), owner
        for position, suffix in enumerate(suffixes, 1):
            item = by_suffix[suffix]
            key = (owner, suffix)
            assert key not in seen
            seen.add(key)
            path = source_root / item['source_file']
            lines = path.read_text(encoding='utf-8').splitlines()
            start, end = item['start_line'], item['end_line']
            assert 1 <= start <= end <= len(lines)
            # R79's text extraction uses newline normalisation.
            excerpt = '\n'.join(lines[start - 1:end]).strip()
            assert excerpt == item['claim_text'].strip(), (owner, suffix, 'changed TeX claim')
            assert sha256(item['claim_text']) == item['claim_sha256'], (owner, suffix)
            checks = EXTRA_CHECKS.get(key, [])
            full = item['full_statement_text']
            for token in checks:
                assert token in full or token in item['claim_text'], (key, token)
            issues = []
            if owner == 'thm:2.4' and suffix == 'even_dimension_case':
                issues.append('The even-dimensional item contains both the range-limited isomorphism and the all-degree p-component isomorphism. Consider two Assertions under the same Reference.')
            if owner == 'prop:2.5':
                issues.append('The equalities replacing inclusion relations have shared conditions (odd m, j<3m-1, or 2-primary components); do not omit them.')
            if owner == 'prop:1-6' and suffix != 'last_argument_additivity':
                issues.append('The initial variable declarations are inherited from the first item; include shared variable types in scope.')
            if owner == 'prop:1-6' and suffix == 'first_argument_additivity':
                issues.append('Extracted snippet starts with the previous item’s trailing 「が成り立つ。」; a semantic boundary adjustment is needed.')
            if owner == 'prop:4.2':
                issues.append('Equation (4.4) is embedded in Proposition 4.2. Detect duplicate Reference registration before allocating a permanent ID.')
            records.append({
                'owner': owner,
                'source_file': item['source_file'],
                'start_line': start, 'end_line': end,
                'source_claim_sha256': item['claim_sha256'],
                'proposed_assertion_key': f'proposal:{owner}:{suffix}',
                'component_position': position,
                'claim_text': item['claim_text'],
                'shared_scope_note': SHARED_SCOPE[owner],
                'boundary_issues': issues,
                'existing_registry_duplicate_status': 'NOT_CHECKED_AGAINST_ALL_PRODUCTION_REGISTRATIONS',
                'registration_allowed': False,
                'permanent_id_allocated': False,
            })
    return {
        'phase': '163 R4-R80',
        'mode': 'READ_ONLY_FIXED_STATEMENT_REGISTRATION_PREFLIGHT',
        'reference_candidate_count': len(ORDER),
        'fixed_statement_candidate_count': len(records),
        'component_position_valid_count': len(records),
        'nonempty_boundary_issue_count': sum(bool(x['boundary_issues']) for x in records),
        'scope_notes_present_count': sum(bool(x['shared_scope_note']) for x in records),
        'duplicate_status': 'UNRESOLVED',
        'semantic_registration_allowed_count': 0,
        'formal_source_boundary_verified_count': 0,
        'original_edition_verified': False,
        'production_registry_modified': False,
        'production_ids_allocated': False,
        'proof_search_connected': False,
        'full_suite_run': False,
        'records': records,
    }


def write_results(result: dict, output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / 'registration_preflight.json').write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    rows = [
        '# Phase 163 R4-R80：命題本文の正式登録前チェック',
        '',
        '登録前の条件・主張順・境界問題の監査。正式採用ではありません。',
        '',
        '| Reference | 順序 | 候補キー | 要追加確認 |',
        '|---|---:|---|---:|',
    ]
    for record in result['records']:
        rows.append(f"| {record['owner']} | {record['component_position']} | `{record['proposed_assertion_key']}` | {len(record['boundary_issues'])} |")
    rows.extend(['', '## 登録前の未解決問題', ''])
    for record in result['records']:
        for issue in record['boundary_issues']:
            rows.append(f"- `{record['proposed_assertion_key']}`: {issue}")
    rows.extend(['', '現行全 Registry との意味的重複確認・原本照合・正式な数学的検証・ID 採番は未実施。', ''])
    (output_dir / 'report.md').write_text('\n'.join(rows), encoding='utf-8')


def main() -> None:
    source = json.loads(INPUT.read_text(encoding='utf-8'))
    assert source['phase'] == '163 R4-R79'
    result = build_review(source, SOURCES)
    write_results(result, OUTPUT)
    print(json.dumps({k: v for k, v in result.items() if k != 'records'}, ensure_ascii=False, indent=2))
    print('R80 preflight complete. No production changes; full pytest not run.')


if __name__ == '__main__':
    main()
