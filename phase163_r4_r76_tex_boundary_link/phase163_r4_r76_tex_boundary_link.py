"""Read-only crosswalk from R75 candidates to actual TeX structural boundaries."""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
from collections import Counter
from pathlib import Path

THEOREM_KINDS = frozenset({'proposition', 'lemma', 'theorem', 'corollary', 'definition', 'defn', 'defi'})
BEGIN_RE = re.compile(r'\\begin\{(proposition|lemma|theorem|corollary|definition|defn|defi)\}')
END_RE = re.compile(r'\\end\{(proposition|lemma|theorem|corollary|definition|defn|defi)\}')
LABEL_RE = re.compile(r'\\label\{([^}]+)\}')
PROOF_RE = re.compile(r'\\(?:begin\{proof\}|textbf\{Proof\.?\}|noindent\s*\\textbf\{Proof\.?\})', re.I)
QED_RE = re.compile(r'\\(?:qed|end\{proof\})')


def scan_tex(text: str) -> list[dict]:
    lines = text.splitlines()
    events = []
    active = None
    for line_number, line in enumerate(lines, 1):
        clean = line.split('%', 1)[0]
        begin = BEGIN_RE.search(clean)
        if begin:
            if active is not None:
                active['warnings'].append('NESTED_THEOREM_BEGIN')
                events.append(active)
            active = {'kind': begin.group(1), 'start_line': line_number,
                      'end_line': None, 'labels': [], 'warnings': []}
        if active is not None:
            active['labels'].extend(LABEL_RE.findall(clean))
        end = END_RE.search(clean)
        if end and active is not None:
            if end.group(1) != active['kind']:
                active['warnings'].append('MISMATCHED_THEOREM_END')
            active['end_line'] = line_number
            events.append(active)
            active = None
    if active is not None:
        active['warnings'].append('UNCLOSED_THEOREM')
        events.append(active)
    return events


def locate_candidate(proposal: dict, text: str) -> dict:
    lines = text.splitlines()
    lineno = proposal['source_line']
    if not isinstance(lineno, int) or lineno < 1 or lineno > len(lines):
        return {'position_status': 'LINE_OUT_OF_RANGE', 'nearest_numbered_owner': None,
                'owner_relation': 'UNRESOLVED', 'owner_kind': None, 'owner_labels': [],
                'owner_start_line': None, 'owner_end_line': None,
                'proof_marker_between': False, 'end_marker_between': False}
    events = scan_tex(text)
    enclosing = next((x for x in events if x['start_line'] <= lineno <= (x['end_line'] or len(lines))), None)
    prev = next((x for x in reversed(events) if x['end_line'] is not None and x['end_line'] < lineno), None)
    owner = enclosing or prev
    between = '\n'.join(lines[(prev['end_line'] if prev else 0):lineno]) if not enclosing else ''
    proof_marker = bool(PROOF_RE.search(between))
    end_marker = bool(QED_RE.search(between))
    if enclosing:
        relation = 'INSIDE_NUMBERED_BODY'
    elif prev and end_marker:
        relation = 'AFTER_QED_UNOWNED'
    elif prev and proof_marker:
        relation = 'POSSIBLE_PROOF_OF_PRECEDING'
    elif prev:
        relation = 'AFTER_PRECEDING_STATEMENT_UNRESOLVED'
    else:
        relation = 'BEFORE_FIRST_NUMBERED_STATEMENT'
    return {'position_status': 'LINE_LOCATED',
            'nearest_numbered_owner': '|'.join(owner['labels']) if owner else None,
            'owner_relation': relation,
            'owner_kind': owner['kind'] if owner else None,
            'owner_labels': owner['labels'] if owner else [],
            'owner_start_line': owner['start_line'] if owner else None,
            'owner_end_line': owner['end_line'] if owner else None,
            'proof_marker_between': proof_marker, 'end_marker_between': end_marker,
            'owner_scan_warnings': owner['warnings'] if owner else []}


