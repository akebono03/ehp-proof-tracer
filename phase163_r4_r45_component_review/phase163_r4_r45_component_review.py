"""Phase 163 R4-R45: read-only TeX evidence packets for existing assertions.

Reference matches do not imply semantic matches. No inferred component order or ID.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
from collections import Counter
from pathlib import Path
from typing import Any

PRIORITY = (
    'toda:Proposition 5.1', 'toda:Proposition 5.3',
    'toda:Proposition 5.6', 'toda:(5.1)', 'toda:(5.3)',
)


def check_inputs(crosswalk: dict[str, Any], extraction: dict[str, Any], mapping: dict[str, Any], inputs: Path) -> None:
    if crosswalk.get('phase') != '163 R4-R44' or crosswalk.get('mode') != 'READ_ONLY_ASSERTION_CROSSWALK':
        raise ValueError('R4-R44 crosswalk is required')
    if extraction.get('phase') != '163 R4-R42' or mapping.get('phase') != '163 R4-R43':
        raise ValueError('R4-R42 extraction and R4-R43 mapping required')
    if any(crosswalk.get(k) is not False for k in ('registration_applied', 'id_allocated', 'proof_search_connected')):
        raise ValueError('crosswalk is not read-only')
    if len(crosswalk['reference_units']) != crosswalk['source_count']:
        raise ValueError('reference unit count mismatch')
    if len(crosswalk['assertion_crosswalk']) != crosswalk['existing_assertion_count']:
        raise ValueError('assertion count mismatch')
    if crosswalk['source_sha256'] != mapping['source_sha256']:
        raise ValueError('mapping source fingerprints mismatch')
    source_map = {}
    for chapter in extraction['chapters']:
        actual = inputs / chapter['source_file']
        if not actual.is_file() or hashlib.sha256(actual.read_bytes()).hexdigest() != chapter['sha256']:
            raise ValueError(f'TeX missing or changed: {actual}')
        source_map[str(chapter['chapter'])] = chapter['sha256']
    if source_map != crosswalk['source_sha256']:
        raise ValueError('extraction source fingerprints mismatch')
    tex_map = {(item['chapter'], item['order']): item for chapter in extraction['chapters'] for item in chapter['items']}
    seen = set()
    for unit in crosswalk['reference_units']:
        key = unit['chapter'], unit['source_order']
        if key not in tex_map or key in seen:
            raise ValueError('missing or repeated source unit')
        seen.add(key)
        if tex_map[key]['tex'] != unit['tex_body']:
            raise ValueError('TeX body differs from extraction')
        if hashlib.sha256(unit['tex_body'].encode('utf-8')).hexdigest() != unit['sha256_tex_body']:
            raise ValueError('TeX body fingerprint mismatch')
    if len(seen) != len(tex_map):
        raise ValueError('source unit omissions')


def make_review(crosswalk: dict[str, Any], extraction: dict[str, Any]) -> dict[str, Any]:
    """Create evidence-only review packets; never assert a semantic match."""
    units_by_ref = {u['existing_reference_id']: u for u in crosswalk['reference_units']
                    if u['existing_reference_id'] is not None}
    if len(units_by_ref) != crosswalk['existing_reference_count']:
        raise ValueError('duplicate existing reference mapping')
    assertions = crosswalk['assertion_crosswalk']
    ids = [a['assertion_id'] for a in assertions]
    if len(ids) != len(set(ids)):
        raise ValueError('duplicate assertion IDs')
    for a in assertions:
        if a['reference_id'] not in units_by_ref or a['match_level'] != 'REFERENCE_ONLY':
            raise ValueError('unexpected pre-confirmed assertion match')
    packages = []
    for rid in PRIORITY:
        if rid not in units_by_ref:
            raise ValueError(f'priority reference unavailable: {rid}')
        unit = units_by_ref[rid]
        group = [a for a in assertions if a['reference_id'] == rid]
        if not group:
            raise ValueError(f'priority reference has no assertion: {rid}')
        # Source line is the beginning of the extraction environment; preserve raw TeX exactly.
        tex_lines = unit['tex_body'].splitlines()
        indexed_lines = [{'line': unit['source_line'] + i, 'tex': line} for i, line in enumerate(tex_lines)]
        packages.append({
            'reference_id': rid, 'chapter': unit['chapter'],
            'source_order': unit['source_order'], 'source_line': unit['source_line'],
            'sha256_tex_body': unit['sha256_tex_body'],
            'tex_lines': indexed_lines,
            'assertions': [{
                'assertion_id': a['assertion_id'],
                'component_position_existing': a['component_position_existing'],
                'scope_existing': a['scope_existing'],
                'content_type': a['content_type'],
                'candidate_span_start': None, 'candidate_span_end': None,
                'match_level': 'REFERENCE_ONLY', 'component_order_confirmed_from_tex': False,
                'review_status': 'NEEDS_SEMANTIC_REVIEW',
            } for a in group],
        })
    reviewed_ids = {a['assertion_id'] for p in packages for a in p['assertions']}
    remainder = [{
        'reference_id': a['reference_id'], 'assertion_id': a['assertion_id'],
        'component_position_existing': a['component_position_existing'],
        'match_level': 'REFERENCE_ONLY', 'review_status': 'NOT_IN_PRIORITY_SET',
    } for a in assertions if a['assertion_id'] not in reviewed_ids]
    if len(reviewed_ids) + len(remainder) != len(assertions):
        raise ValueError('assertion accounting mismatch')
    return {
        'phase': '163 R4-R45', 'mode': 'READ_ONLY_COMPONENT_EVIDENCE',
        'source_sha256': crosswalk['source_sha256'],
        'total_assertions': len(assertions), 'priority_reference_count': len(packages),
        'priority_assertion_count': len(reviewed_ids),
        'other_assertion_count': len(remainder),
        'existing_position_count': sum(a['component_position_existing'] is not None for a in assertions),
        'unknown_position_count': sum(a['component_position_existing'] is None for a in assertions),
        'semantic_matches_confirmed': 0, 'positions_newly_confirmed': 0,
        'packets': packages, 'remaining_assertions': remainder,
        'registration_applied': False, 'id_allocated': False,
        'proof_search_connected': False, 'source_verified': False,
    }


def write_output(result: dict[str, Any], output: Path) -> None:
    output.mkdir(parents=True, exist_ok=True)
    (output / 'review.json').write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    rows = []
    for p in result['packets']:
        for a in p['assertions']:
            rows.append({'reference_id': p['reference_id'], 'chapter': p['chapter'],
                         'source_order': p['source_order'], 'source_line': p['source_line'],
                         **a})
    with (output / 'priority_assertions.csv').open('w', newline='', encoding='utf-8-sig') as file:
        writer = csv.DictWriter(file, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    lines = ['# Phase 163 R4-R45 個別主張の本文照合資料', '',
             f"- 既存 Assertion 総数: {result['total_assertions']}",
             f"- 優先対象: {result['priority_reference_count']} Reference / {result['priority_assertion_count']} Assertion",
             f"- その他: {result['other_assertion_count']} Assertion",
             '- 本文の位置と個別主張の意味的一致は未確認。推測による順序変更なし。',
             '- Reference の TeX を行番号付きで収録。校閲後に明示的な span を確定する。', '']
    for p in result['packets']:
        lines.extend([f"## {p['reference_id']}", '',
                      f"章 {p['chapter']}、章内順序 {p['source_order']}、開始行 {p['source_line']}", '',
                      '### 既存 Assertion', '',
                      '| Assertion ID | 既存 component_position | 状態 |', '|---|---:|---|'])
        for a in p['assertions']:
            pos = a['component_position_existing']
            lines.append(f"| `{a['assertion_id']}` | {pos if pos is not None else '未設定'} | 要意味照合 |")
        lines.extend(['', '### TeX 本文（行番号付き）', '', '```tex'])
        lines.extend(f"% line {line['line']}\n{line['tex']}" for line in p['tex_lines'])
        lines.extend(['```', ''])
    (output / 'review.md').write_text('\n'.join(lines), encoding='utf-8')


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument('--crosswalk', type=Path, required=True)
    parser.add_argument('--extraction', type=Path, required=True)
    parser.add_argument('--mapping', type=Path, required=True)
    parser.add_argument('--inputs', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    crosswalk = json.loads(args.crosswalk.read_text(encoding='utf-8'))
    extraction = json.loads(args.extraction.read_text(encoding='utf-8'))
    mapping = json.loads(args.mapping.read_text(encoding='utf-8'))
    check_inputs(crosswalk, extraction, mapping, args.inputs)
    result = make_review(crosswalk, extraction)
    write_output(result, args.output)
    print(json.dumps({k: v for k, v in result.items() if k not in ('packets', 'remaining_assertions')},
                     indent=2, ensure_ascii=False))
    print('No registry/source changes; full pytest suite not run.')


if __name__ == '__main__':
    main()
