"""Phase 164 R8-R4: read-only production ProofStep construction inventory.

Classifies sites, never rewrites mathematical proof origins or proof steps.
"""
from __future__ import annotations

import argparse
import ast
from collections import Counter, defaultdict
import json
from pathlib import Path

EXCLUDED_PREFIXES = (
    'apply_', 'audit_', 'diagnose_', 'debug_', 'fix_', 'run_',
    'probe_', 'inspect_', 'test_', 'check_', 'migrate_', 'patch_',
)
EXCLUDED_CONTAINS = ('_backup', '_bak', '_old', '_before_apply', '_pre_change', '_snapshot')
CORE = {'proof.py'}
REPLAY_TOKENS = ('replay', 'presentation', 'renderer', 'formatter')


def _name(node: ast.AST) -> str | None:
    if isinstance(node, ast.Name):
        return node.id
    if isinstance(node, ast.Attribute):
        return node.attr
    return None


def _rule(node: ast.Call) -> str:
    for keyword in node.keywords:
        if keyword.arg == 'rule':
            value = keyword.value
            if isinstance(value, ast.Attribute) and isinstance(value.value, ast.Name) and value.value.id == 'ProofRule':
                return value.attr
            return 'DYNAMIC'
    return 'UNKNOWN'


def _site_kind(name: str, rule: str, filename: str) -> str:
    if filename in CORE:
        return 'core_engine_keep_or_internal_refactor'
    if name == 'apply_inference_match':
        return 'inference_factory_migrate'
    if name == 'ProofStep':
        if rule == 'GIVEN':
            return 'given_source_boundary_review'
        if rule == 'INFERENCE':
            return 'inference_constructor_provenance_review'
        if rule in {'RELATION', 'EXACTNESS', 'EHP_EXACTNESS', 'KERNEL_COMPUTATION', 'IMAGE_COMPUTATION', 'COKERNEL_COMPUTATION'}:
            return 'typed_constructor_factory_migrate'
        return 'other_constructor_review'
    if name == 'replace':
        return 'dataclass_replace_type_review'
    return 'unclassified'


def inventory(root: Path) -> dict:
    root = Path(root)
    sites = []
    skipped = []
    errors = []
    scanned = 0
    for path in sorted(root.glob('*.py')):
        filename = path.name
        if filename.startswith(EXCLUDED_PREFIXES) or any(token in filename for token in EXCLUDED_CONTAINS):
            skipped.append(filename)
            continue
        try:
            tree = ast.parse(path.read_text(encoding='utf-8-sig'), filename=filename)
        except (SyntaxError, UnicodeError) as exc:
            errors.append({'file': filename, 'error': str(exc)})
            continue
        scanned += 1
        aliases = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.ImportFrom) and node.module == 'proof':
                for alias in node.names:
                    if alias.name == 'ProofStep':
                        aliases.add(alias.asname or alias.name)
        class Visitor(ast.NodeVisitor):
            def __init__(self):
                self.scope = []
            def visit_ClassDef(self, node):
                self.scope.append(node.name)
                self.generic_visit(node)
                self.scope.pop()
            def visit_FunctionDef(self, node):
                self.scope.append(node.name)
                self.generic_visit(node)
                self.scope.pop()
            visit_AsyncFunctionDef = visit_FunctionDef
            def visit_Call(self, node):
                name = _name(node.func)
                recognized = ((name in aliases or name == 'ProofStep') and name is not None) or name == 'apply_inference_match' or name == 'replace'
                if recognized:
                    kindname = 'ProofStep' if name in aliases else name
                    rule = _rule(node) if kindname == 'ProofStep' else None
                    kind = _site_kind(kindname, rule or '', filename)
                    if kindname == 'replace' and not isinstance(node.func, ast.Name):
                        kind = 'dataclass_replace_type_review'
                    sites.append({'file': filename, 'line': node.lineno, 'function': '.'.join(self.scope) or '<module>', 'call': kindname, 'rule': rule, 'category': kind})
                self.generic_visit(node)
        Visitor().visit(tree)
    sites.sort(key=lambda site: (site['file'], site['line'], site['call']))
    counts = dict(sorted(Counter(site['category'] for site in sites).items()))
    grouped = defaultdict(list)
    for site in sites:
        grouped[site['category']].append(site)
    candidate_files = {site['file'] for site in sites if site['category'] in {'given_source_boundary_review', 'inference_factory_migrate', 'inference_constructor_provenance_review', 'typed_constructor_factory_migrate', 'other_constructor_review'}}
    return {'phase': '164 R8-R4', 'mode': 'READ_ONLY_PRODUCTION_FACTORY_BATCH_PLANNING', 'scope': 'root-level Python with named tooling/backup files excluded', 'scanned_files': scanned, 'skipped_count': len(skipped), 'skipped_examples': skipped[:20], 'parse_errors': errors, 'category_counts': counts, 'migration_candidate_files': sorted(candidate_files), 'sites': sites, 'production_modified': False, 'full_pytest_run': False, 'r8_closed': False, 'limitations': ['AST sites are not runtime reachability evidence', 'replace() is not necessarily a ProofStep mutation', 'GIVEN constructors require source trust assessment', 'proof.py must not import a factory importing proof.py', 'replay reuse is not construction']}


