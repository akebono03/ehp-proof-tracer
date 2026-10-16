"""R6-1 R3: bounded review of the existing R2 classification; no production writes."""
from __future__ import annotations
import ast
import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
HERE = Path(__file__).resolve().parent
SOURCE = ROOT / 'phase165_r6_1_r2_classification' / 'classification.json'
REVIEW = {'NAMED_GROUP_BRANCH_REVIEW', 'GROUP_TYPE_BRANCH_REVIEW', 'ACTIVE_GROUP_SPECIFIC_ADAPTER', 'GROUP_SPECIFIC_ADAPTER_NOT_REACHED_BY_IMPORT_GRAPH'}
SEARCH_TERMS = ('goal', 'expand', 'search', 'backward', 'provider', 'reconstruct', 'rule')


def classify_candidate(record: dict) -> dict:
    """Evidence-based triage; ambiguous branches remain unresolved for human review."""
    category = record['category']
    path = record['file']
    function = record['function']
    conditions = record.get('conditions', [])
    texts = ' '.join(c.get('expression', '') for c in conditions)
    if category in ('ACTIVE_GROUP_SPECIFIC_ADAPTER', 'GROUP_SPECIFIC_ADAPTER_NOT_REACHED_BY_IMPORT_GRAPH'):
        disposition = 'REPLACE_WITH_GENERIC_RULE_BEFORE_REMOVAL'
        reason = '群専用の逆向き前提生成が明示的に登録されている'
    elif category == 'NAMED_GROUP_BRANCH_REVIEW':
        disposition = 'MANUAL_REVIEW_NAMED_GOAL_BRANCH'
        reason = '固定された群名に基づく条件があり、証明経路の固定かを確認する必要がある'
    else:
        disposition = 'MANUAL_REVIEW_GROUP_TYPE_BRANCH'
        reason = '群の型・次数判定は正当な型検査の可能性があるため自動撤去しない'
    return {'file': path, 'function': function, 'line': record['line'],
            'original_category': category, 'disposition': disposition, 'reason': reason,
            'reachable_by_imports': record.get('reachable_by_imports', False),
            'import_path': record.get('import_path', []),
            'importers': record.get('importers', []),
            'conditions': conditions, 'keywords_in_condition': [w for w in SEARCH_TERMS if w in texts.lower()]}


def run(source: Path = SOURCE, output: Path = HERE) -> dict:
    original = json.loads(source.read_text(encoding='utf-8'))
    rows = [classify_candidate(r) for r in original['records'] if r['category'] in REVIEW]
    counts = dict(Counter(row['original_category'] for row in rows))
    active = [r for r in rows if r['disposition'] == 'REPLACE_WITH_GENERIC_RULE_BEFORE_REMOVAL' and r['reachable_by_imports']]
    report = {'phase': '165 R6-1 R3', 'mode': 'READ_ONLY',
              'source': str(source), 'counts': counts, 'reviewed_candidates': len(rows),
              'confirmed_by_prior_static_audit': [r['file'] + ':' + r['function'] for r in active],
              'status': 'PENDING_MANUAL_SEMANTIC_REVIEW',
              'limitations': ['R2はトップレベルの探索関連関数のみを対象とする',
                              'import到達性は実行時の呼び出しを証明しない',
                              '116候補すべてを自動で正当・不要と断定できない',
                              '撤去前に規則の一般化と回帰テストが必要'],
              'candidates': rows}
    output.mkdir(parents=True, exist_ok=True)
    (output / 'triage.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    lines = ['# Phase 165 R6-1 R3 最終候補監査', '',
             '**注：この結果だけでR6-1の完了・全群専用処理の撤去を宣言しません。**', '',
             '## 分類件数', '']
    lines += [f'- {k}: {v}' for k, v in sorted(counts.items())]
    lines += ['', '## 確認済みの撤去候補（置換前の削除は禁止）', '']
    lines += [f'- `{x}`' for x in report['confirmed_by_prior_static_audit']] or ['- なし']
    for category in ('ACTIVE_GROUP_SPECIFIC_ADAPTER', 'NAMED_GROUP_BRANCH_REVIEW', 'GROUP_TYPE_BRANCH_REVIEW', 'GROUP_SPECIFIC_ADAPTER_NOT_REACHED_BY_IMPORT_GRAPH'):
        items = [r for r in rows if r['original_category'] == category]
        if not items:
            continue
        lines += ['', f'## {category}（{len(items)}件）', '']
        for row in items:
            condition = ' | '.join(c['expression'].replace('`', "'").replace('\n', ' ') for c in row['conditions'])
            lines.append(f"- `{row['file']}:{row['line']}` `{row['function']}` / import到達={row['reachable_by_imports']} / {row['disposition']}")
            if condition:
                lines.append(f'  - 条件: `{condition[:240]}`')
            if row['import_path']:
                lines.append('  - 経路: ' + ' → '.join(f'`{x}`' for x in row['import_path']))
    lines += ['', '## 限界', ''] + ['- ' + x for x in report['limitations']]
    (output / 'triage.md').write_text('\n'.join(lines) + '\n', encoding='utf-8')
    return report


if __name__ == '__main__':
    result = run()
    print(json.dumps({'phase': result['phase'], 'status': result['status'], 'reviewed_candidates': result['reviewed_candidates'], 'counts': result['counts'], 'confirmed_by_prior_static_audit': result['confirmed_by_prior_static_audit'], 'output': str(HERE / 'triage.md')}, ensure_ascii=False, indent=2))
