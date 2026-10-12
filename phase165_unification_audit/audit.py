from __future__ import annotations

import ast
import json
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUTPUT = ROOT / 'phase165_unification_audit_output'
EXCLUDED = {'tests', 'archive', 'probes', '.git', '.venv', 'venv', '__pycache__'}
LEGACY = {
    'phase162_pi5_3_web_replay',
    'phase162_web_narrative_integration',
    'phase162_pi5_3_backward_selection',
    'phase164_r5_web_registry_connection',
}
PREREQUISITE_SELECTORS = {
    'build_phase50_representative_result',
    'build_phase56_representative_result',
    '_phase162_ehp_leaves',
    'create_legacy_given_proof_step',
}

def is_production(path: Path) -> bool:
    parts = path.relative_to(ROOT).parts
    if any(part in EXCLUDED or part.startswith('phase') and len(parts) > 1 for part in parts[:-1]):
        return False
    return path.parent == ROOT and path.suffix == '.py'


def main() -> int:
    OUTPUT.mkdir(exist_ok=True)
    modules = {}
    parse_errors = []
    imports = defaultdict(list)
    symbols = defaultdict(list)
    for path in sorted(ROOT.glob('*.py')):
        if not is_production(path):
            continue
        try:
            tree = ast.parse(path.read_text(encoding='utf-8-sig'), filename=str(path))
        except (SyntaxError, UnicodeError) as exc:
            parse_errors.append({'file': path.name, 'error': str(exc)})
            continue
        modules[path.stem] = path.name
        for node in ast.walk(tree):
            if isinstance(node, ast.ImportFrom) and node.module:
                imports[node.module.split('.')[0]].append({'file': path.name, 'line': node.lineno, 'imported': [a.name for a in node.names]})
            elif isinstance(node, ast.Import):
                for name in node.names:
                    imports[name.name.split('.')[0]].append({'file': path.name, 'line': node.lineno, 'imported': ['*']})
            elif isinstance(node, ast.Call):
                name = None
                if isinstance(node.func, ast.Name):
                    name = node.func.id
                elif isinstance(node.func, ast.Attribute):
                    name = node.func.attr
                if name in PREREQUISITE_SELECTORS:
                    symbols[name].append({'file': path.name, 'line': node.lineno})
    legacy = {name: {'exists': name in modules, 'imported_by': imports.get(name, [])} for name in sorted(LEGACY)}
    report = {
        'phase': '165 unification and cleanup audit',
        'mode': 'READ_ONLY',
        'production_root_python_count': len(modules),
        'parse_errors': parse_errors,
        'legacy_module_references': legacy,
        'prerequisite_selector_calls': dict(sorted(symbols.items())),
        'safe_to_delete_production_modules': [],
        'reason': 'Static AST references alone cannot establish complete runtime reachability or reflection-based imports.',
        'full_pytest_run': False,
    }
    (OUTPUT / 'report.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    lines = ['# Phase 165: 統一・旧実装の監査', '', '本監査は読み取り専用で、既存ファイルを削除しません。', '', f'本番ルート Python: {len(modules)} 件', f'構文解析エラー: {len(parse_errors)} 件', '', '## 旧モジュールへの参照']
    for name, detail in legacy.items():
        lines.append(f'- `{name}`: 存在={detail["exists"]}, 静的 import={len(detail["imported_by"])}')
        for source in detail['imported_by']:
            lines.append(f'  - `{source["file"]}:{source["line"]}`')
    lines.extend(['', '## 前提選択・GIVEN 生成の呼び出し'])
    for name, uses in sorted(symbols.items()):
        lines.append(f'- `{name}`: {len(uses)} 件')
        for use in uses:
            lines.append(f'  - `{use["file"]}:{use["line"]}`')
    lines.extend(['', '## 判定', '削除確定ファイル: 0 件。動的 import・既存 API・テスト依存の確認前には自動削除しません。', '全体 pytest は実行していません。'])
    (OUTPUT / 'report.md').write_text('\n'.join(lines) + '\n', encoding='utf-8')
    print('\n'.join(lines[:17]))
    print('Report:', OUTPUT / 'report.md')
    return 0 if not parse_errors else 1


if __name__ == '__main__':
    raise SystemExit(main())