def write_report(result: dict, output: Path) -> None:
    output = Path(output)
    output.mkdir(parents=True, exist_ok=True)
    (output / 'audit.json').write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    lines = ['# Phase 164 R8-R4 — ProofStep 生成経路の一括移行計画', '', '- 判定: **CLASSIFIED_NOT_YET_MIGRATED**', f'- 解析ファイル: {result["scanned_files"]}', f'- 除外ファイル: {result["skipped_count"]}', f'- 構文エラー: {len(result["parse_errors"])}', '- 本番コード変更: なし', '- 全体 pytest: 未実施', '', '## 分類件数', '']
    for name, count in result['category_counts'].items():
        lines.append(f'- `{name}`: {count}')
    lines += ['', '## 移行原則', '', '- GIVEN: 文献・原本・trusted roots の確認境界を維持し、無条件生成を禁止する。', '- INFERENCE: `apply_inference_match()` の規則検証を共通 Factory 経由にする。', '- Relation / Kernel / Image / Cokernel / Exactness: 型固有の検証を保つ。', '- `proof.py`: 循環 import を避けるため中核エンジンは直接逆依存させない。', '- Replay: 既存 ProofStep の identity を保持し、新たに生成しない。', '- `replace()`: 対象の型が ProofStep と確認できたものだけ移行候補。', '', '## 本番移行候補ファイル', '']
    for file in result['migration_candidate_files']:
        lines.append('- `' + file + '`')
    lines += ['', '## 移行候補一覧（行番号付き）', '']
    for site in result['sites']:
        if site['category'] not in ('dataclass_replace_type_review', 'core_engine_keep_or_internal_refactor'):
            lines.append(f'- `{site["file"]}:{site["line"]}` — `{site["function"]}` / `{site["call"]}` / `{site["rule"]}` / `{site["category"]}`')
    lines += ['', '## 次段階との境界', '', 'R8-R4 では全対象を一括分類する。以後は同一カテゴリー単位で Factory と呼び出し元をまとめて移行し、最後に残存箇所を再監査する。数学的根拠のない GIVEN の自動生成と ProofStep の再作成は行わない。', '']
    (output / 'report.md').write_text('\n'.join(lines), encoding='utf-8')


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument('--root', type=Path, default=Path('.'))
    parser.add_argument('--output', type=Path, default=Path('phase164_r8_r4_output'))
    args = parser.parse_args()
    result = inventory(args.root)
    write_report(result, args.output)
    print('\n'.join(['Phase 164 R8-R4 classified; no production changes', f'Files: {result["scanned_files"]}  Sites: {len(result["sites"])}  Parse errors: {len(result["parse_errors"])}', 'R8 not closed; full pytest NOT run']))
    if result['parse_errors']:
        raise SystemExit(1)


if __name__ == '__main__':
    main()
