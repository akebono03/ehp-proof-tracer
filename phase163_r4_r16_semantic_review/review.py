"""R4-R16: read-only, conservative semantic-review queue for Chapter I."""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
from pathlib import Path

from phase163_r4_r15_chapter1.inventory import extract, strip_comments, legacy_locators

COLUMNS = ('candidate_no', 'start_line', 'end_line', 'category', 'label',
           'provisional_unit', 'review_priority', 'context_signal', 'parent_named_label',
           'legacy_locator', 'legacy_locator_state', 'semantic_identity',
           'source_verification', 'statement_id', 'search_status', 'excerpt')


def locator_for(label: str) -> str:
    if label.startswith('prop:1-') and label[7:].isdigit():
        return 'Proposition 1.' + label[7:]
    if label == 'lem:double-coset':
        return 'Lemma 1.1 (provisional)'
    return ''


def classify_context(text: str, category: str) -> tuple[str, str, str]:
    """Classify for human review, never as mathematical proof of identity."""
    if category == 'named_statement':
        return 'NAMED_STATEMENT_REVIEW', 'HIGH', 'theorem_environment'
    excerpt = text.lower()
    if any(token in excerpt for token in ('\\begin{proof}', '証明', 'proof.')):
        return 'POSSIBLE_PROOF_INTERNAL', 'MEDIUM', 'proof_marker'
    if any(token in excerpt for token in ('定義', 'と定め', 'とおく', 'と書', 'を表す')):
        return 'POSSIBLE_DEFINITION', 'HIGH', 'definition_marker'
    if any(token in excerpt for token in ('\\cong', '\\simeq', '\\cong', '\\subseteq', '\\supseteq', '=')):
        return 'POSSIBLE_MATH_CLAIM', 'MEDIUM', 'relation_symbol'
    return 'MATH_SPAN_UNDETERMINED', 'HIGH', 'no_safe_signal'


def inventory(tex: str, legacy_text: str = '') -> list[dict[str, str | int]]:
    spans = extract(tex)
    lines = [strip_comments(line) for line in tex.splitlines()]
    known = set(re.findall(r'reference_locator\s*=\s*["\']([^"\']+)', legacy_text))
    rows: list[dict[str, str | int]] = []
    for i, item in enumerate(spans, 1):
        start = int(item['start_line']); end = int(item['end_line'])
        # Nearby prose is only a review hint, not a verified mathematical statement.
        context = ' '.join(lines[max(0, start - 4): min(len(lines), end + 3)])
        unit, priority, signal = classify_context(context, str(item['category']))
        label = str(item['label'])
        locator = locator_for(label)
        rows.append(dict(candidate_no=i, start_line=start, end_line=end,
                         category=item['category'], label=label,
                         provisional_unit=unit, review_priority=priority,
                         context_signal=signal, parent_named_label='',
                         legacy_locator=locator,
                         legacy_locator_state=('LOCATOR_ONLY_NOT_EQUIVALENCE' if locator in known else
                                               'NOT_MATCHED' if locator else 'NOT_APPLICABLE'),
                         semantic_identity='UNREVIEWED', source_verification='UNVERIFIED',
                         statement_id='', search_status='NOT_CONNECTED',
                         excerpt=item['tex_excerpt']))
    return rows


def nested_items(tex: str) -> list[dict[str, str | int]]:
    """Record enumerated components of named results as review candidates, not facts."""
    rows = []
    lines = tex.splitlines()
    for item in extract(tex):
        if item['category'] != 'named_statement':
            continue
        start, end = int(item['start_line']), int(item['end_line'])
        for index in range(start - 1, end):
            if re.search(r'\\item(?:\[[^]]*\])?', strip_comments(lines[index])):
                rows.append({'parent_label': item['label'], 'line': index + 1,
                             'indicator': 'enumerated_clause', 'status': 'REVIEW_REQUIRED'})
    return rows


def write_csv(path: Path, records: list[dict], fields: tuple[str, ...]) -> None:
    with path.open('w', newline='', encoding='utf-8-sig') as stream:
        writer = csv.DictWriter(stream, fieldnames=fields)
        writer.writeheader()
        writer.writerows(records)


def run(source: Path, out: Path, legacy: Path | None = None) -> dict:
    raw = source.read_bytes(); tex = raw.decode('utf-8-sig')
    legacy_text = legacy.read_text(encoding='utf-8-sig') if legacy and legacy.exists() else ''
    rows = inventory(tex, legacy_text)
    clauses = nested_items(tex)
    out.mkdir(parents=True, exist_ok=True)
    write_csv(out / 'semantic_review_queue.csv', rows, COLUMNS)
    write_csv(out / 'named_subclauses.csv', clauses, ('parent_label', 'line', 'indicator', 'status'))
    named = [r for r in rows if r['category'] == 'named_statement']
    summary = {'phase': '163 R4-R16', 'source_sha256': hashlib.sha256(raw).hexdigest(),
               'source_file': source.name, 'syntactic_candidates': len(rows),
               'named_statements': len(named), 'enumerated_clause_markers': len(clauses),
               'formal_statement_ids_assigned': 0, 'semantically_verified': 0,
               'existing_legacy_file_available': bool(legacy_text),
               'constraints': ['Review queue only; classifications are heuristic, not established mathematical identity.',
                               'Embedded prose and inline math require full human review.',
                               'Nested items are not automatically separate statements.',
                               'Locator coincidence never establishes equivalence.',
                               'No repository, registry, or proof-search code is changed.']}
    (out / 'summary.json').write_text(json.dumps(summary, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    report = [
        '# Phase 163 R4-R16 — 第1章の意味単位精査キュー', '',
        f'- TeX 構文候補: {len(rows)} 箇所',
        f'- 名前付き命題環境: {len(named)} 箇所',
        f'- 命題環境内の列挙項目マーカー: {len(clauses)} 箇所（個別命題件数ではない）',
        '- 原典との数学的同一性を検証済み: 0 件',
        '- Statement ID 正式発行: 0 件', '',
        '## 運用', '',
        'semantic_review_queue.csv を掲載順に確認し、数学的主張・定義・証明中間式・重複表現を人手で確定する。',
        '既存67成分との一致は名前や locator の一致だけでは確定しない。',
        '命題環境に含まれる複数の主張は named_subclauses.csv で別途確認する。',
        '本文中の独立命題・インライン数式は現時点で網羅されていない。',
        '原典照合済みとするには Toda 原典（翻刻原稿とは区別）との比較が必要。',
        '既存コードを変更せず、全体テストは Phase 終了時のみ実施する。', ''
    ]
    (out / 'report.md').write_text('\n'.join(report), encoding='utf-8')
    return summary


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument('--source', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--legacy', type=Path)
    args = parser.parse_args()
    print(json.dumps(run(args.source, args.output, args.legacy), ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
