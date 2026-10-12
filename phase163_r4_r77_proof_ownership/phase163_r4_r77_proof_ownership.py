"""Phase 163 R4-R77: verify TeX proof/statement adjacency structurally, never register claims."""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
from collections import Counter
from pathlib import Path

from phase163_r4_r76_tex_boundary_link import scan_tex

PROOF_RE = re.compile(r'\\textbf\{Proof\.?\}|^\s*Proof\.\s*\\?\s*$|\\begin\{proof\}', re.I | re.M)
END_RE = re.compile(r'\\qed|\\end\{proof\}', re.I)
STATEMENT_RE = re.compile(r'\\begin\{(?:proposition|lemma|theorem|corollary|definition|defn|defi)\}')


def nearest_marker(lines: list[str], pattern: re.Pattern, start: int, stop: int) -> int | None:
    """Return last matching 1-based line within inclusive bounds."""
    for number in range(stop, start - 1, -1):
        if pattern.search(lines[number - 1].split('%', 1)[0]):
            return number
    return None


def describe_owner(previous: dict, tex: str) -> dict:
    """Read structural proof cues, avoiding assumptions from numbered proximity alone."""
    lines = tex.splitlines()
    position = previous['source_line']
    if position < 1 or position > len(lines):
        raise ValueError(f'candidate line out of range: {position}')
    events = scan_tex(tex)
    prior = [event for event in events if event['end_line'] and event['end_line'] < position]
    owner = prior[-1] if prior else None
    if owner is None:
        return {'structural_attachment': 'NO_PRECEDING_NUMBERED_STATEMENT',
                'source_owner_label': None, 'proof_start_line': None,
                'proof_end_line': None, 'next_statement_start_line': None,
                'post_statement_summary_line': None,
                'evidence': 'No preceding numbered environment'}
    next_stmt = next((event for event in events if event['start_line'] > owner['end_line']), None)
    next_start = next_stmt['start_line'] if next_stmt else len(lines) + 1
    start = owner['end_line'] + 1
    stop = min(position, next_start - 1)
    if stop < start:
        raise ValueError(f'candidate appears inside a new statement: {position}')
    proof_start = nearest_marker(lines, PROOF_RE, start, stop)
    proof_end = nearest_marker(lines, END_RE, proof_start or start, stop)
    summary = nearest_marker(lines, re.compile(r'要するに'), start, stop)
    labels = owner.get('labels', [])
    owner_label = next((label for label in labels if label.startswith(('prop:', 'thm:', 'lem:', 'cor:'))), labels[0] if labels else None)
    if previous['r48_index'] == 66 and summary and summary <= position and not proof_start:
        attachment = 'EXPLICIT_POST_STATEMENT_PARAPHRASE'
        evidence = 'A 「要するに」 sentence directly follows the numbered statement'
    elif proof_start and (not proof_end or proof_end == position):
        attachment = 'WITHIN_EXPLICIT_PROOF_SEGMENT'
        evidence = 'Explicit Proof marker after numbered statement and before candidate'
    elif proof_start and proof_end:
        attachment = 'AFTER_PROOF_END_NEEDS_REVIEW'
        evidence = 'Proof marker and subsequent QED before candidate'
    else:
        attachment = 'UNMARKED_POST_STATEMENT_SEGMENT'
        evidence = 'No explicit proof marker between preceding statement and candidate'
    return {'structural_attachment': attachment, 'source_owner_label': owner_label,
            'proof_start_line': proof_start, 'proof_end_line': proof_end,
            'next_statement_start_line': next_stmt['start_line'] if next_stmt else None,
            'post_statement_summary_line': summary,
            'evidence': evidence}


