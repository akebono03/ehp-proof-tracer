"""Read-only, AST-based Phase 165 R6-2 R4-A inventory.

No production module is imported, and no repository file is modified.
"""
from __future__ import annotations

import argparse
import ast
from collections import Counter
from datetime import datetime, timezone
import json
from pathlib import Path
import re

DEFAULT_MODULES = (
    'ehp_rules', 'stable_rules', 'set_rules', 'hopf_rules',
    'scalar_rules', 'relation_rules', 'map_property_rules',
    'homomorphism_rules', 'indeterminacy_rules',
)
SKIP_DIRS = {'.git', '.venv', 'venv', '__pycache__', '.pytest_cache', 'node_modules', 'archive', 'dist', 'build'}
PRODUCTION = (
    'phase165_r8_rule_provider.py', 'rule_catalog.py',
    'phase165_r57_r26_generic_search_connection.py',
    'phase165_r52_r9_shared_math.py',
)
CONNECTION_FUNCTIONS = {
    'create_rule_expansion_provider': 'symbolic_inverse',
    'build_generic_backward_expansion_provider': 'generic_unification',
    'reverse_rules_from_witnesses': 'verified_witness',
    'generate_seeded_backward_goals': 'seeded_witness',
}


def _function_names(tree: ast.AST) -> set[str]:
    return {n.name for n in ast.walk(tree) if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))}


def _called_name(node: ast.AST) -> str:
    if isinstance(node, ast.Name):
        return node.id
    if isinstance(node, ast.Attribute):
        return node.attr
    return ''


def _read_tree(path: Path) -> tuple[ast.AST | None, str | None]:
    try:
        return ast.parse(path.read_text(encoding='utf-8-sig'), filename=str(path)), None
    except (OSError, UnicodeError, SyntaxError) as exc:
        return None, f'{type(exc).__name__}: {exc}'


def _paths(root: Path):
    # Only top-level production modules, recursively for tests. Archived or
    # installer copies must never inflate live rule counts.
    yield from sorted(root.glob('*.py'))


def _source_defs(root: Path) -> tuple[list[dict], list[dict]]:
    definitions = []
    problems = []
    for path in _paths(root):
        tree, error = _read_tree(path)
        if error:
            problems.append({'file': path.name, 'error': error})
            continue
        assert tree is not None
        for n in tree.body:
            if not isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef)):
                continue
            calls = [c for c in ast.walk(n) if isinstance(c, ast.Call)]
            constructs = any(_called_name(c.func) == 'InferenceRule' for c in calls)
            if not (constructs or n.name.endswith('_inference_rule')):
                continue
            required = []
            arguments = n.args.posonlyargs + n.args.args
            required_pos = len(arguments) - len(n.args.defaults)
            required.extend(x.arg for x in arguments[:required_pos])
            required.extend(x.arg for x, default in zip(n.args.kwonlyargs, n.args.kw_defaults) if default is None)
            direct_rules = [c for c in calls if _called_name(c.func) == 'InferenceRule']
            names = []
            has_conclusion_pattern = False
            has_premises = False
            for c in direct_rules:
                for kw in c.keywords:
                    if kw.arg == 'name' and isinstance(kw.value, ast.Constant) and isinstance(kw.value.value, str):
                        names.append(kw.value.value)
                    if kw.arg == 'conclusion_pattern' and not (isinstance(kw.value, ast.Constant) and kw.value.value is None):
                        has_conclusion_pattern = True
                    if kw.arg == 'premise_patterns':
                        has_premises = True
            eligible = (path.stem in DEFAULT_MODULES and n.name.endswith('_inference_rule') and not required)
            definitions.append({
                'id': f'{path.stem}.{n.name}', 'file': path.name,
                'function': n.name, 'line': n.lineno, 'constructs_inference_rule': constructs,
                'reported_rule_names': names, 'direct_conclusion_pattern': has_conclusion_pattern,
                'direct_premise_patterns': has_premises,
                'required_parameters': required, 'r8_factory_eligible_by_ast': eligible,
                'backward_capability': 'UNKNOWN', 'forward_capability': 'UNKNOWN',
                'search_connected': 'UNKNOWN', 'tested': 'UNKNOWN',
                'limitation': 'Static inventory: runtime predicates, guards and generated patterns not evaluated.',
            })
    return definitions, problems


