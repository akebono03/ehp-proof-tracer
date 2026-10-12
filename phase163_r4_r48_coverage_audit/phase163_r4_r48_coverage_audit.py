"""R4-R48: read-only, conservative coverage audit of the R4-R47 TeX catalog.

A candidate is a review prompt, never a validated mathematical statement.
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
START = re.compile(r'\\begin\{(theorem|proposition|lemma|corollary|definition|remark|equation)\}')
DISPLAY = re.compile(r'\\\[|\\begin\{(align\*?|gather\*?|multline\*?|displaymath|equation\*?|flalign\*?)\}')
CUES = re.compile(r'定義する|と定める|とおく|と置く|を定義|と呼ぶ|という|\\(?:textbf|emph)\{(?:定義|Definition)\}')
INLINE_MATH = re.compile(r'(?<!\\)\$|\\\(|\\\[|\\(?:pi|alpha|beta|eta|nu|Delta|Omega|Ex|pit|pis|todai|mathbb)\b')


def clean_source(source: str) -> str:
    """Strip non-escaped TeX comments, keeping original line positions."""
    lines = []
    for line in source.splitlines(keepends=True):
        i = 0
        while i < len(line):
            if line[i] == '%':
                j = i - 1
                while j >= 0 and line[j] == '\\':
                    j -= 1
                if (i - j - 1) % 2 == 0:
                    line = line[:i] + ('\n' if line.endswith('\n') else '')
                    break
            i += 1
        lines.append(line)
    return ''.join(lines)


def span_end(clean: str, match: re.Match[str]) -> tuple[int, bool]:
    kind = match.group(1)
    close = re.search(r'\\end\{' + re.escape(kind) + r'\}', clean[match.end():])
    return ((match.end() + close.end(), False) if close else (len(clean), True))


def containing(spans: list[tuple[int, int]], start: int, end: int) -> bool:
    return any(a <= start and end <= b for a, b in spans)


def classify_chapter(chapter: int, raw: bytes, registered: list[dict]) -> tuple[list[dict], dict]:
    source = raw.decode('utf-8-sig')
    clean = clean_source(source)
    registered_by_start = {x['source_line']: x for x in registered}
    registered_spans = []
    all_spans = []
    conflicts = []
    for m in START.finditer(clean):
        end, unclosed = span_end(clean, m)
        line = clean.count('\n', 0, m.start()) + 1
        all_spans.append((m.start(), end, m.group(1), line))
        matching = registered_by_start.get(line)
        if matching is None or matching['kind'] != m.group(1):
            conflicts.append({'chapter': chapter, 'line': line, 'reason': 'UNMATCHED_ENVIRONMENT'})
            continue
        body = clean[m.start():end]
        if hashlib.sha256(body.encode('utf-8')).hexdigest() != matching['sha256_tex_body']:
            conflicts.append({'chapter': chapter, 'line': line, 'reason': 'BODY_HASH_MISMATCH'})
            continue
        if unclosed:
            conflicts.append({'chapter': chapter, 'line': line, 'reason': 'UNCLOSED_ENVIRONMENT'})
        registered_spans.append((m.start(), end))
    if len(registered_spans) != len(registered):
        conflicts.append({'chapter': chapter, 'reason': 'REGISTERED_COUNT_MISMATCH',
                          'expected': len(registered), 'found': len(registered_spans)})
    if conflicts:
        raise ValueError('Catalog/source discrepancy: ' + json.dumps(conflicts, ensure_ascii=False))
    rows = []
    def add(kind: str, pos: int, excerpt: str, reason: str) -> None:
        line = clean.count('\n', 0, pos) + 1
        rows.append({'chapter': chapter, 'source_line': line, 'category': kind,
                     'reason': reason, 'excerpt': excerpt.strip()[:260],
                     'review_status': 'UNREVIEWED'})
    # Every registered nested equation is covered by its parent. Report, do not duplicate.
    nested = []
    for a, b, kind, line in all_spans:
        parents = [(p, q, parent_kind, parent_line) for p, q, parent_kind, parent_line in all_spans
                   if p < a and b <= q]
        if parents:
            nested.append({'chapter': chapter, 'source_line': line, 'kind': kind,
                           'parent_kind': parents[-1][2], 'parent_line': parents[-1][3],
                           'action': 'RETAIN_EXISTING_SOURCE_UNIT'})
    for m in DISPLAY.finditer(clean):
        if m.group(0) == r'\[':
            close = clean.find(r'\]', m.end())
            if close < 0:
                add('UNMATCHED_DISPLAY', m.start(), clean[m.start():m.start()+130], 'MISSING_DISPLAY_END')
                continue
            end = close + 2
        else:
            name = m.group(1)
            cm = re.search(r'\\end\{' + re.escape(name) + r'\}', clean[m.end():])
            if cm is None:
                add('UNMATCHED_DISPLAY', m.start(), clean[m.start():m.start()+130], 'MISSING_DISPLAY_END')
                continue
            end = m.end() + cm.end()
        if containing(registered_spans, m.start(), end):
            continue
        add('OUTSIDE_DISPLAY', m.start(), clean[m.start():min(end, m.start()+220)],
            'DISPLAY_OUTSIDE_REGISTERED_ENVIRONMENT')
    # Line-based prose cues are intentionally suggestive, not asserted to be definitions.
    for m in re.finditer(r'[^\n]+', clean):
        line = m.group(0)
        if containing(registered_spans, m.start(), m.end()):
            continue
        if CUES.search(line) and INLINE_MATH.search(line):
            add('PROSE_DEFINITION_CUE', m.start(), line, 'DEFINITION_WORD_AND_MATH')
    counts = dict(sorted(Counter(x['category'] for x in rows).items()))
    return rows, {'chapter': chapter, 'registered_count': len(registered),
                  'nested_count': len(nested), 'nested': nested,
                  'candidate_counts': counts}


def audit(catalog: dict, inputs: Path) -> dict:
    items = catalog['items']
    if len(items) != 108 or any(not x['TEX_REGISTERED'] for x in items):
        raise ValueError('Unexpected registered source catalog')
    if [x['publication_position'] for x in items] != list(range(1, len(items)+1)):
        raise ValueError('Publication positions changed')
    all_rows = []
    chapters = []
    for chapter, filename in CHAPTER_FILES.items():
        path = inputs / filename
        raw = path.read_bytes()
        if hashlib.sha256(raw).hexdigest() != catalog['source_sha256'][str(chapter)]:
            raise ValueError('Source SHA-256 mismatch: ' + filename)
        subset = [x for x in items if x['chapter'] == chapter]
        rows, info = classify_chapter(chapter, raw, subset)
        chapters.append(info)
        all_rows.extend(rows)
    return {'phase': '163 R4-R48', 'mode': 'READ_ONLY_COVERAGE_AUDIT',
            'registered_count': len(items),
            'existing_reference_count': len(catalog['existing_reference_ids']),
            'existing_assertion_count': len(catalog['existing_assertion_ids']),
            'source_sha256': catalog['source_sha256'],
            'candidate_count': len(all_rows),
            'candidate_counts': dict(sorted(Counter(r['category'] for r in all_rows).items())),
            'nested_registered_environment_count': sum(x['nested_count'] for x in chapters),
            'chapters': chapters, 'candidates': all_rows,
            'candidate_semantics_verified': False,
            'registration_applied': False,
            'registry_modified': False, 'ids_allocated': False,
            'proof_search_connected': False}


def write_report(report: dict, output: Path) -> None:
    output.mkdir(parents=True, exist_ok=True)
    (output / 'audit.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    with (output / 'candidates.csv').open('w', encoding='utf-8-sig', newline='') as f:
        cols = ['chapter', 'source_line', 'category', 'reason', 'excerpt', 'review_status']
        writer = csv.DictWriter(f, fieldnames=cols)
        writer.writeheader()
        writer.writerows(report['candidates'])
    with (output / 'report.md').open('w', encoding='utf-8') as f:
        f.write('# Phase 163 R4-R48 カバレッジ監査\n\n')
        f.write('候補は未審査であり、独立命題・定義の存在を確定したものではない。\n\n')
        f.write(f"登録済み環境：{report['registered_count']}、未審査候補：{report['candidate_count']}、入れ子環境：{report['nested_registered_environment_count']}\n\n")
        for chapter in report['chapters']:
            f.write(f"- 第{chapter['chapter']}章：登録済み{chapter['registered_count']}、入れ子{chapter['nested_count']}\n")
        f.write('\n## 候補分類\n\n')
        for name, count in report['candidate_counts'].items():
            f.write(f'- {name}: {count}\n')
        f.write('\n既存 ID・TeX・登録カタログは変更していない。\n')


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument('--catalog', type=Path, required=True)
    parser.add_argument('--inputs', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    catalog = json.loads(args.catalog.read_text(encoding='utf-8-sig'))
    report = audit(catalog, args.inputs)
    write_report(report, args.output)
    print(json.dumps({k: v for k, v in report.items() if k not in ('chapters', 'candidates')}, ensure_ascii=False, indent=2))
    print('Coverage candidates written:', args.output)


if __name__ == '__main__':
    main()