def audit(data: dict, source_directory: Path) -> dict:
    proposals = data['focused_proposals']
    if len(proposals) != 11 or len({p['r48_index'] for p in proposals}) != 11:
        raise ValueError('R75 focused proposals must contain 11 unique candidates')
    rows = []
    source_hashes = {}
    for p in proposals:
        source_file = p['source_file']
        source_path = source_directory / source_file
        row = {'r48_index': p['r48_index'], 'chapter': p['chapter'],
               'source_file': source_file, 'source_line': p['source_line'],
               'proposed_ownership': p['proposed_ownership'],
               'provisional_group': p['provisional_group'],
               'excerpt_sha256': p['excerpt_sha256'],
               'source_boundary_verified': False,
               'mathematical_role_verified': False,
               'registration_allowed': False}
        if source_path.is_file():
            raw = source_path.read_bytes()
            source_hashes[source_file] = hashlib.sha256(raw).hexdigest()
            row.update(locate_candidate(p, raw.decode('utf-8-sig')))
        else:
            row.update({'position_status': 'SOURCE_MISSING', 'owner_relation': 'UNRESOLVED',
                        'nearest_numbered_owner': None, 'owner_kind': None,
                        'owner_labels': [], 'owner_start_line': None,
                        'owner_end_line': None, 'proof_marker_between': False,
                        'end_marker_between': False})
        rows.append(row)
    counts = dict(sorted(Counter(row['owner_relation'] for row in rows).items()))
    return {'phase': '163 R4-R76', 'mode': 'READ_ONLY_TEX_NUMBERED_BOUNDARY_CROSSWALK',
            'source_phase': '163 R4-R75', 'candidate_count': len(rows),
            'source_sha256': source_hashes, 'owner_relation_counts': counts,
            'line_located_count': sum(r['position_status'] == 'LINE_LOCATED' for r in rows),
            'formal_source_boundary_verified_count': 0,
            'mathematical_role_verified_count': 0,
            'semantic_registration_allowed_count': 0,
            'original_edition_verified': False, 'production_registry_modified': False,
            'production_ids_allocated': False, 'proof_search_connected': False,
            'full_suite_run': False, 'records': rows}


def write_reports(result: dict, dest: Path) -> None:
    dest.mkdir(parents=True, exist_ok=True)
    (dest / 'numbered_boundary_crosswalk.json').write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    columns = ['r48_index', 'chapter', 'source_file', 'source_line', 'proposed_ownership',
               'provisional_group', 'position_status', 'owner_relation', 'owner_kind',
               'nearest_numbered_owner', 'owner_start_line', 'owner_end_line',
               'proof_marker_between', 'end_marker_between', 'excerpt_sha256']
    with (dest / 'numbered_boundary_crosswalk.csv').open('w', encoding='utf-8-sig', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=columns, extrasaction='ignore')
        writer.writeheader()
        writer.writerows(result['records'])
    lines = ['# Phase 163 R4-R76：番号付き命題との構造的境界照合', '',
             'TeX 上の構造位置だけを機械的に照合。数学的・原本上の帰属を正式認定しない。', '',
             f'- 対象: {result["candidate_count"]}件',
             f'- 出典行を特定: {result["line_located_count"]}件',
             '- 正式な境界検証・Registry 変更・ID 採番: 0件', '',
             '| R48 | 章 | 行 | 命題環境 | 直近ラベル | 構造上の位置 |',
             '|---:|---:|---:|---|---|---|']
    for row in result['records']:
        lines.append(f'| {row["r48_index"]} | {row["chapter"]} | {row["source_line"]} | '
                     f'{row.get("owner_kind") or "-"} | {row.get("nearest_numbered_owner") or "-"} | '
                     f'{row["owner_relation"]} |')
    lines.extend(['', '注意：本文中の Proof マーカーや \\qed の存在は確定的な帰属を意味しません。',
                  '原本照合と意味の判断は後続段階で実施します。'])
    (dest / 'report.md').write_text('\n'.join(lines) + '\n', encoding='utf-8')


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', type=Path, required=True)
    parser.add_argument('--sources', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    data = json.loads(args.input.read_text(encoding='utf-8-sig'))
    result = audit(data, args.sources)
    write_reports(result, args.output)
    print(json.dumps({key: value for key, value in result.items() if key != 'records'}, ensure_ascii=False, indent=2))
    if result['line_located_count'] != 11:
        raise SystemExit('ERROR: all 11 candidates must locate an actual source line')


if __name__ == '__main__':
    main()
