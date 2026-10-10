"""Phase 163 R4-R2: read-only, scoped registration-site coverage audit.

This is a static source-site inventory, not a count of distinct math claims.
"""
from __future__ import annotations

import ast
import csv
import json
from collections import Counter
from pathlib import Path


ENTRY_NAMES = frozenset({
    'ProofRepositoryEntry', 'TheoremFactEntry',
    'GeneratorTypingFact', 'GeneratorAmbientGroupFact',
    'ZeroCompositionFactEntry', 'MapIsomorphismFactEntry',
    'AssertionEntry', 'TodaFixedStatementComponent',
})
REGISTRY_NAMES = frozenset({
    'register', 'add_assertion', 'add_reference',
    'build_standard_proof_repository',
})
CORE_FILES = (
    'toda_rules.py', 'theorem_facts.py', 'proof_repository.py',
    'standard_repository.py', 'toda_literature_statement_boundary.py',
    'generator_facts.py',
)
EXCLUDED_PREFIXES = ('phase', 'archive', 'backup', 'test_', 'probe_')


def call_name(node: ast.AST) -> str | None:
    if isinstance(node, ast.Name):
        return node.id
    if isinstance(node, ast.Attribute):
        return node.attr
    return None


def literal_keyword(node: ast.Call, key: str) -> str | None:
    for kw in node.keywords:
        if kw.arg == key and isinstance(kw.value, ast.Constant):
            if isinstance(kw.value.value, str):
                return kw.value.value
    return None


def inspect_source(path: Path, root: Path) -> list[dict[str, object]]:
    text = path.read_text(encoding='utf-8-sig')
    tree = ast.parse(text, filename=str(path))
    rows: list[dict[str, object]] = []
    for node in ast.walk(tree):
        if isinstance(node, (ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef)):
            if isinstance(node, ast.ClassDef) and (node.name.endswith('Statement') or node.name.endswith('Definition')):
                kind = 'statement_or_definition_class'
            elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and (
                node.name.startswith(('build_', 'register_', 'get_')) and
                any(token in node.name.lower() for token in ('repository', 'registry', 'fact'))
            ):
                kind = 'repository_factory_candidate'
            else:
                continue
            symbol = node.name
            key = ''
        elif isinstance(node, ast.Call):
            symbol = call_name(node.func)
            if symbol in ENTRY_NAMES:
                kind = 'entry_constructor_site'
            elif symbol in REGISTRY_NAMES:
                kind = 'registry_or_factory_call_site'
            else:
                continue
            key = literal_keyword(node, 'key') or literal_keyword(node, 'assertion_id') or ''
        else:
            continue
        rows.append({
            'file': path.relative_to(root).as_posix(), 'line': node.lineno,
            'kind': kind, 'symbol': symbol, 'explicit_key': key,
            'mapping_status': 'not_verified',
        })
    return rows


def scan_root(root: Path) -> tuple[list[dict[str, object]], list[str]]:
    """Inspect active root Python modules only; no recursive archive inclusion."""
    rows: list[dict[str, object]] = []
    errors: list[str] = []
    for path in sorted(root.glob('*.py')):
        if path.name.startswith(EXCLUDED_PREFIXES):
            continue
        try:
            rows.extend(inspect_source(path, root))
        except (SyntaxError, UnicodeError, OSError) as exc:
            errors.append(f'{path.name}: {type(exc).__name__}: {exc}')
    return rows, errors


def summarize(rows: list[dict[str, object]]) -> dict[str, int]:
    return dict(sorted(Counter(str(row['kind']) for row in rows).items()))


