"""Phase 163 R4-R15: conservative, read-only inventory of Toda Chapter I TeX."""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
from pathlib import Path

THEOREMS = frozenset({'theorem', 'proposition', 'lemma', 'corollary', 'definition', 'notation', 'assumption', 'remark'})
MATH_ENVS = frozenset({'equation', 'align', 'gather', 'multline', 'flalign', 'eqnarray'})
BEGIN = re.compile(r'\\begin\{([A-Za-z]+\*?)\}')
LABEL = re.compile(r'\\label\{([^}]+)\}')
END_TEMPLATE = r'\\end\{%s\}'
DISPLAY = re.compile(r'(?<!\\)\\\[|(?<!\\)\\\]')
INLINE = re.compile(r'(?<!\\)\$')


def strip_comments(line: str) -> str:
    """Remove unescaped TeX comments while retaining text preceding them."""
    for i, ch in enumerate(line):
        if ch == '%' and (i == 0 or len(line[:i]) - len(line[:i].rstrip('\\')) & 1 == 0):
            return line[:i]
    return line


def extract(tex: str) -> list[dict[str, str | int]]:
    lines = [strip_comments(line) for line in tex.splitlines()]
    records: list[dict[str, str | int]] = []
    within = False
    i = 0
    while i < len(lines):
        line = lines[i]
        if '\\section*{CHAPTER I' in line:
            within = True
        if within and '\\end{document}' in line:
            break
        if not within:
            i += 1
            continue
        match = BEGIN.search(line)
        kind = ''
        env = ''
        start = i
        if match:
            env = match.group(1)
            base = env.rstrip('*')
            if base in THEOREMS:
                kind = 'named_statement'
            elif base in MATH_ENVS:
                kind = 'numbered_math' if not env.endswith('*') else 'unnumbered_math'
        if kind:
            # TeX environments can contain nested math/enumerate blocks; stop at matching end.
            depth = 0
            end_re = re.compile(END_TEMPLATE % re.escape(env))
            j = i
            while j < len(lines):
                depth += len(re.findall(r'\\begin\{' + re.escape(env) + r'\}', lines[j]))
                depth -= len(end_re.findall(lines[j]))
                if depth == 0:
                    break
                j += 1
            j = min(j, len(lines) - 1)
            body = '\n'.join(lines[i:j + 1]); labels = LABEL.findall(body)
            records.append({'category': kind, 'environment': env, 'start_line': start + 1,
                            'end_line': j + 1, 'label': labels[0] if labels else '',
                            'tex_excerpt': ' '.join(body.split())[:240], 'review_status': 'UNREVIEWED',
                            'legacy_match': 'NOT_CHECKED', 'statement_id': ''})
            i = j + 1
            continue
        # Unnumbered display formulas are separately retained, not silently discarded.
        if r'\[' in line:
            j = i
            while j < len(lines) and r'\]' not in lines[j]:
                j += 1
            j = min(j, len(lines) - 1)
            body = '\n'.join(lines[i:j + 1])
            records.append({'category': 'unnumbered_display', 'environment': r'\[...\]',
                            'start_line': i + 1, 'end_line': j + 1, 'label': '',
                            'tex_excerpt': ' '.join(body.split())[:240], 'review_status': 'UNREVIEWED',
                            'legacy_match': 'NOT_CHECKED', 'statement_id': ''})
            i = j + 1
            continue
        i += 1
    return records


def legacy_locators(path: Path | None) -> set[str]:
    if path is None or not path.exists():
        return set()
    text = path.read_text(encoding='utf-8-sig')
    return set(re.findall(r'reference_locator\s*=\s*["\']([^"\']+)', text))


def run(source: Path, out: Path, legacy: Path | None = None) -> dict:
    data = source.read_bytes()
    rows = extract(data.decode('utf-8-sig'))
    matches = legacy_locators(legacy)
    for row in rows:
        if row['label'].startswith('prop:1-'):
            suffix = row['label'].split('prop:1-', 1)[1]
            locator = 'Proposition 1.' + suffix
        elif row['label'] == 'lem:double-coset':
            locator = 'Lemma 1.1'  # inferred from adjacent commented label, review required
        else:
            locator = ''
        row['legacy_match'] = ('LOCATOR_PRESENT_NEEDS_SEMANTIC_REVIEW' if locator in matches
                               else 'NO_LOCATOR_MATCH' if locator else 'NOT_CHECKED')
    out.mkdir(parents=True, exist_ok=True)
    cols = ['category', 'environment', 'start_line', 'end_line', 'label', 'tex_excerpt',
            'review_status', 'legacy_match', 'statement_id']
    with (out / 'candidates.csv').open('w', encoding='utf-8-sig', newline='') as f:
        w = csv.DictWriter(f, fieldnames=cols); w.writeheader(); w.writerows(rows)
    named = [r for r in rows if r['category'] == 'named_statement']
    counters = {cat: sum(r['category'] == cat for r in rows) for cat in
                ('named_statement', 'numbered_math', 'unnumbered_math', 'unnumbered_display')}
    result = {'chapter': 1, 'source_sha256': hashlib.sha256(data).hexdigest(),
              'source_file': source.name, 'candidate_count': len(rows), 'category_counts': counters,
              'named_labels': [r['label'] for r in named],
              'legacy_file_checked': bool(legacy and legacy.exists()),
              'statement_ids_assigned': 0, 'source_verified': 0,
              'limitations': ['Candidates are TeX syntax spans, not distinct mathematical statements.',
                              'Prose definitions, inline math and unnumbered claims require manual full-text review.',
                              'A label/locator match is not proof of mathematical equivalence.',
                              'No existing registry or proof-search behavior is modified.']}
    (out / 'summary.json').write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    md = ['# Phase 163 R4-R15 — 第1章文献項目の暫定棚卸し', '',
          '原稿 TeX の構文に基づく**候補リスト**であり、命題単位の全件登録・原典との照合完了ではありません。', '',
          f'- 候補箇所: {len(rows)}',
          f'- 命題環境: {len(named)}',
          f'- ラベル: {", ".join(r["label"] for r in named)}',
          '- Statement ID 採番: 0（レビュー確定前の仮採番を禁止）',
          '- 認定済み原典照合: 0', '', '## 要確認', '',
          '1. 本文中の Definition・独立した数学的主張・インライン式を読み取る。',
          '2. 候補式が定義・仮定・等式・単なる計算のどれに該当するか判定する。',
          '3. 既存 Registry の数学的意味・条件・適用範囲を照合する。',
          '4. 原典照合後にのみ恒久 Statement ID と文献掲載順を登録する。',
          '', '## 保留事項', ''] + ['- ' + x for x in result['limitations']]
    (out / 'report.md').write_text('\n'.join(md) + '\n', encoding='utf-8')
    return result


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument('--source', type=Path, required=True)
    p.add_argument('--output', type=Path, required=True)
    p.add_argument('--legacy', type=Path)
    a = p.parse_args()
    print(json.dumps(run(a.source, a.output, a.legacy), ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
