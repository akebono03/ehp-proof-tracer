"""Phase 163 R4-R74: read-only editorial review of R73's 65 unresolved rows."""
from __future__ import annotations

import csv
import hashlib
import json
from collections import Counter
from pathlib import Path

DEFINITION_COMPONENT = frozenset({107, 108, 121, 138, 154, 218})
UNNUMBERED_ASSERTION = frozenset({120, 122, 123, 140})
CONSTRUCTION_CONTEXT = frozenset({143, 144})
HOLD = frozenset({66, 67, 68, 69, 133, 142, 256})
PROOF_CONTEXT = frozenset({
    45, 48, 59, 111, 112, 113, 114, 115, 116, 128, 130, 131,
    132, 134, 135, 145, 146, 147, 156, 158, 161, 167, 169, 172,
    183, 206, 209, 210, 211, 215, 219, 221, 222, 224, 225, 226,
    227, 229, 233, 234, 236, 237, 263, 265, 266, 268,
})
PROPOSALS = {
    'DEFINITION_COMPONENT_REVIEW': DEFINITION_COMPONENT,
    'UNNUMBERED_ASSERTION_REVIEW': UNNUMBERED_ASSERTION,
    'PROOF_CONTEXT_REVIEW': PROOF_CONTEXT,
    'PROOF_CONSTRUCTION_REVIEW': CONSTRUCTION_CONTEXT,
    'HOLD_BOUNDARY_REVIEW': HOLD,
}
EXPLANATIONS = {
    'DEFINITION_COMPONENT_REVIEW': '定義・写像・記号の構成範囲に属する可能性。定義の正式な境界は未確定。',
    'UNNUMBERED_ASSERTION_REVIEW': '一般的な関係・同型として独立 Assertion の可能性。番号付き本文との包含関係は未確認。',
    'PROOF_CONTEXT_REVIEW': '前後の証明・推論・特殊化への帰属を優先する候補。独立 Reference かどうかは未確認。',
    'PROOF_CONSTRUCTION_REVIEW': '局所的な写像・図式の構成要素の可能性。正式な定義としては未判定。',
    'HOLD_BOUNDARY_REVIEW': '命題の言い換え、証明の結論、または複数主張の境界が不明なため保留。',
}


def review(previous: dict) -> dict:
    if previous.get('phase') != '163 R4-R73' or previous.get('source_phase') != '163 R4-R72':
        raise ValueError('Expected genuine R73 data')
    rows = previous.get('records')
    if not isinstance(rows, list) or len(rows) != 237:
        raise ValueError('Expected 237 R73 records')
    identities = [r['r48_index'] for r in rows]
    if len(set(identities)) != len(identities):
        raise ValueError('Duplicate R48 index')
    pending = {r['r48_index'] for r in rows if r['proposed_role'] == 'UNREVIEWED'}
    catalog = set().union(*PROPOSALS.values())
    if len(pending) != 65 or pending != catalog or sum(map(len, PROPOSALS.values())) != 65:
        raise ValueError('Remaining candidate set changed; do not silently reclassify')
    proposals = []
    for row in rows:
        if row['proposed_role'] != 'UNREVIEWED':
            continue
        if hashlib.sha256(row['excerpt'].encode('utf-8')).hexdigest() != row['excerpt_sha256']:
            raise ValueError(f"Excerpt hash mismatch: {row['r48_index']}")
        if not row.get('context'):
            raise ValueError(f"Missing context: {row['r48_index']}")
        roles = [name for name, indices in PROPOSALS.items() if row['r48_index'] in indices]
        if len(roles) != 1:
            raise ValueError(f"Ambiguous assignment: {row['r48_index']}")
        proposals.append({
            'r48_index': row['r48_index'],
            'chapter': row['chapter'],
            'source_file': row['source_file'],
            'source_line': row['source_line'],
            'proposed_review_role': roles[0],
            'reason': EXPLANATIONS[roles[0]],
            'excerpt_sha256': row['excerpt_sha256'],
            'excerpt': row['excerpt'],
            'context': row['context'],
            'mathematical_role_verified': False,
            'registration_allowed': False,
            'production_reference_id': None,
        })
    return {
        'phase': '163 R4-R74',
        'mode': 'READ_ONLY_REMAINING_BOUNDARY_PROPOSALS',
        'source_phase': '163 R4-R73',
        'candidate_count': 237,
        'preserved_prior_editorial_proposal_count': 172,
        'new_boundary_review_proposal_count': 65,
        'role_counts': dict(sorted(Counter(x['proposed_review_role'] for x in proposals).items())),
        'unresolved_mathematical_boundaries': 65,
        'original_edition_verified': False,
        'mathematical_role_verified_count': 0,
        'production_registry_modified': False,
        'production_ids_allocated': False,
        'proof_search_connected': False,
        'full_suite_run': False,
        'preserved_prior_record_digest': hashlib.sha256(json.dumps(
            [r for r in rows if r['proposed_role'] != 'UNREVIEWED'], ensure_ascii=False, sort_keys=True
        ).encode('utf-8')).hexdigest(),
        'proposals': proposals,
    }


def write_reports(result: dict, output: Path) -> None:
    output.mkdir(parents=True, exist_ok=True)
    (output / 'remaining_boundary_proposals.json').write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    fields = ['r48_index', 'chapter', 'source_file', 'source_line', 'proposed_review_role', 'reason', 'excerpt_sha256', 'excerpt', 'context', 'mathematical_role_verified', 'registration_allowed']
    with (output / 'remaining_boundary_proposals.csv').open('w', encoding='utf-8-sig', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=fields, extrasaction='ignore')
        writer.writeheader()
        writer.writerows(result['proposals'])
    lines = ['# Phase 163 R4-R74：残る65候補の境界確認案', '', '原文の前後関係に基づく編集上の候補。数学的認定・原本照合・正式登録は未実施。', '', '## 件数', '']
    for role, count in result['role_counts'].items():
        lines.append(f'- {role}: {count}')
    lines += ['', '## 候補別の根拠', '']
    for row in result['proposals']:
        lines += [f"### R48 #{row['r48_index']}（第{row['chapter']}章 {row['source_line']}行）", '', f"- {row['proposed_review_role']}: {row['reason']}", '', '```tex', row['excerpt'], '```', '', '```text', row['context'], '```', '']
    (output / 'report.md').write_text('\n'.join(lines), encoding='utf-8')


def main() -> None:
    root = Path(__file__).resolve().parent.parent
    previous = json.loads((root / 'phase163_r4_r73_output' / 'role_decisions.json').read_text(encoding='utf-8'))
    result = review(previous)
    write_reports(result, root / 'phase163_r4_r74_output')
    print(json.dumps({key: val for key, val in result.items() if key != 'proposals'}, ensure_ascii=False, indent=2))
    print('R74 read-only boundary proposals generated. Full pytest not run.')


if __name__ == '__main__':
    main()