def audit(root: Path, output: Path) -> dict[str, object]:
    rows, errors = scan_root(root)
    missing_core = [name for name in CORE_FILES if not (root / name).is_file()]
    # Bridge evidence intentionally does not equate metadata with typed theorems.
    bridge_counts = None
    bridge_issue = None
    try:
        from phase163_r4_registry_bridge import build_registry_bridge
        result = build_registry_bridge()
        bridge_counts = dict(sorted(Counter(r.status.value for r in result.records).items()))
        unresolved = [{'source': r.source, 'key': r.source_key,
                       'detail': r.detail} for r in result.unresolved]
    except (ImportError, ValueError, KeyError, TypeError, AttributeError) as exc:
        bridge_issue = f'{type(exc).__name__}: {exc}'
        unresolved = []

    report = {
        'audit_type': 'static active-root source sites + default bridge snapshot',
        'scope': 'Python modules directly in repository root; excludes tests, archives and phase folders',
        'files_scanned': len([p for p in root.glob('*.py') if not p.name.startswith(EXCLUDED_PREFIXES)]),
        'site_count': len(rows), 'site_counts_by_kind': summarize(rows),
        'missing_core_files': missing_core, 'parse_errors': errors,
        'bridge_status_counts': bridge_counts, 'bridge_unresolved': unresolved,
        'bridge_error': bridge_issue,
        'limitations': [
            'A constructor site is not a runtime record and not a unique mathematical statement.',
            'Statement class definitions are types, not registered theorem instances.',
            'Dynamically constructed registrations and indirect factories may not be captured.',
            'Rule catalog statements are not automatically literature-fixed statements.',
            'Equivalent, duplicate, specialized and generic mathematical assertions remain unclassified.',
            'Definition provenance, proof completion order and citation permission are not inferred.',
            'R4 integration is incomplete; no backward search or renderer integration.',
        ],
    }
    output.mkdir(parents=True, exist_ok=True)
    (output / 'summary.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    with (output / 'sites.csv').open('w', newline='', encoding='utf-8-sig') as f:
        writer = csv.DictWriter(f, fieldnames=['file', 'line', 'kind', 'symbol', 'explicit_key', 'mapping_status'])
        writer.writeheader()
        writer.writerows(rows)
    lines = [
        '# Phase 163 R4-R2 — 全登録経路の網羅性監査（途中結果）', '',
        '## 対象と測定単位',
        f'- 直接配置された Python ファイル: {report["files_scanned"]} 件',
        f'- 静的候補箇所: {len(rows)} 件（命題数ではない）',
        '- 監査範囲: リポジトリ直下の稼働コード。テスト・archive・過去 phase フォルダは除外。',
        '', '## 静的候補の分類',
    ]
    lines.extend(f'- {key}: {value}' for key, value in report['site_counts_by_kind'].items())
    lines.extend(['', '## R4 Bridge', ''])
    if bridge_counts is not None:
        lines.extend(f'- {key}: {value}' for key, value in bridge_counts.items())
    else:
        lines.append(f'- 実行時監査不能: {bridge_issue}')
    lines.extend(['', '## 未解決の出典', ''])
    lines.extend(f'- {x["source"]}/{x["key"]}: {x["detail"]}' for x in unresolved)
    if not unresolved:
        lines.append('- なし（今回 bridge が成功し、対象の未解決がない場合に限る）' if bridge_counts is not None else '- bridge 未実行')
    lines.extend(['', '## 調査上の未達成項目', ''])
    lines.extend(f'- {item}' for item in report['limitations'])
    if missing_core:
        lines.extend(['', '## 見つからない中心ファイル', *[f'- {x}' for x in missing_core]])
    if errors:
        lines.extend(['', '## 構文解析エラー', *[f'- {x}' for x in errors]])
    lines.extend(['', '## 判定', '',
                  '**全登録命題の網羅性は未確認。今回の件数から数学的な全命題数を算出しない。**',
                  'Phase 163 R4-R2 は読み取り専用の監査段階である。全体 pytest は行わない。'])
    (output / 'report.md').write_text('\n'.join(lines) + '\n', encoding='utf-8')
    return report


if __name__ == '__main__':
    result = audit(Path.cwd(), Path.cwd() / 'phase163_r4_r2_output')
    print('Phase 163 R4-R2 static candidate sites:', result['site_count'])
    print('Bridge status:', result['bridge_status_counts'])
    print('Saved: phase163_r4_r2_output/report.md and sites.csv')
    print('Not a unique theorem count. Full suite not run.')
