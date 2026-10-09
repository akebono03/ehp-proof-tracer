"""Phase 163 R1I: read-only singleton registry coverage audit."""
from __future__ import annotations
import argparse
import ast
import csv
import importlib
import json
from pathlib import Path


def discover_singletons(source_root: Path) -> list[dict]:
    rows = []
    for path in sorted(source_root.glob('*.py')):
        try:
            tree = ast.parse(path.read_text(encoding='utf-8-sig'), filename=str(path))
        except (SyntaxError, UnicodeError) as exc:
            rows.append({'file': path.name, 'name': '(parse error)', 'line': 0, 'expression': str(exc)})
            continue
        for node in tree.body:
            targets = []
            if isinstance(node, ast.Assign):
                targets = [t.id for t in node.targets if isinstance(t, ast.Name)]
            elif isinstance(node, ast.AnnAssign) and isinstance(node.target, ast.Name):
                targets = [node.target.id]
            for name in targets:
                if name.endswith('_REPOSITORY') or name.endswith('_CATALOG'):
                    expr = ast.unparse(node.value) if node.value is not None else ''
                    rows.append({'file': path.name, 'name': name, 'line': node.lineno, 'expression': expr[:240]})
    return rows


def inspect_composition() -> dict:
    module = importlib.import_module('composition_facts')
    repo = module.ZERO_COMPOSITION_FACT_REPOSITORY
    entries = tuple(repo.facts)
    return {'repository': 'ZERO_COMPOSITION_FACT_REPOSITORY', 'entry_count': len(entries),
            'fact_types': [type(x).__name__ for x in entries],
            'relation_types': [x.relation_type.name for x in entries]}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('--source-root', type=Path, default=Path.cwd())
    parser.add_argument('--output', type=Path, default=Path('phase163_r1i_output'))
    args = parser.parse_args()
    rows = discover_singletons(args.source_root)
    errors = []
    try:
        composition = inspect_composition()
    except Exception as exc:
        composition = None
        errors.append(f'{type(exc).__name__}: {exc}')
    args.output.mkdir(parents=True, exist_ok=True)
    with (args.output / 'singleton_registry_definitions.csv').open('w', newline='', encoding='utf-8-sig') as f:
        writer = csv.DictWriter(f, fieldnames=['file', 'name', 'line', 'expression'])
        writer.writeheader()
        writer.writerows(rows)
    summary = {
        'phase': '163 R1I',
        'scope': 'top-level *.py in project root only; no archive / phase patch folders',
        'singleton_definition_sites': len(rows),
        'composition_repository': composition,
        'errors': errors,
        'not_confirmed': [
            'runtime factory-created registries not enumerated',
            'full literature statement identity and deduplication',
            'publication order and proof-completion positions',
            'dependency eligibility and fixed-versus-proof-internal semantics',
        ],
        'status': 'R1 INVENTORY EVIDENCE; full mathematical statement count not established',
    }
    (args.output / 'summary.json').write_text(json.dumps(summary, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    lines = ['# Phase 163 R1I 登録方式の残件確認', '',
             '既知の実行時 Repository: R1G で theorem=1, standard proof=4。R1H で map=1, generator typing=3, ambient=3。',
             'これらは異なる種類の登録実体であり、数学的命題数として合計しない。', '',
             f'今回のプロジェクト直下の *_REPOSITORY / *_CATALOG 定義箇所: {len(rows)}',
             f'零合成事実の実行時件数: {composition["entry_count"] if composition else "取得失敗"}', '',
             '## 境界',
             '- R1 は登録場所・登録方式の棚卸しと未確認事項の記録を担当する。',
             '- R2 は Statement ID と登録構造の設計。',
             '- R3 は文献掲載順と証明完了位置の確認。',
             '- R5 は依存関係と使用可能性の検証。',
             '- R4 の統合までは網羅的な登録命題総数を断定しない。', '']
    (args.output / 'report.md').write_text('\n'.join(lines), encoding='utf-8')
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 1 if errors else 0


if __name__ == '__main__':
    raise SystemExit(main())
