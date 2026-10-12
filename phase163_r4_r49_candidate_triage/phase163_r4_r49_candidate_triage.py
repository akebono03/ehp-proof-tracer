"""Phase 163 R4-R49: read-only lexical triage of R4-R48 review candidates.

No mathematical claim is certified and no statement is registered here.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
from collections import Counter
from pathlib import Path

CHAPTER_FILES = {
    1: 'Toda_01_corrected.tex',
    2: 'Toda_02_2(2).tex',
    3: 'Toda_03_2(2).tex',
    4: 'Toda_04_2(2).tex',
    5: 'Toda_05_2(6).tex',
}
# These are TeX tokens, not ordinary text delimiters.  A double backslash
# followed by [2mm] is a line break with spacing, never a display opener.
DISPLAY_OPEN = re.compile(r'(?<!\\)\\\[|\\begin\{(align\*?|gather\*?|multline\*?|displaymath|equation\*?|flalign\*?)\}')


def strip_comments(source: str) -> str:
    cleaned = []
    for line in source.splitlines(keepends=True):
        for index, char in enumerate(line):
            if char != '%':
                continue
            backslashes = 0
            j = index - 1
            while j >= 0 and line[j] == '\\':
                backslashes += 1
                j -= 1
            if backslashes % 2 == 0:
                line = line[:index] + ('\n' if line.endswith('\n') else '')
                break
        cleaned.append(line)
    return ''.join(cleaned)


def parse_displays(source: str) -> list[dict]:
    """Find well-formed display intervals, keeping nested environments explicit."""
    clean = strip_comments(source)
    found = []
    for match in DISPLAY_OPEN.finditer(clean):
        kind = match.group(1)
        if kind is None:
            end_at = clean.find(r'\]', match.end())
            end = end_at + 2 if end_at >= 0 else None
            token = 'bracket'
        else:
            closing = re.search(r'\\end\{' + re.escape(kind) + r'\}', clean[match.end():])
            end = match.end() + closing.end() if closing else None
            token = kind
        if end is None:
            continue
        start_line = clean.count('\n', 0, match.start()) + 1
        found.append({'start': match.start(), 'end': end, 'line': start_line,
                      'token': token})
    return found


def _line_offsets(source: str) -> list[int]:
    offsets = [0]
    for line in source.splitlines(keepends=True):
        offsets.append(offsets[-1] + len(line))
    return offsets


def triage(audit: dict, catalog: dict, inputs: Path) -> dict:
    """Create a fully accounted, stable review queue from all R4-R48 candidates."""
    if audit.get('phase') != '163 R4-R48' or catalog.get('phase') != '163 R4-R47':
        raise ValueError('Expected R4-R48 audit and R4-R47 catalog')
    if audit.get('candidate_count') != len(audit.get('candidates', [])):
        raise ValueError('R4-R48 candidate count mismatch')
    if len(catalog['items']) != 108 or audit['registered_count'] != 108:
        raise ValueError('Existing 108 units must remain fixed')
    if [x['publication_position'] for x in catalog['items']] != list(range(1, 109)):
        raise ValueError('Catalog publication positions changed')
    if audit['source_sha256'] != catalog['source_sha256']:
        raise ValueError('Audit/catalog source checksums differ')
    catalog_snapshot = hashlib.sha256(json.dumps(catalog, ensure_ascii=False, sort_keys=True).encode('utf-8')).hexdigest()
    prepared = {}
    for chapter, filename in CHAPTER_FILES.items():
        raw = (inputs / filename).read_bytes()
        if hashlib.sha256(raw).hexdigest() != catalog['source_sha256'][str(chapter)]:
            raise ValueError('TeX source digest mismatch: ' + filename)
        source = raw.decode('utf-8-sig')
        cleaned = strip_comments(source)
        spans = parse_displays(source)
        offsets = _line_offsets(cleaned)
        prepared[chapter] = (cleaned, spans, offsets)
    queue = []
    first_for_unit = {}
    for index, candidate in enumerate(audit['candidates'], start=1):
        chapter = int(candidate['chapter'])
        source, spans, offsets = prepared[chapter]
        line = int(candidate['source_line'])
        if not 1 <= line < len(offsets):
            raise ValueError('Candidate line outside source')
        excerpt = candidate['excerpt']
        category = candidate['category']
        line_content = source[offsets[line-1]:offsets[line]]
        candidate_token = 'bracket' if excerpt.startswith(r'\[') else None
        if excerpt.startswith(r'\begin{'):
            candidate_token = re.match(r'\\begin\{([^}]+)\}', excerpt).group(1)
        interval = next((s for s in spans if s['line'] == line and s['token'] == candidate_token), None)
        # A valid outer display owns inner aligned environments. A malformed
        # R4-R48 pseudo-opener is not admitted as a mathematical candidate.
        if category == 'OUTSIDE_DISPLAY' and interval is None:
            status = 'LEXICAL_FALSE_POSITIVE'
            group_id = None
            reason = 'R4-R48 opener not recognized as an independent TeX display'
        elif category == 'OUTSIDE_DISPLAY':
            parents = [s for s in spans if s is not interval and s['start'] < interval['start']
                       and interval['end'] <= s['end']]
            owner = min(parents, key=lambda s: s['start']) if parents else interval
            group_id = f"tex-display:ch{chapter:02d}:line{owner['line']:05d}"
            if owner is not interval:
                status = 'NESTED_DISPLAY_FRAGMENT'
                reason = 'Already represented by surrounding display block'
            elif group_id in first_for_unit:
                status = 'DUPLICATE_DISPLAY_FRAGMENT'
                reason = 'Review block was already emitted'
            else:
                status = 'DISPLAY_REVIEW_REQUIRED'
                reason = 'Independent display block; semantic role not established'
                first_for_unit[group_id] = index
        elif category == 'PROSE_DEFINITION_CUE':
            status = 'DEFINITION_CUE_REVIEW_REQUIRED'
            group_id = f'tex-prose:ch{chapter:02d}:line{line:05d}'
            reason = 'Definition-like prose; mathematical independence unverified'
        else:
            status = 'OTHER_REVIEW_REQUIRED'
            group_id = f'tex-other:ch{chapter:02d}:line{line:05d}'
            reason = 'Candidate type not adjudicated'
        # Source context is source text, not a synthesized interpretation.
        source_lines = source.splitlines()
        context_start = max(1, line-3)
        context_end = min(len(source_lines), line+5)
        context = '\n'.join(f'{n}: {source_lines[n-1]}' for n in range(context_start, context_end+1))
        queue.append({'r48_index': index, 'chapter': chapter, 'source_line': line,
                      'original_category': category, 'triage_status': status,
                      'review_group_id': group_id,
                      'group_primary_r48_index': first_for_unit.get(group_id),
                      'reason': reason, 'excerpt': excerpt,
                      'context': context, 'review_decision': 'UNREVIEWED'})
    counts = dict(sorted(Counter(x['triage_status'] for x in queue).items()))
    return {'phase': '163 R4-R49', 'mode': 'READ_ONLY_LEXICAL_TRIAGE',
            'registered_source_count': 108,
            'original_candidate_count': len(queue),
            'status_counts': counts,
            'distinct_display_review_count': counts.get('DISPLAY_REVIEW_REQUIRED', 0),
            'definition_cue_review_count': counts.get('DEFINITION_CUE_REVIEW_REQUIRED', 0),
            'source_sha256': catalog['source_sha256'],
            'catalog_snapshot_sha256': catalog_snapshot,
            'mathematical_independence_reviewed': False,
            'new_statement_count_confirmed': 0,
            'registration_applied': False,
            'registry_modified': False,
            'ids_allocated': False,
            'proof_search_connected': False,
            'review_queue': queue}


def save_report(report: dict, target: Path) -> None:
    target.mkdir(parents=True, exist_ok=True)
    (target / 'triage.json').write_text(json.dumps(report, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
    columns = ['r48_index', 'chapter', 'source_line', 'original_category',
               'triage_status', 'review_group_id', 'group_primary_r48_index',
               'reason', 'excerpt', 'context', 'review_decision']
    with (target / 'review_queue.csv').open('w', encoding='utf-8-sig', newline='') as stream:
        writer = csv.DictWriter(stream, fieldnames=columns)
        writer.writeheader()
        writer.writerows(report['review_queue'])
    with (target / 'report.md').open('w', encoding='utf-8') as stream:
        stream.write('# Phase 163 R4-R49 候補整理監査\n\n')
        stream.write('機械的な TeX 字句整理のみ。独立命題・定義・証明途中の式の数学的判定は未実施。\n\n')
        stream.write(f"- 元候補：{report['original_candidate_count']}件\n")
        stream.write(f"- 表示数式のレビュー単位：{report['distinct_display_review_count']}件\n")
        stream.write(f"- 定義らしい文章：{report['definition_cue_review_count']}件\n")
        for status, count in report['status_counts'].items():
            stream.write(f'- {status}：{count}件\n')
        stream.write('\n## 注記\n\n')
        stream.write('同じ表示の入れ子・改行指定の誤認は整理するが、文献にある独立命題の数は確定しない。\n')
        stream.write('既存108環境、23 Reference、67 Assertion と出典 TeX は変更しない。\n')


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument('--audit', type=Path, required=True)
    parser.add_argument('--catalog', type=Path, required=True)
    parser.add_argument('--inputs', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    audit_data = json.loads(args.audit.read_text(encoding='utf-8-sig'))
    catalog_data = json.loads(args.catalog.read_text(encoding='utf-8-sig'))
    result = triage(audit_data, catalog_data, args.inputs)
    save_report(result, args.output)
    print(json.dumps({k: v for k, v in result.items() if k != 'review_queue'}, ensure_ascii=False, indent=2))
    print('R4-R49 review queue:', args.output)


if __name__ == '__main__':
    main()