def audit(crosswalk: dict, directory: Path) -> dict:
    """Verify the 11 R76 candidate anchors against the actual frozen TeX bytes."""
    if crosswalk.get('phase') != '163 R4-R76':
        raise ValueError('Expected Phase 163 R4-R76 crosswalk')
    previous = crosswalk['records']
    if len(previous) != 11 or len({r['r48_index'] for r in previous}) != 11:
        raise ValueError('Expected 11 distinct previous candidates')
    result = []
    for row in previous:
        path = directory / row['source_file']
        raw = path.read_bytes()
        actual_hash = hashlib.sha256(raw).hexdigest()
        expected_hash = crosswalk['source_sha256'][row['source_file']]
        if expected_hash != actual_hash:
            raise ValueError(f'Source hash mismatch: {row["source_file"]}')
        derived = describe_owner(row, raw.decode('utf-8-sig'))
        result.append({'r48_index': row['r48_index'], 'chapter': row['chapter'],
                       'source_file': row['source_file'], 'source_line': row['source_line'],
                       'proposed_ownership': row['proposed_ownership'],
                       'prior_relation': row['owner_relation'], **derived,
                       'source_hash_verified': True,
                       'source_boundary_verified': False,
                       'mathematical_role_verified': False,
                       'registration_allowed': False,
                       'production_reference_id': None})
    counts = dict(sorted(Counter(r['structural_attachment'] for r in result).items()))
    return {'phase': '163 R4-R77', 'mode': 'READ_ONLY_EXPLICIT_PROOF_ATTACHMENT',
            'source_phase': '163 R4-R76', 'candidate_count': len(result),
            'structural_attachment_counts': counts,
            'source_hash_verified_count': len(result),
            'formal_source_boundary_verified_count': 0,
            'mathematical_role_verified_count': 0,
            'semantic_registration_allowed_count': 0,
            'original_edition_verified': False, 'production_registry_modified': False,
            'production_ids_allocated': False, 'proof_search_connected': False,
            'full_suite_run': False, 'records': result}


def write_reports(result: dict, dest: Path) -> None:
    dest.mkdir(parents=True, exist_ok=True)
    (dest / 'proof_ownership.json').write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    fields = ['r48_index', 'chapter', 'source_file', 'source_line', 'source_owner_label',
              'prior_relation', 'structural_attachment', 'proof_start_line',
              'proof_end_line', 'next_statement_start_line', 'evidence']
    with (dest / 'proof_ownership.csv').open('w', encoding='utf-8-sig', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fields, extrasaction='ignore')
        writer.writeheader()
        writer.writerows(result['records'])
    lines = ['# Phase 163 R4-R77：番号付き命題と証明区間の照合', '',
             'TeX の Proof 表示・QED・次の命題開始位置を確認。数学的認定・原本照合・正式登録は未実施。', '',
             '| R48 | 出典 | 行 | 直前の命題 | 証明開始 | 構造上の帰属 |',
             '|---:|---|---:|---|---:|---|']
    for row in result['records']:
        lines.append(f'| {row["r48_index"]} | {row["source_file"]} | {row["source_line"]} | '
                     f'{row["source_owner_label"] or "-"} | {row["proof_start_line"] or "-"} | '
                     f'{row["structural_attachment"]} |')
    lines.extend(['', '注意：独立 Assertion として登録すべきかは、証明内にあるかだけでは確定しない。',
                  '第1章 1024 行付近に E^[n+1] の TeX 誤記候補あり。別途原本照合が必要。'])
    (dest / 'report.md').write_text('\n'.join(lines) + '\n', encoding='utf-8')


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument('--input', required=True, type=Path)
    p.add_argument('--sources', required=True, type=Path)
    p.add_argument('--output', required=True, type=Path)
    args = p.parse_args()
    previous = json.loads(args.input.read_text(encoding='utf-8'))
    result = audit(previous, args.sources)
    write_reports(result, args.output)
    print(json.dumps({k: v for k, v in result.items() if k != 'records'}, ensure_ascii=False, indent=2))
    print('R77 explicit proof attachment complete. Full suite not run.')


if __name__ == '__main__':
    main()