def _connection_scan(root: Path) -> dict:
    result = {}
    for relative in PRODUCTION:
        path = root / relative
        if not path.is_file():
            result[relative] = {'present': False, 'functions': [], 'calls': [], 'imports': []}
            continue
        tree, error = _read_tree(path)
        if error:
            result[relative] = {'present': True, 'parse_error': error, 'functions': [], 'calls': [], 'imports': []}
            continue
        calls = sorted({_called_name(c.func) for c in ast.walk(tree) if isinstance(c, ast.Call)})
        imports = sorted({alias.name for n in ast.walk(tree) if isinstance(n, ast.ImportFrom) for alias in n.names})
        result[relative] = {'present': True, 'functions': sorted(_function_names(tree)), 'calls': calls, 'imports': imports}
    shared = result.get('phase165_r52_r9_shared_math.py', {})
    generic = result.get('phase165_r57_r26_generic_search_connection.py', {})
    shared_calls = set(shared.get('calls', ()))
    shared_imports = set(shared.get('imports', ()))
    generic_calls = set(generic.get('calls', ()))
    result['paths'] = {
        'symbolic_via_generic': {
            'evidence': 'build_generic_backward_expansion_provider' in shared_calls and 'discover_explicit_goal_candidates' in generic_calls and 'generate_discovered_premises' in generic_calls,
            'status': 'STATIC_CONNECTION_ONLY',
        },
        'verified_witness': {
            'evidence': 'reverse_rules_from_witnesses' in shared_calls,
            'status': 'STATIC_CONNECTION_ONLY',
        },
        'seeded_witness': {
            'evidence': 'generate_seeded_backward_goals' in shared_calls,
            'status': 'STATIC_CONNECTION_ONLY',
        },
        'pi43_adapter': {
            'evidence': 'expand_existing_pi43_rules' in shared_calls or 'expand_existing_pi43_rules' in shared_imports,
            'status': 'STATIC_CONNECTION_ONLY',
        },
    }
    return result


def _test_inventory(root: Path) -> list[dict]:
    output = []
    directory = root / 'tests'
    if not directory.is_dir():
        return output
    for path in sorted(directory.rglob('test_*.py')):
        if any(part in SKIP_DIRS for part in path.relative_to(root).parts):
            continue
        tree, error = _read_tree(path)
        if error:
            output.append({'file': str(path.relative_to(root)), 'error': error, 'tests': []})
            continue
        names = [n.name for n in ast.walk(tree) if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef)) and n.name.startswith('test_')]
        output.append({'file': str(path.relative_to(root)), 'tests': names})
    return output


def audit(root: Path) -> dict:
    root = root.resolve()
    if not root.is_dir():
        raise ValueError(f'not a directory: {root}')
    definitions, errors = _source_defs(root)
    connections = _connection_scan(root)
    tests = _test_inventory(root)
    return {
        'phase': '165 R6-2 R4-A', 'mode': 'READ_ONLY_STATIC_AUDIT',
        'root': str(root), 'generated_utc': datetime.now(timezone.utc).isoformat(),
        'default_rule_modules': list(DEFAULT_MODULES),
        'definitions': definitions, 'connections': connections,
        'test_inventory': tests, 'parse_errors': errors,
        'summary': {
            'rule_factory_or_constructor_functions': len(definitions),
            'r8_factory_eligible_by_ast': sum(x['r8_factory_eligible_by_ast'] for x in definitions),
            'top_level_python_modules': len(list(_paths(root))),
            'test_functions_discovered': sum(len(x['tests']) for x in tests),
            'parse_errors': len(errors),
            'runtime_usable_rules_verified': 0,
        },
        'caveats': [
            'An eligible factory is not necessarily a successfully discovered runtime rule.',
            'A discovered rule is not necessarily backwards applicable for any given Goal.',
            'A static connection does not prove successful reconstruction.',
            'Rule definitions in nested functions, dynamically generated code and non-root packages are not exhaustively inventoried.',
            'No rule, reference, mathematical validity or test result is certified by this report.',
        ],
    }


def markdown_report(report: dict) -> str:
    s = report['summary']
    lines = [
        '# Phase 165 R6-2 R4-A 読み取り専用監査', '',
        f"- 対象: `{report['root']}`", '- 方式: AST 静的解析（本番コードの import・書換えなし）',
        f"- 規則候補を含むトップレベル関数: {s['rule_factory_or_constructor_functions']}",
        f"- R8 自動収集条件に構文上合致: {s['r8_factory_eligible_by_ast']}",
        f"- `tests/` で発見したテスト関数: {s['test_functions_discovered']}",
        f"- Python 解析エラー: {s['parse_errors']}", '',
        '## 探索への接続（静的証拠）', '',
        '| 経路 | 構文上の接続 | 実行検証 |', '|---|---|---|',
    ]
    for name, item in report['connections']['paths'].items():
        lines.append(f"| `{name}` | {'あり' if item['evidence'] else '未確認'} | 未実施 |")
    lines += ['', '## 規則候補', '', '| ID | 行 | R8収集条件 | Backward | 探索接続 |', '|---|---:|---|---|---|']
    for item in report['definitions']:
        lines.append(f"| `{item['id']}` | {item['line']} | {'合致' if item['r8_factory_eligible_by_ast'] else '対象外'} | UNKNOWN | UNKNOWN |")
    lines += ['', '## 留保事項', '']
    lines.extend(f'- {x}' for x in report['caveats'])
    lines += ['', '## 次 Phase との境界', '', 'R4-A は存在・収集条件・接続構文のみ監査する。R4-B で runtime 実証・分類を行い、R5 以降で不足規則を実装する。', '']
    return '\n'.join(lines)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument('--root', required=True, type=Path)
    parser.add_argument('--out', required=True, type=Path)
    args = parser.parse_args()
    result = audit(args.root)
    args.out.mkdir(parents=True, exist_ok=True)
    (args.out / 'rule_inventory.json').write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    (args.out / 'rule_inventory.md').write_text(markdown_report(result), encoding='utf-8')
    print(json.dumps({'status': 'AUDITED_READ_ONLY', 'summary': result['summary'], 'output': str(args.out)}, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
